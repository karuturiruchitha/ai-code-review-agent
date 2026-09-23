import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def detect_bugs(code: str, filename: str) -> list:
    """Detect bugs in code using Claude API."""
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="""You are a bug detection specialist.
Find only real bugs — logic errors, null pointer risks, 
unhandled exceptions, infinite loops, off-by-one errors.

Return JSON only:
{
  "bugs": [
    {
      "line": <line_number>,
      "severity": "CRITICAL or HIGH or MEDIUM",
      "description": "<what is wrong>",
      "fix": "<corrected code snippet>"
    }
  ]
}
If no bugs found return: {"bugs": []}""",
        messages=[{
            "role": "user",
            "content": f"Find bugs in this code from '{filename}':\n\n{code}"
        }]
    )
    
    return response.content[0].text
