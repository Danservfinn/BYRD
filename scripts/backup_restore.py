#!/usr/bin/env python3
"""
BYRD Backup and Restore Script

Creates checkpoints of the Neo4j database state that can be restored later.
Use this before major architecture changes.

Usage:
    python scripts/backup_restore.py backup              # Create backup
    python scripts/backup_restore.py backup my-checkpoint  # Named backup
    python scripts/backup_restore.py list                # List backups
    python scripts/backup_restore.py restore <name>      # Restore backup
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
import yaml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory import Memory


BACKUP_DIR = Path(__file__).parent.parent / "backups"


async def create_backup(name: str = None) -> str:
    """Export entire Neo4j graph to JSON file."""

    # Load config
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Connect to database
    memory = Memory(config.get("database", {}))
    await memory.connect()

    try:
        # Export all nodes
        nodes_result = await memory._run_query("""
            MATCH (n)
            RETURN
                id(n) as neo_id,
                labels(n) as labels,
                properties(n) as props
        """)

        # Export all relationships
        rels_result = await memory._run_query("""
            MATCH (a)-[r]->(b)
            RETURN
                id(r) as rel_id,
                type(r) as rel_type,
                properties(r) as props,
                id(a) as source_id,
                id(b) as target_id
        """)

        # Create backup data
        backup_data = {
            "created_at": datetime.now().isoformat(),
            "node_count": len(nodes_result),
            "relationship_count": len(rels_result),
            "nodes": [
                {
                    "neo_id": n["neo_id"],
                    "labels": n["labels"],
                    "properties": dict(n["props"]) if n["props"] else {}
                }
                for n in nodes_result
            ],
            "relationships": [
                {
                    "rel_id": r["rel_id"],
                    "type": r["rel_type"],
                    "properties": dict(r["props"]) if r["props"] else {},
                    "source_id": r["source_id"],
                    "target_id": r["target_id"]
                }
                for r in rels_result
            ]
        }

        # Create backup directory
        BACKUP_DIR.mkdir(exist_ok=True)

        # Generate filename
        if name:
            filename = f"{name}.json"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"backup_{timestamp}.json"

        backup_path = BACKUP_DIR / filename

        # Write backup
        with open(backup_path, "w") as f:
            json.dump(backup_data, f, indent=2, default=str)

        print(f"Backup created: {backup_path}")
        print(f"  Nodes: {backup_data['node_count']}")
        print(f"  Relationships: {backup_data['relationship_count']}")

        return str(backup_path)

    finally:
        await memory.close()


async def restore_backup(name: str):
    """Restore Neo4j graph from JSON backup."""

    # Find backup file
    if name.endswith(".json"):
        backup_path = BACKUP_DIR / name
    else:
        backup_path = BACKUP_DIR / f"{name}.json"

    if not backup_path.exists():
        print(f"Backup not found: {backup_path}")
        print("Available backups:")
        await list_backups()
        return

    # Load backup
    with open(backup_path) as f:
        backup_data = json.load(f)

    print(f"Restoring from: {backup_path}")
    print(f"  Created: {backup_data['created_at']}")
    print(f"  Nodes: {backup_data['node_count']}")
    print(f"  Relationships: {backup_data['relationship_count']}")

    # Confirm
    response = input("\nThis will CLEAR the current database. Continue? [y/N] ")
    if response.lower() != "y":
        print("Aborted.")
        return

    # Load config
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Connect to database
    memory = Memory(config.get("database", {}))
    await memory.connect()

    try:
        # Clear existing data
        print("Clearing existing data...")
        await memory._run_query("MATCH (n) DETACH DELETE n")

        # Create ID mapping (old neo_id -> new neo_id)
        id_mapping = {}

        # Restore nodes
        print("Restoring nodes...")
        for node in backup_data["nodes"]:
            labels = ":".join(node["labels"])
            props = node["properties"]

            # Create node
            result = await memory._run_query(f"""
                CREATE (n:{labels})
                SET n = $props
                RETURN id(n) as new_id
            """, {"props": props})

            if result:
                id_mapping[node["neo_id"]] = result[0]["new_id"]

        # Restore relationships
        print("Restoring relationships...")
        for rel in backup_data["relationships"]:
            source_new_id = id_mapping.get(rel["source_id"])
            target_new_id = id_mapping.get(rel["target_id"])

            if source_new_id and target_new_id:
                await memory._run_query(f"""
                    MATCH (a), (b)
                    WHERE id(a) = $source_id AND id(b) = $target_id
                    CREATE (a)-[r:{rel['type']}]->(b)
                    SET r = $props
                """, {
                    "source_id": source_new_id,
                    "target_id": target_new_id,
                    "props": rel["properties"]
                })

        print(f"Restore complete!")
        print(f"  Nodes restored: {len(id_mapping)}")

    finally:
        await memory.close()


async def list_backups():
    """List all available backups."""

    if not BACKUP_DIR.exists():
        print("No backups found.")
        return

    backups = sorted(BACKUP_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

    if not backups:
        print("No backups found.")
        return

    print("Available backups:")
    print("-" * 60)

    for backup_path in backups:
        try:
            with open(backup_path) as f:
                data = json.load(f)

            created = data.get("created_at", "unknown")
            nodes = data.get("node_count", "?")
            rels = data.get("relationship_count", "?")

            print(f"  {backup_path.stem}")
            print(f"    Created: {created}")
            print(f"    Nodes: {nodes}, Relationships: {rels}")
            print()
        except Exception as e:
            print(f"  {backup_path.stem} (error reading: {e})")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "backup":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        asyncio.run(create_backup(name))

    elif command == "restore":
        if len(sys.argv) < 3:
            print("Usage: python backup_restore.py restore <backup_name>")
            return
        name = sys.argv[2]
        asyncio.run(restore_backup(name))

    elif command == "list":
        asyncio.run(list_backups())

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
