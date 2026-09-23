import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SECURITY_RULES = [
    "SQL injection — user input in queries without parameterization",
    "Hardcoded secrets — API keys, passwords, tokens in code",
    "Insecure API calls — HTTP instead of HTTPS",
    "Missing input validation — unvalidated user input",
    "Exposed sensitive data — PII or credentials in logs",
    "Weak encryption — MD5, SHA1 usage",
    "Missing authentication checks on endpoints"
]

def scan_security(code: str, filename: str) -> list:
    """Scan code for security vulnerabilities."""
    
    rules_text = "\n".join(f"- {r}" for r in SECURITY_RULES)
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=f"""You are a security code reviewer.
Check only for these vulnerability types:
{rules_text}

Return JSON only:
{{
  "vulnerabilities": [
    {{
      "line": <line_number>,
      "type": "<vulnerability type>",
      "severity": "CRITICAL or HIGH or MEDIUM",
      "description": "<what the risk is>",
      "fix": "<how to fix it>"
    }}
  ]
}}
If no vulnerabilities found return: {{"vulnerabilities": []}}""",
        messages=[{
            "role": "user",
            "content": f"Scan this code from '{filename}' for security issues:\n\n{code}"
        }]
    )
    
    return response.content[0].text
