# AI Code Review Agent — Architecture

## Overview

```
Developer raises Pull Request
           ↓
Azure DevOps Pipeline triggers (PR only — not every commit)
           ↓
Agent fetches changed files via git diff
(only .java, .js, .jsx, .py, .ts files)
           ↓
Files chunked by function/method boundaries
(not by line count — avoids cutting mid-function)
           ↓
4 specialized tools run on each chunk:
  ├── Bug Detector      → logic errors, null risks
  ├── Security Scanner  → SQL injection, secrets, auth
  ├── Debt Analyzer     → duplication, naming, complexity
  └── Fix Suggester     → corrected code for each issue
           ↓
Results merged and deduplicated
           ↓
Code Health Score calculated (0–100)
           ↓
PR comment posted on Azure DevOps automatically
           ↓
If Critical bugs → pipeline FAILS, merge blocked
           ↓
Results saved to MySQL database
           ↓
React dashboard shows health trend over time
```

## Cost Optimization Strategy

| Strategy | Token Reduction |
|---|---|
| PR-only trigger (not every commit) | ~85% |
| Diff-based review (changed lines only) | ~70% |
| Skip non-logic files (json, yml, css) | ~15% |
| Chunk by function (not whole file) | ~40% |
| Daily token budget cap | Safety net |

## Database Schema

```sql
CREATE TABLE code_reviews (
  id INT AUTO_INCREMENT PRIMARY KEY,
  pr_id VARCHAR(100),
  repository VARCHAR(200),
  reviewer_run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  health_score INT,
  critical_count INT,
  warning_count INT,
  suggestion_count INT,
  files_reviewed INT,
  tokens_used INT
);

CREATE TABLE review_issues (
  id INT AUTO_INCREMENT PRIMARY KEY,
  review_id INT,
  filename VARCHAR(300),
  line_number INT,
  issue_type ENUM('CRITICAL','WARNING','SUGGESTION'),
  category ENUM('BUG','SECURITY','DEBT'),
  description TEXT,
  suggested_fix TEXT,
  FOREIGN KEY (review_id) REFERENCES code_reviews(id)
);
```

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| AI | Claude API (Anthropic) | Best code understanding |
| Agent | LangChain + ReAct | Multi-step reasoning |
| Pipeline | Azure DevOps | Real enterprise CI/CD |
| Backend | Python + FastAPI | Fast, lightweight |
| Database | MySQL | Store review history |
| Frontend | React + Chart.js | Health trend dashboard |
