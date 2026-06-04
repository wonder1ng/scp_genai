import base64, os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
full_path = lambda path: os.path.join(os.path.dirname(__file__), path)
image_url = full_path("juga.png")

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf_8")

def ask_about_image(question, b64):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    # {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                    # {"type": "image_url", "image_url": {"url": f"data:image/webp;base64,{b64}"}}
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
                ]
            }
        ]
    )
    print(response)
    print("response.choices[0].message.content")
    print(response.choices[0].message.content)

    return response.choices[0].message.content

questions = [
    "이 이미지에 있는 한글 글자를 다 읽어 해설 빼고 OCR로 글자만 읽어",
    "해당 이미지 주요 색상",
    "이미지의 전체 분위기 한 문장으로 표현",
    "이 주식 차트를 보고 어떤 종목인지 알려주고 기술적 분석해",
    "이 주식 차트를 보고 어떤 종목인지 알려주고 매수 또는 매도 타이밍을 분석하고 왜 그런지 기술적으로 설명해",
]

b64 = encode_image(image_url)
for q in questions:
    print("=" * 20)
    print("질문:", q)
    print("답변:", ask_about_image(q, b64))