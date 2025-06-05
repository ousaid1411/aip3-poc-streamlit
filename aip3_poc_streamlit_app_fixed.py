from openai import OpenAI
import os

# Use secret or environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You're a procurement officer drafting a tender spec."},
        {"role": "user", "content": "Draft functional requirements for a CRM system"}
    ]
)

draft = response.choices[0].message.content
