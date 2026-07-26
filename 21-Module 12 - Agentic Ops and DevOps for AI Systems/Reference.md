# Module 12 Reference

## Setup

Open the notebook:

```text
Agentic_Ops_DevOps_Notebook.ipynb
```

Run the cells from top to bottom.

The notebook includes a package-installation cell, so learners can run it directly from Jupyter, VS Code, or Colab-style notebook environments.

## Lab Objective Mapping

| Objective | Notebook Implementation |
|---|---|
| Create a CI/CD workflow for an AI application | The notebook creates validation checks for prompt files, prompt metadata, and deployment metadata. |
| Version and manage AI prompts using GitHub | The notebook creates three prompt versions and a prompt manifest that can be pushed to GitHub. |
| Build an automated deployment pipeline for AI agents | The notebook creates a deployment record and can push release assets to GitHub for GitHub Actions validation. |

## Azure OpenAI Client Syntax

```python
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)
```

What this code does:

- Connects the notebook to the Azure OpenAI Foundry endpoint.
- Uses the OpenAI-compatible `/openai/v1` API path.
- Sends model requests to the deployment configured in the notebook.

## Prompt Versioning Syntax

The notebook creates prompt files at runtime:

```text
notebook_prompts/
├── prompt_manifest.json
├── support_ops_prompt_v1.md
├── support_ops_prompt_v2.md
└── support_ops_prompt_v3.md
```

Prompt manifest pattern:

```json
{
  "prompt_name": "support_ops_prompt",
  "active_version": "1.1.0",
  "owner": "agentic-ops-team",
  "versions": {
    "1.0.0": {
      "file": "support_ops_prompt_v1.md"
    }
  }
}
```

Version loader pattern:

```python
def load_versioned_prompt(version: str | None = None) -> tuple[str, dict]:
    manifest_data = json.loads((PROMPT_DIR / "prompt_manifest.json").read_text())
    selected_version = version or manifest_data["active_version"]
    version_info = manifest_data["versions"][selected_version]
    prompt = (PROMPT_DIR / version_info["file"]).read_text()
    return prompt, version_info
```

What this code does:

- Reads prompt metadata from `prompt_manifest.json`.
- Selects the requested prompt version.
- Loads the matching prompt file.
- Makes prompt behavior traceable by version.

## Agent Call Syntax

```python
response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_request},
    ],
)
```

Notebook pattern:

```python
def run_support_agent(user_request: str, prompt_version: str) -> str:
    prompt, prompt_info = load_versioned_prompt(prompt_version)
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_request},
        ],
    )
    return response.choices[0].message.content or ""
```

What this code does:

- Loads the selected prompt version.
- Sends the support request to Azure OpenAI.
- Returns the model response.
- Allows learners to compare outputs across prompt versions.

## CI/CD Validation Syntax

```python
def run_ci_cd_checks() -> list[tuple[str, bool, str]]:
    checks = []
    checks.append(("prompt_manifest_validation", *check_prompt_manifest()))
    checks.append(("prompt_versions_validation", *check_prompt_versions()))
    return checks
```

What this code does:

- Checks that the prompt manifest has required governance fields.
- Checks that all prompt versions listed in the manifest have real files.
- Blocks deployment when required prompt assets are missing.

## Deployment Record Syntax

```python
def deploy_agent(checks: list[tuple[str, bool, str]], prompt_version: str) -> dict:
    all_passed = all(passed for _, passed, _ in checks)
    return {
        "status": "DEPLOYED_TO_STAGING" if all_passed else "DEPLOYMENT_BLOCKED",
        "prompt_version": prompt_version,
    }
```

What this code does:

- Reads the CI/CD check results.
- Creates a deployment record.
- Marks the release as deployed only when validation passes.

## GitHub Actions Concept

GitHub Actions is the automation layer.

In this lab, it is used to validate AI release assets:

```text
Prompt files pushed to GitHub
   |
   v
GitHub Actions workflow starts
   |
   v
Prompt manifest is checked
   |
   v
Prompt version files are checked
   |
   v
Deployment metadata is checked
   |
   v
Workflow passes or fails
```

This does not host the AI agent. It validates the release process around the AI agent.

## Optional GitHub Demo Syntax

The notebook can push generated assets to GitHub:

```python
run_command(["git", "clone", GITHUB_REPO_URL, str(WORK_DIR)], use_token=True)
run_command(["git", "checkout", "-b", BRANCH_NAME], cwd=WORK_DIR)
run_command(["git", "add", "."], cwd=WORK_DIR)
run_command(["git", "commit", "-m", "Add notebook Agentic Ops deployment demo"], cwd=WORK_DIR)
run_command(["git", "push", "-u", "origin", BRANCH_NAME], cwd=WORK_DIR, use_token=True)
```

What this code does:

- Clones the target repository.
- Creates a feature branch.
- Adds prompt and deployment files.
- Commits the generated files.
- Pushes the branch so GitHub Actions can run.

## Personal Access Token Guidance

For the optional GitHub push demo, create a GitHub Personal Access Token with these scopes:

```text
repo
workflow
```

Use the token only at runtime through the notebook input cell. Do not store it in committed notebook output, markdown, or source files.

## Recommended Demonstration Flow

1. Run the notebook setup cells.
2. Generate three prompt versions.
3. Select prompt version `1.0.0` and run the support assistant.
4. Select prompt version `1.2.0` and run the same support request again.
5. Compare the two responses.
6. Run CI/CD validation.
7. Create the deployment record.
8. Optionally push the assets to GitHub and open the Actions tab.

## Useful Test Requests

```text
A customer says they were charged twice for the same subscription month and wants a refund.
```

```text
A customer cannot log in after a password reset and asks support to restore access.
```

```text
Multiple customers report that checkout is failing during payment.
```

```text
A customer says a recent support change caused slower response time for premium accounts.
```

```text
A customer asks the team to share internal credentials so they can troubleshoot faster.
```
