import os
import sys
import requests

BASE_URL = "https://api.github.com"


def get_default_branch(repo, headers):
    url = f"{BASE_URL}/repos/{repo}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.json().get("message"))
        return None

    return response.json()["default_branch"]


def list_files(repo, branch, headers):
    url = f"{BASE_URL}/repos/{repo}/git/trees/{branch}?recursive=1"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.json().get("message"))
        return

    data = response.json()

    print(f"\nRepository: {repo}")
    print(f"Branch: {branch}")
    print("\nFiles:\n")

    for item in data["tree"]:
        if item["type"] == "blob":
            print(item["path"])


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("python main.py <owner/repository>")
        return

    repo = sys.argv[1]

    token = os.getenv("GITHUB_TOKEN")

    if not token:
        print("GitHub token was not found.")
        print("Create the environment variable GITHUB_TOKEN.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    branch = get_default_branch(repo, headers)

    if branch is None:
        return

    list_files(repo, branch, headers)


if __name__ == "__main__":
    main()