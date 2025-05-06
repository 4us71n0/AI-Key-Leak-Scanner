import os
import re
import requests
import argparse
import json
import time

# GitHub Token from Environment Variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("❌ Error: GITHUB_TOKEN environment variable not set.")
    exit(1)

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

API_KEY_RULES = [
    ("OpenAI User Key", r"sk-[a-zA-Z0-9]{48}"),
    ("OpenAI Project Key", r"sk-proj-[a-zA-Z0-9]{22,}"),
    ("Anthropic Key", r"prod_[a-z0-9]{32,}"),
    ("Google AI Key", r"AIza[0-9A-Za-z\-_]{35}"),
    ("Mistral AI Key", r"mistral_[a-zA-Z0-9]{32,}"),
    ("Cohere Key", r"CCH-[a-zA-Z0-9_-]{32,}"),
    ("Stability Key", r"sk-[a-z0-9]{40,}"),
    ("Replicate Key", r"r8_[a-zA-Z0-9]{32,}"),
    ("Hugging Face Key", r"hf_[a-zA-Z0-9]{32,}"),
    ("ElevenLabs Key", r"elevenlabs-[a-z0-9]{32,}"),
    ("Together AI Key", r"together-[a-zA-Z0-9]{32,}"),
    ("Groq Key", r"gsk_[a-zA-Z0-9]{32,}"),
    ("AI21 Key", r"ai21-[a-zA-Z0-9]{32,}"),
    ("Baseten Key", r"btv_[a-zA-Z0-9]{32,}"),
    ("Pinecone Key", r"pnc_[a-zA-Z0-9]{32,}"),
    ("Modal Key", r"mod_[a-zA-Z0-9]{32,}"),
    ("RunPod Key", r"runpod-[a-zA-Z0-9]{32,}"),
    ("Banana Key", r"ban_[a-zA-Z0-9]{32,}")
]

def get_repos(org_or_user, max_repos=100):
    url = f"https://api.github.com/users/{org_or_user}/repos?per_page={max_repos}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"[!] Failed to fetch repos for {org_or_user}: {response.text}")
        return []
    return response.json()

def get_branches(owner, repo_name):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/branches"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"[!] Failed to fetch branches for {repo_name}: {response.text}")
        return []
    return [branch["name"] for branch in response.json()]

def get_commits(owner, repo_name, branch='main', per_page=100):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/commits?sha={branch}&per_page={per_page}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"[!] Failed to fetch commits for {repo_name} on branch {branch}: {response.text}")
        return []
    return response.json()

def scan_commits_for_secrets(commits, repo_name, owner, fast_mode=False, verbose=False):
    leaks = []
    for commit in commits:
        sha = commit.get('sha', '')
        message = commit.get('commit', {}).get('message', '')
        commit_url = f"https://github.com/{owner}/{repo_name}/commit/{sha}"

        for name, pattern in API_KEY_RULES:
            if re.search(pattern, message):
                log = f"[⚠️] {name} in commit message: {commit_url}\n    ➤ {message.strip()[:100]}"
                leaks.append(log)
                if verbose:
                    print(log)

        if fast_mode:
            continue

        diff_url = commit.get('url')
        if diff_url:
            diff_response = requests.get(diff_url, headers=HEADERS)
            if diff_response.status_code == 200:
                diff_text = diff_response.text
                for name, pattern in API_KEY_RULES:
                    if re.search(pattern, diff_text):
                        log = f"[⚠️] {name} in commit diff: {commit_url}"
                        leaks.append(log)
                        if verbose:
                            print(log)
                time.sleep(0.5)
    return leaks

def main():
    parser = argparse.ArgumentParser(description="AI Key Leak Scanner for GitHub Repos (All Branches, No Cloning)")
    parser.add_argument("--org", type=str, help="GitHub organization name to scan")
    parser.add_argument("--user", type=str, help="GitHub user name to scan")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--fast", action="store_true", help="Fast mode (skip diffs, only scan commit messages)")

    args = parser.parse_args()
    target = args.org if args.org else args.user

    if not target:
        print("❌ Error: Either --org or --user must be specified.")
        return

    repos = get_repos(target)
    print(f"\n📦 Found {len(repos)} repos in {target}")

    results = []
    for repo in repos:
        name = repo["name"]
        print(f"\n🔍 Scanning repo: {name}")
        branches = get_branches(target, name)
        for branch in branches:
            print(f"  🌿 Branch: {branch}")
            commits = get_commits(target, name, branch)
            leaks = scan_commits_for_secrets(commits, name, target, fast_mode=args.fast, verbose=args.verbose)
            if leaks:
                results.append({"repo": name, "branch": branch, "leaks": leaks})

    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            print(f"\n📁 Repo: {result['repo']} | Branch: {result['branch']}")
            for leak in result["leaks"]:
                print(leak)

if __name__ == "__main__":
    main()
