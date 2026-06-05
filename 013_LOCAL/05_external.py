import requests

OLLAMA_HOST = " http://localhost:11434"
OLLAMA_ENDPOINT = f"{OLLAMA_HOST}/api/generate"

payload = {
    "model": "exaone3.5",
    "prompt": "파이썬으로 구현하는 헬로우 월드 코드를 보여줘",
    # "system": False
}

response = requests.post(OLLAMA_ENDPOINT, json=payload)
data = response.json()

print("모델 응답:", data.get("response"))