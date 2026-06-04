import base64, os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
full_path = lambda path: os.path.join(os.path.dirname(__file__), path)

client = OpenAI()
prompt = "노을 지는 해변, 잔잔한 파도, 수채화 스타일"

result = client.images.generate(
    model="gpt-image-1.5",
    prompt=prompt,
    size="1024x1024",
    quality="medium"
)

b64 = result.data[0].b64_json
with open(full_path("output.png"), "wb") as f:
    f.write(base64.b64decode(b64))

print("저장 완료")