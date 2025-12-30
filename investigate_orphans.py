#!/usr/bin/env python3
"""Quick investigation of orphan content and similarity matching."""

import asyncio
from dotenv import load_dotenv
load_dotenv()

import yaml
import os
import re
from pathlib import Path

def expand_env_vars(config_str):
    def expand(match):
        var_expr = match.group(1)
        if ':-' in var_expr:
            var_name, default = var_expr.split(':-', 1)
        else:
            var_name, default = var_expr, ''
        return os.environ.get(var_name, default)
    return re.sub(r'\$\{([^}]+)\}', expand, config_str)

async def investigate():
    config_str = Path('config.yaml').read_text()
    config = yaml.safe_load(expand_env_vars(config_str))
    memory_config = config.get('memory', {})

    from memory import Memory
    memory = Memory(memory_config)
    await memory.connect()

    # Get orphaned experiences
    orphans = await memory.get_orphaned_experiences(limit=10)
    print('=== ORPHANED EXPERIENCES ===')
    for o in orphans[:5]:
        print(f"\nID: {o.get('id', 'n/a')[:20]}")
        print(f"Type: {o.get('type', 'unknown')}")
        print(f"Content: {o.get('content', '')[:200]}...")

    # Get sample beliefs
    beliefs = await memory.get_beliefs(limit=100)
    print(f'\n=== BELIEFS ({len(beliefs)} total) ===')
    for b in beliefs[:3]:
        print(f"\nID: {b.get('id', 'n/a')[:20]}")
        print(f"Confidence: {b.get('confidence', 0)}")
        print(f"Content: {b.get('content', '')[:200]}...")

    # Try similarity matching manually
    print('\n=== TESTING SIMILARITY ===')
    threshold = memory.CONNECTION_HEURISTIC_CONFIG["similarity_threshold"]
    print(f'Threshold: {threshold}')

    if orphans and beliefs:
        for orphan in orphans[:3]:
            orphan_content = orphan.get('content', '')
            print(f"\n--- Orphan: {orphan.get('type', '?')} ---")
            print(f"Content: {orphan_content[:100]}...")

            # Find best matching beliefs
            matches = []
            for b in beliefs:
                sim = memory._compute_text_similarity(orphan_content, b.get('content', ''))
                if sim > 0:
                    matches.append((sim, b.get('content', '')[:60]))

            matches.sort(reverse=True)
            print(f"Top 3 matches (need >= {threshold}):")
            for sim, content in matches[:3]:
                status = "✅" if sim >= threshold else "❌"
                print(f"  {status} {sim:.4f} - {content}...")

    await memory.close()

if __name__ == "__main__":
    asyncio.run(investigate())
