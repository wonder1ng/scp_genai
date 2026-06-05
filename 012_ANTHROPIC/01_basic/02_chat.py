import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

messages = []

def ask(question):
    messages.append({"role": "user", "content": question})
    message = client.messages.create(
        # haiku(빠름), sonnet, opus(최신, 고성능)
        model="claude-haiku-4-5",
        max_tokens=300,
        messages=messages
    )
    answer = message.content[0].text
    messages.append({"role": "assistant", "content": answer})
    return answer

print("[챗봇]", ask("내 이름은 홍길동이야")) 
print("[챗봇]", ask("내가 누구라고?")) 