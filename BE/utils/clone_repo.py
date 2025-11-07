# utils/clone_repo.py
import git
import os
import re
import requests

def clone_repo(repo_url: str, base_dir: str):
    # Basic validation
    if not re.match(r"^https://(github\.com)/.+/.+\.git$", repo_url) and not re.match(r"^https://(github\.com)/.+/.+$", repo_url):
        raise ValueError("Invalid GitHub URL. Must be in format https://github.com/user/repo(.git)")

    # Check if repo is reachable
    response = requests.get(repo_url)
    if response.status_code != 200:
        raise ConnectionError(f"Repository not reachable: {response.status_code}")

    # Extract repo name
    repo_name = repo_url.rstrip("/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    repo_path = os.path.join(base_dir, repo_name)

    print(f"[INFO] Cloning {repo_url} into {repo_path} ...")

    try:
        git.Repo.clone_from(repo_url, repo_path)
        print("[INFO] Clone successful.")
    except Exception as e:
        raise RuntimeError(f"Git clone failed: {e}")

    return repo_name, repo_path
