# mamba uninstall -y openai; mamba install -y openai
import base64, openai, os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as f:
        base64_bytes = base64.b64encode(f.read()).decode("utf_8")
        return f"data:image/jpeg;base64,{base64_bytes}"

def ask_chatbot(image_path, user_input, role = "당신은 스포츠 트레이너입니다."):
    image_base64 = encode_image_to_base64(image_path)
        
    final_message=[
        {"role": "system", "content": role},
        {"role": "user", "content": [
            {
                "type": "text",
                "text": user_input
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_base64
                }
            }
        ]}
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=final_message
    )
    
    final_response = response.choices[0].message.content
    return final_response

base_path = "\\".join(__file__.split("\\")[:-1]) + "\\images"
# image_path = base_path + "\\img01.jpg"
# q = "여기에 몇 마리의 동물이 있나요?"
# print(ask_chatbot(image_path, q))

image_path = base_path + "\\squats-good.jpg"
q = "나의 스쿼트 자세가 어떤지 전문가 입장으로 10점 만점으로 평가 후 해설, 담변은 한국어로"
print(ask_chatbot(image_path, q))
print("=" * 60)
image_path = base_path + "\\squats-bad.jpg"
q = "나의 스쿼트 자세가 어떤지 전문가 입장으로 10점 만점으로 평가 후 해설, 담변은 한국어로. 평가 불가할 경우 이유 상세 설명"
print(ask_chatbot(image_path, q))