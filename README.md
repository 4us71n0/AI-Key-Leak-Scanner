# AI Key Leak Scanner

This tool scans GitHub repositories for sensitive AI keys (API keys, secrets, etc.) in commit messages and diffs. It's designed to work as both a standalone Python script and as a Docker container.

---

### 🧑‍💻 Supported AI Models

The tool scans for API keys related to the following AI models and services:

1. OpenAI User Key
2. OpenAI Project Key
3. Anthropic Key
4. Google AI Key
5. Mistral AI Key
6. Cohere Key
7. Stability Key
8. Replicate Key
9. Hugging Face Key
10. ElevenLabs Key
11. Together AI Key
12. Groq Key
13. AI21 Key
14. Baseten Key
15. Pinecone Key
16. Modal Key
17. RunPod Key
18. Banana Key

---

### 🚀 Usage

You can use this tool in two ways:

1. **Using Docker**
2. **Running Python script directly**

---

## 🐳 Using with Docker

### Prerequisites

- Docker installed on your machine.
- GitHub personal access token for authentication.
  - You can generate a GitHub token [here](https://github.com/settings/tokens).

### Running the Docker Container

1. **Run the Docker image**  
   Use the following command to scan a GitHub user's or organization's repositories:
   
   - Replace `GITHUB_TOKEN` with your actual GitHub token.
   - Replace `your_username_or_org` with the GitHub username or organization name you want to scan.
   
   
   ```
   docker run -e GITHUB_TOKEN=ghp_your_actual_token 4us71n0/ai-key-scanner --user your_username_or_org --verbose --output json
   ```

   If you want to scan all repositories of an organization instead of a user, use --org:
   
   ```
   docker run -e GITHUB_TOKEN=ghp_your_actual_token 4us71n0/ai-key-scanner --org your_org_name --verbose --output text
   ```

   --verbose: Enable detailed output logs for debugging.

   --output: Choose either json (for structured output) or text (for human-readable output).

   --fast: Skip scanning commit diffs, only scan commit messages.

Example output:

```
[
  {
    "repo": "repo-name",
    "leaks": [
      "[⚠️] OpenAI User Key in commit message: https://github.com/username/repo-name/commit/1234567890abcdef1234567890abcdef12345678\n    ➤ Key found in message"
    ]
  }
]
```
## 🐍 Running the Python Script Directly

### Prerequisites

1. **Install Python**
   
     You will need Python 3.x installed on your machine.

2. **Install dependencies**
   
     Install the required Python libraries:
   
```
pip install -r requirements.txt
```

3. **Set up the GitHub Token**
   
     You will need a GitHub personal access token to authenticate requests to the GitHub API.
   
     Set the GITHUB_TOKEN as an environment variable before running the script:
   
```
export GITHUB_TOKEN=ghp_your_actual_token
```

### Running the Script

1. **Scan a GitHub user**
   
     Use the following command to scan a specific user:
```
python scanner.py --user your_username --verbose --output json
```
2. **Scan a GitHub organization**
   
     If you want to scan an organization, use the --org flag:
```
python scanner.py --org your_org_name --verbose --output text
```
### Command-line Options
--org: Scan a GitHub organization.

--user: Scan a specific GitHub user.

--verbose: Enable detailed output logging.

--output: Choose either json or text output format.

--fast: Skip scanning commit diffs, only scan commit messages.

### Example usage:

```
python scanner.py --user your_username --output json --verbose
```

## 💡 Notes
Rate Limiting: GitHub API requests are rate-limited. If you hit the rate limit, you'll need to wait before making more requests. This can be mitigated by using a GitHub Personal Access Token (PAT).

Scanning Commits: This tool scans both commit messages and diffs for potential secret keys, such as API keys from popular services (OpenAI, Google, etc.).
Privacy: Ensure that you are authorized to scan the repositories, as this tool will expose sensitive information if found.
