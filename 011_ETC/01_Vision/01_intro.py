from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

image_url = r"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Kunmadaras_Motorsport_2021._szeptember_19._JM_%28153%29.jpg/1280px-Kunmadaras_Motorsport_2021._szeptember_19._JM_%28153%29.jpg"

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "이 이미지를 한국어로 설명해"},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        }
    ]
)

print(response)
print("response.choices[0].message.content")
print(response.choices[0].message.content)