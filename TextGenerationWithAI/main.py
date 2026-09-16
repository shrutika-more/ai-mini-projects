import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_text(prompt, content_type, tone, length):
    instruction = f"""
You are FOX AI, a helpful AI writing assistant.

Create a {content_type.lower()} based on the user's request.

Writing tone: {tone}
Preferred length: {length}

Important instructions:
- Follow the requested content type.
- Keep the writing natural and useful.
- Do not mention that you are an AI.
- Return only the generated content.
- Do not add unnecessary explanations before or after the content.

User request:
{prompt}
"""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": instruction
            }
        ],
        temperature=0.7,
        max_completion_tokens=2048,
        top_p=1
    )

    return completion.choices[0].message.content