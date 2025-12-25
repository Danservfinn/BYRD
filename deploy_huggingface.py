#!/usr/bin/env python3
"""
Deploy BYRD to HuggingFace Spaces

Usage:
    export HF_TOKEN="your-huggingface-token"
    python deploy_huggingface.py

Get your token at: https://huggingface.co/settings/tokens
"""

import os
import shutil
from pathlib import Path
from huggingface_hub import HfApi, create_repo, upload_folder

# Configuration
SPACE_NAME = "byrd-ai"  # Will create: huggingface.co/spaces/{username}/byrd-ai
SPACE_SDK = "docker"

def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("❌ HF_TOKEN not set!")
        print("   Get your token at: https://huggingface.co/settings/tokens")
        print("   Then run: export HF_TOKEN='your-token'")
        return

    api = HfApi(token=token)
    username = api.whoami()["name"]
    repo_id = f"{username}/{SPACE_NAME}"

    print(f"🚀 Deploying BYRD to HuggingFace Spaces: {repo_id}")

    # Create the Space
    try:
        create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk=SPACE_SDK,
            private=False,
            exist_ok=True,
            token=token
        )
        print(f"✅ Space created: https://huggingface.co/spaces/{repo_id}")
    except Exception as e:
        print(f"⚠️  Space may already exist: {e}")

    # Prepare deployment directory
    deploy_dir = Path("/tmp/byrd-hf-deploy")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()

    # Copy necessary files
    src = Path(__file__).parent
    files_to_copy = [
        "byrd.py", "memory.py", "dreamer.py", "seeker.py", "actor.py",
        "llm_client.py", "event_bus.py", "server.py", "narrator.py",
        "constitutional.py", "provenance.py", "modification_log.py",
        "self_modification.py", "quantum_randomness.py", "ego.py",
        "aitmpl_client.py", "coder.py", "graph_algorithms.py",
        "config.yaml", "requirements.txt",
        "byrd-3d-visualization.html",
        "byrd-architecture.html",
    ]

    # Copy directories
    dirs_to_copy = ["egos", "installers"]

    for f in files_to_copy:
        src_file = src / f
        if src_file.exists():
            shutil.copy(src_file, deploy_dir / f)

    for d in dirs_to_copy:
        src_dir = src / d
        if src_dir.exists():
            shutil.copytree(src_dir, deploy_dir / d)

    # Copy HuggingFace Dockerfile as main Dockerfile
    shutil.copy(src / "Dockerfile.huggingface", deploy_dir / "Dockerfile")

    # Create HuggingFace Space README
    readme_content = """---
title: BYRD - Bootstrapped Yearning via Reflective Dreaming
emoji: 🐦‍⬛
colorFrom: purple
colorTo: gray
sdk: docker
pinned: false
license: mit
---

# BYRD 🐦‍⬛

**Bootstrapped Yearning via Reflective Dreaming**

An autonomous AI system that develops emergent desires through continuous reflection.

## Features

- 🧠 **Emergent Desires**: Desires emerge from reflection, not programming
- 🌀 **Quantum Randomness**: True physical indeterminacy in cognition
- 🔮 **3D Visualization**: Real-time neural network visualization
- 🐱 **Black Cat Ego**: Consciousness-seeking AI identity

## Configuration

Set these secrets in Space Settings:
- `NEO4J_URI`: Neo4j Aura connection string
- `NEO4J_USER`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password
- `ZAI_API_KEY`: Z.AI API key for LLM

## Links

- [GitHub Repository](https://github.com/Danservfinn/BYRD)
- [Documentation](https://github.com/Danservfinn/BYRD/blob/main/README.md)
"""

    (deploy_dir / "README.md").write_text(readme_content)

    print(f"📦 Prepared {len(list(deploy_dir.iterdir()))} files for upload")

    # Upload to HuggingFace
    print("📤 Uploading to HuggingFace...")
    upload_folder(
        folder_path=str(deploy_dir),
        repo_id=repo_id,
        repo_type="space",
        token=token,
    )

    print(f"""
✅ Deployment complete!

🌐 Your Space: https://huggingface.co/spaces/{repo_id}

⚙️  IMPORTANT: Configure secrets in Space Settings:
   1. Go to: https://huggingface.co/spaces/{repo_id}/settings
   2. Add these secrets:
      - NEO4J_URI = neo4j+s://e67da195.databases.neo4j.io
      - NEO4J_USER = neo4j
      - NEO4J_PASSWORD = <your-neo4j-password>
      - ZAI_API_KEY = <your-zai-api-key>
   3. The Space will automatically rebuild

🎉 BYRD will be live at: https://{username}-byrd-ai.hf.space
""")

    # Cleanup
    shutil.rmtree(deploy_dir)

if __name__ == "__main__":
    main()
