#!/usr/bin/env python3
"""
Deploy SearXNG to HuggingFace Spaces

Usage:
    python deploy_searxng.py
"""

import shutil
from pathlib import Path
from huggingface_hub import HfApi, create_repo, upload_folder

SPACE_NAME = "byrd-search"
SPACE_SDK = "docker"

def main():
    api = HfApi()
    username = api.whoami()["name"]
    repo_id = f"{username}/{SPACE_NAME}"

    print(f"🔍 Deploying SearXNG to: {repo_id}")

    # Create the Space
    try:
        create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk=SPACE_SDK,
            private=False,
            exist_ok=True
        )
        print(f"✅ Space ready: https://huggingface.co/spaces/{repo_id}")
    except Exception as e:
        print(f"⚠️  {e}")

    # Prepare deployment
    src = Path(__file__).parent / "searxng-space"
    deploy_dir = Path("/tmp/searxng-deploy")

    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)

    shutil.copytree(src, deploy_dir)

    print(f"📦 Uploading {len(list(deploy_dir.iterdir()))} files...")

    # Upload
    upload_folder(
        folder_path=str(deploy_dir),
        repo_id=repo_id,
        repo_type="space",
    )

    searxng_url = f"https://{username}-byrd-search.hf.space"

    print(f"""
✅ SearXNG deployed!

🔍 Search URL: {searxng_url}
📡 API endpoint: {searxng_url}/search?q=QUERY&format=json

Update BYRD config.yaml:
  seeker:
    research:
      searxng_url: "{searxng_url}"
""")

    shutil.rmtree(deploy_dir)

if __name__ == "__main__":
    main()
