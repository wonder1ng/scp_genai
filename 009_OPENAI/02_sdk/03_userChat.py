# mamba uninstall -y openai; mamba install -y openai
import openai, os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

role = "Your are a helpful assistant."

def ask_chatbot(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": user_input}
        ]
    )

    final_response = response.choices[0].message.content
    return final_response

while True:
    user_input = input("\n질문: ").strip()
    chatbot_response = ask_chatbot(user_input)
    print("챗봇 응답:", chatbot_response)