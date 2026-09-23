# AI Code Review Agent 🤖

An intelligent multi-step AI agent that automatically reviews code on 
**Azure DevOps Pull Requests** using **Claude API** and **LangChain**.

## What It Does

Every time a developer raises a Pull Request in Azure DevOps, this agent:

1. 🔍 **Detects bugs** — logic errors, null pointer risks, unhandled exceptions
2. 🔒 **Scans security** — SQL injection, hardcoded secrets, insecure API calls
3. 📊 **Analyzes technical debt** — duplicate code, magic numbers, poor naming
4. 💡 **Suggests fixes** — actual corrected code, not just "fix this"
5. 📈 **Scores the code** — Code Health Score (0–100) per Pull Request
6. 💬 **Posts PR comment** — review posted directly on Azure DevOps PR
7. 🚫 **Blocks merge** — if Critical bugs found, pipeline fails automatically
8. 📉 **Tracks history** — all reviews stored in MySQL, trends on dashboard

## Architecture

```
Developer raises PR
        ↓
Azure DevOps Pipeline triggers
        ↓
Agent pulls only changed files (git diff)
        ↓
Smart chunking by function/method boundaries
        ↓
4 specialized Claude API tools run in parallel:
  ├── Bug Detector
  ├── Security Scanner  
  ├── Technical Debt Analyzer
  └── Fix Suggester
        ↓
Results merged → Code Health Score calculated
        ↓
PR comment posted on Azure DevOps
        ↓
Results stored in MySQL
        ↓
React dashboard shows health trends over time
```

## Cost Optimization

- Triggers **only on Pull Requests** — not every commit (90% token reduction)
- Reviews **only changed lines** via git diff — not entire files
- Skips non-logic files: `*.json`, `*.yml`, `*.md`, `*.css`
- Daily token budget cap with queue for overflow
- Smart chunking by function boundaries — no mid-function cuts

## Tech Stack

| Layer | Technology |
|---|---|
| AI Brain | Claude API (Anthropic) — claude-sonnet |
| Agent Framework | LangChain + ReAct |
| Pipeline | Azure DevOps YAML |
| Backend | Python (FastAPI) |
| Database | MySQL |
| Frontend | React.js + Chart.js |

## Setup

```bash
git clone https://github.com/karuturiruchitha/ai-code-review-agent
cd ai-code-review-agent
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY and AZURE_DEVOPS_TOKEN to .env
python agent/review_agent.py
```

## Environment Variables

```env
ANTHROPIC_API_KEY=your_claude_api_key
AZURE_DEVOPS_TOKEN=your_azure_token
AZURE_ORG_URL=https://dev.azure.com/your-org
DB_HOST=localhost
DB_NAME=code_review_db
DB_USER=root
DB_PASSWORD=your_password
```

## Sample PR Comment Output

```
🤖 AI Code Review Agent — Health Score: 72/100

🔴 CRITICAL (1 issue)
└── Line 45: SQL injection risk — user input passed directly to query

🟡 WARNING (2 issues)
├── Line 23: Hardcoded API key detected
└── Line 67: Empty catch block — exception swallowed silently

🟢 SUGGESTION (1 issue)
└── Line 34: Method too long (67 lines) — consider splitting

✅ View full report → dashboard link
```

## Azure DevOps Pipeline

```yaml
trigger: none

pr:
  branches:
    include:
      - main
      - develop

steps:
  - script: pip install -r requirements.txt
  - script: python agent/review_agent.py
    env:
      ANTHROPIC_API_KEY: $(ANTHROPIC_API_KEY)
```

## Status

🚧 **In active development** — core agent and Azure DevOps integration complete.
Dashboard and MySQL history tracking in progress.

## Author

**Ruchitha Karuturi** — Full Stack Developer & AI Integration Specialist  
[LinkedIn](https://linkedin.com/in/ruchitha-karuturi-51a49b24a) | 
[GitHub](https://github.com/karuturiruchitha)
