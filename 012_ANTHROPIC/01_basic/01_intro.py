import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

message = client.messages.create(
    # haiku(빠름), sonnet, opus(최신, 고성능)
    model="claude-haiku-4-5",
    max_tokens=300,
    messages=[{
        "role": "user", "content": "안녕! 한 눈장으로 너를 소개해"
    }]
)

print(message.content[0].text)