import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def suggest_fix(code: str, issue_description: str) -> str:
    """Generate a corrected code suggestion for a given issue."""
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="""You are a code fix specialist.
Given a piece of code and an issue description, provide the corrected version.

Rules:
- Return ONLY the fixed code snippet, nothing else
- Keep the same language and style as the original
- Fix only the specific issue described
- Do not refactor or rewrite unrelated parts
- Add a brief comment explaining what you changed""",
        messages=[{
            "role": "user",
            "content": f"Issue: {issue_description}\n\nOriginal code:\n{code}\n\nProvide the fixed version:"
        }]
    )
    
    return response.content[0].text
