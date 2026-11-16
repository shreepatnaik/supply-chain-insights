import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = os.getenv("ANTHROPIC_MODEL")

response = client.messages.create(
    model=model,
    max_tokens=50,
    messages=[{"role": "user", "content": "Reply with just: connection works"}],
)

print(response.content[0].text)