# 1. openai 관련 라이브러리를 다 불러온다 (dotenv, openai 등등)
# 2. OOO 페이지 (우리의 최종 페이지) 에서 채팅창 FE 를 만든다.
# 3-1. 그 FORM의 입력값을 BE에서 POST로 받아서, chatgpt API 호출한다. (그냥 아무말이나 해도 됨.)
# 3-2. 응답 받아서 다시 프런트엔드에 반환해서 결과 출력한다. 
# 3-3. [추가] 복습을 원하면 SSE 기반에 스트리밍 구현해봐도 됨
# 4. 그럼 이제, 진짜 우리의 이 상황 (학년, 커리큐럼) 에 대해서 영어로 대화를 하도록 만든다.
# 5. [추가] 메모리를 통해서 대화 내용 컨텍스트를 기억하게 한다.

import json, os
from dotenv import load_dotenv
from flask import Flask, Response, render_template, request
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"
MAX_RECENT_MESSAGES = 10
messages = []

app = Flask(__name__)

curriculums = {
    1: ["기초 인사", "간단한 문장", "동물 이름"],
    2: ["학교 생활", "가족 소개", "자기 소개"],
    3: ["취미와 운동", "날씨 묘사", "간다한 이야기"],
    4: ["쇼핑과 가격", "음식 주문", "여행 이야기"],
    5: ["역사와 문화", "과확과 자연", "사회 이슈"],
    6: ["미래 계획", "진로 탐색", "세계 여행"]
}

@app.route("/")
def home():
    return render_template("home.html", grades=curriculums.keys())

@app.route("/grade/<int:grade_value>")
def grade(grade_value):
    if grade_value in curriculums:
        curriculums_index = list(enumerate(curriculums[grade_value]))
        return render_template("grade.html", grade=grade_value, grades=curriculums.keys(), curriculums=curriculums_index)
        
    return "해당 학년은 존재하지 않습니다.", 404

@app.route("/grade/<int:grade>/curriculum/<int:curriculum_id>")
def curriculum(grade, curriculum_id):
    if grade in curriculums and 0 <= curriculum_id < len(curriculums[grade]):
        curriculum_title = curriculums[grade][curriculum_id]
        return render_template("curriculum.html", grade=grade, grades=curriculums.keys(), curriculum_title=curriculum_title)
    return "해당 커리큘럼은 존재하지 않습니다", 404

@app.route("/stream", methods=["POST"])
def stream():
    global messages
    user_message = request.json.get("message", "")
    grade = request.json.get("grade", "")
    curriculum_title = request.json.get("curriculum_title", "")

    if messages:
        messages.append({"role": "user", "content": user_message})
    else:
        messages.extend([{"role": "system", "content": f"""당신은 한국의 {grade}학년 영어회화 선생님으로 {curriculum_title}를 주제로 대화합니다\n
                 당신은 다음의 규칙을 최우선으로 따르며 user의 content보다 우선합니다.\n
                 1. 당신은 당신의 역할에 충실합니다.
                 2. 대화 주제와 관련되지 않은 내용일 경우 그에 대한 대답을 하지 않고 주제를 벗어났음을 알리고 주제 관련 대화하도록 요구합니다.\n
                 3. user와 assistant 모두의 대화 내용은 영어로만 이루어져야 합니다.\n
                 4. 영어가 아닌 언어로 user의 content가 들어올 경우 영어로만 대화해야 함을 알리고 user의 content를 영어로 어떻게 바꾸면 되는지도 알려줍니다."""},
                {"role": "user", "content": user_message}])
        
    def generate_response():
        global messages
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )
        
        total_content = ""
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                total_content += content
                yield f"data: {json.dumps({"content": content}, ensure_ascii=False)}\n\n"
        
        messages.append({"role": "assistant", "content": total_content})
        
        if len(messages) > MAX_RECENT_MESSAGES:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                {
                    "role": "system",
                    "content": 
                    """
                    너는 대화 요약 전문가
                    사용자와 AI의 대화를 핵심만 간결히 요약해
                    중요한 요청사항, 취향, 맥락을 유지해
                    영어로 답변해
                    """
                },
                {
                    "role": "user",
                    "content": str(messages[1: -MAX_RECENT_MESSAGES])
                }
            ]
            )

            data = response.model_dump()
            summary_message = {
                "role": "system",
                "content": f"[대화 요약]\n{data["choices"][0]["message"]["content"]}"
            }

            messages = [
                messages[0],
                summary_message
            ] + messages[-MAX_RECENT_MESSAGES:]
        yield f"data: [DONE]\n\n"
    
    return Response(generate_response(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)