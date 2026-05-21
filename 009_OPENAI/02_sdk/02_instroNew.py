# mamba uninstall -y openai; mamba install -y openai
import openai, os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

role = "Your are a helpful assistant."

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "당신은 내 질문에 답변 잘하는 챗봇"},
        {"role": "user", "content": "안녕"}
    ]
)

final_response = response.choices[0].message.content
print(final_response)