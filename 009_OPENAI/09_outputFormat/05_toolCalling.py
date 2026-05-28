import os, json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_weather(city):
    weather = {"서울": "맑음, 22도", "부산": "흐림, 25도", "LA": "맑음, 27도"}
    return weather.get(city, "해당 도시의 정보는 없습니다.")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "특정 도시의 현재 날씨를 조회한다",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "도시 이름"}
                },
                "required": ["city"]
            }
        }
    }
]

prompt = "서울의 날씨를 알려주시오."

response = client.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "질문에 대해 JSON으로만 답변하시오"},
        {"role": "user", "content": prompt}
    ],
    tools=tools
)

message = response.choices[0].message
print("message")
print(message)
if message.tool_calls:
    call = message.tool_calls[0]
    print("모델이 호출하려는 함수:", call.function.name)
    print("모델이 추가하려는 인자:", json.loads(call.function.arguments))

prompt += f"\n\n참고 자료: {message}"

# final_reply = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "질문에 대해 친절하게 답변하시오"},
#         {"role": "user", "content": prompt}
#     ]
# )

print("최종 메시지:", message.content)