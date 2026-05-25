# ollama pull qwen2.5:1.5b
# ollama pull exaone3.5:2.4b
import requests

MODEL_NAME = "qwen2.5:1.5b"
# MODEL_NAME = "exaone3.5:2.4b"
# MODEL_NAME = "exaone3.5:latest"

def ask_qwen(question):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": question,
            "stream": False
        }
    )

    data = response.json()
    print(data)
    # 오류 응답 형태: {'error': "model 'exaone3.5:latest' not found"}
    # 성공 응답 형태:
    # {'model': 'exaone3.5:2.4b', 
    #  'created_at': '2026-05-25T11:13:00.1202157Z', 
    #  'response': '답변', 
    #  'done': True, 
    #  'done_reason': 'stop', 
    #  'context': ["indices"], # 대화 관련 내용
    #  'total_duration': 37821514400, 
    #  'load_duration': 35526006800, 
    #  'prompt_eval_count': 51, # 입력 프롬프트 토큰 수
    #  'prompt_eval_duration': 228738100, 
    #  'eval_count': 104, # 생성 출력 값 토큰 수
    #  'eval_duration': 2017207400}
    return data["response"]

while True:
    user_input = input("질문: ")
    if user_input == "exit":
        print("종료합니다>")
        break

    print("응답:", ask_qwen(user_input))