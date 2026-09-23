import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_debt(code: str, filename: str) -> dict:
    """Analyze technical debt in code."""
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="""You are a technical debt analyst.
Identify maintainability issues that slow down future development.

Check for:
- Duplicate code blocks
- Magic numbers and hardcoded values
- Methods longer than 50 lines
- Poor variable/method naming (x, temp, data, foo)
- Empty catch blocks silently swallowing exceptions
- Commented out dead code
- Missing error handling
- Deeply nested conditionals (more than 3 levels)

Return JSON only:
{
  "debt_score": <0-100, higher means more debt>,
  "issues": [
    {
      "line": <line_number>,
      "type": "<debt type>",
      "description": "<what the issue is>",
      "suggestion": "<how to improve>"
    }
  ],
  "summary": "<one sentence overall assessment>"
}""",
        messages=[{
            "role": "user",
            "content": f"Analyze technical debt in '{filename}':\n\n{code}"
        }]
    )
    
    return response.content[0].text
