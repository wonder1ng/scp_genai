# mamba install -y openai==0.28
import openai, os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "당신은 내 질문에 답변 잘하는 챗봇"},
        {"role": "user", "content": "안녕"}
    ]
)

final_response = response.choices[0].message.content
print(final_response)