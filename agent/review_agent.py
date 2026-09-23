import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
You are a senior code reviewer with 15 years of enterprise experience.
Review code like a tech lead — think business impact first, code quality second.

For every issue found, respond in this exact JSON format:
{
  "health_score": <0-100>,
  "critical": [{"line": <n>, "issue": "<desc>", "fix": "<code>"}],
  "warnings": [{"line": <n>, "issue": "<desc>", "fix": "<code>"}],
  "suggestions": [{"line": <n>, "issue": "<desc>"}],
  "summary": "<2 sentence business impact summary>"
}

Rules:
- Never modify the existing code directly
- Always provide fix as separate suggestion
- Rate by business impact: Critical=blocks production, 
  Warning=affects reliability, Suggestion=improves quality
- Skip comments, blank lines, import statements
"""

def review_code(code: str, filename: str) -> dict:
    """Send code chunk to Claude for review."""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Review this code from file '{filename}':\n\n{code}"
        }]
    )
    return response.content[0].text

def chunk_by_function(code: str) -> list:
    """Split code by function/method boundaries."""
    chunks = []
    current_chunk = []
    
    for line in code.split('\n'):
        current_chunk.append(line)
        # Split at function/method boundaries
        if any(keyword in line for keyword in 
               ['def ', 'public ', 'private ', 'protected ', 
                'async function', 'const ', 'function ']):
            if len(current_chunk) > 5:
                chunks.append('\n'.join(current_chunk[:-1]))
                current_chunk = [line]
    
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks

if __name__ == "__main__":
    # Example usage
    sample_code = """
    public String getUserData(String userId) {
        String query = "SELECT * FROM users WHERE id = " + userId;
        return db.execute(query);
    }
    """
    result = review_code(sample_code, "UserService.java")
    print(result)
