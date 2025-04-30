# AI Key Leak Scanner

This tool scans GitHub repositories for sensitive AI keys (API keys, secrets, etc.) in commit messages and diffs. It's designed to work as both a standalone Python script and as a Docker container.

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
   
   ```bash
   docker run -e GITHUB_TOKEN=ghp_your_actual_token 4us71n0/ai-key-scanner --user your_username_or_org --verbose --output json

