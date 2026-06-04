import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from openai import OpenAI
import requests

load_dotenv()
app = Flask(__name__, static_folder="public")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"

@app.route("/")
def index():
    return send_from_directory("public", "index.html")

@app.route("/api/codecheck", methods=["POST"])
def code_check():
    data = request.get_json()
    print("data")
    print(data)
    message = data.message
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "너는 모든 프로그래밍 언어에 통달한 경력 40년 차의 프로그래머야\n다음 코드를 보고 코드 리뷰를 간단하지만 핵심 있게 해"},
            {"role": "user", "content": message}
            ],
    )
    
    return jsonify({"result": response.choices[0].message.content})

@app.route("/web")
def web():
    return send_from_directory("public", "web.html")

@app.route("/web/api/codecheck", methods=["POST"])
def web_code_check():
    data = request.get_json()
    code_url = data["codeUrl"]
    checked = data["checked"]
    weaks = ", ".join([data["weaks"][i] for i in range(len(checked)) if checked[i]])
    
    if code_url.find("ithub"):
        if code_url.find("ithub.com"):
            code_url = code_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/refs/heads/")
    else:
        return jsonify({"result": "url 오류"})
    resp = requests.get(code_url)
    if (resp.status_code != 200):
        print(resp.status_code)
        code_url = code_url.replace("/refs/heads/", "/")
        resp = requests.get(code_url)
        if (resp.status_code != 200):
            print(code_url)
            return jsonify({"result": "url 오류"})
    code = resp.text.split("\n")
    code = "\n".join([f"{i+1} {code[i]}" for i in range(len(code))])
    print("code")
    print(code)
    prompt = (
        "다음 소스코드를 보고 취약점을 분석하시오.\n"
        f"다음 항목의 보안 위험에 대해 항목 별로 설명하시오. {weaks}"
        "코드의 각 줄 첫 숫자는 코드의 줄 번호"
        "각 취약점에 대해 해당 코드의 라인 번호, 코드 스니펫, 취약점 설명과 개선 방안을 간단하게 설명하시오. 코드 내의 주석은 무시하라.\n\n"
        f"라인 번호는 숫자와 콤마로만 나열"
        "소스코드:\n"
        "----------\n"
        f"{code}\n"
        "----------\n"
    )

    # response = '코드 리뷰를 통해 다음의 주요 보안 위험을 분석하였으며, 각 취약점에 대한 설명과 개선 방안을 제시합니다.\n\n### 1. 민감정보(하드 코딩된 암호)\n- **라인 번호**: 16\n- **코드 스니펫**: `# cursor.execute("INSERT INTO users (username, password) VALUES (\'admin\', \'admin123\')")`\n- **취약점 설명**: 하드코딩된 사용자명과 비밀번호는 소스코드에 직접 삽입되어 있어, 외부인이 소스코드를 유출하거나 접근할 경우 민감정보가 노출될 수 있습니다.\n- **개선 방안**: 비밀번호는 환경 변수나 구성 파일 등의 안전한 장소에 저장하고, 하드코딩하지 않는 방식을 사용해야 합니다.\n\n### 2. SQL Injection\n- **라인 번호**: 32\n- **코드 스니펩**: `query = f"SELECT * FROM users WHERE username = \'{username}\' AND password = \'{password}\'"`\n- **취약점 설명**: 사용자가 입력한 데이터를 직접 SQL 쿼리에 통합하여 DB에 접근하는 구조로, 이를 통해 공격자가 쿼리를 조작할 수 있습니다. 예를 들어, `username`에 `\' OR \'1\'=\'1`을 입력하면 인증 우회를 할 수 있습니다.\n- **개선 방안**: SQL 쿼리에서 사용자 입력을 사용할 때는 Prepared Statements를 활용해 사용자 입력을 안전하게 처리해야 합니다. 즉, parameters binding을 통해 방어할 수 있습니다.\n\n### 3. XSS (Cross-Site Scripting)\n- **라인 번호**: 60\n- **코드 스니펫**: `return "<h1>Welcome to the secure area!</h1>"`\n- **취약점 설명**: 동적으로 생성된 HTML 코드에서 사용자 입력을 검증하지 않는다면, XSS 공격에 취약해질 수 있습니다. 예를 들어, 사용자가 특수 문자를 삽입할 경우 HTML에서 코드 실행이 가능해질 수 있습니다.\n- **개선 방안**: 사용자 입력을 HTML에 직접적으로 출력하는 경우, HTML 특수 문자를 이스케이프 처리하여 XSS 공격을 방지해야 합니다. Flask에서는 `escape()` 함수를 사용할 수 있습니다.\n\n### 4. Software Supply Chain Failures\n- **라인 번호**: 7\n- **코드 스니펫**: `import sqlite3`\n- **취약점 설명**: 코드에서 의존하고 있는 외부 라이브러리나 패키지가 취약점을 포함하고 있을 경우, 보안 공격에 노출될 수 있습니다. 특히, 외부 파이썬 라이브러리에서 알려진 보안 취약점이 발생할 경우 큰 위험을 초래할 것입니다.\n- **개선 방안**: 외부 라이브러리에 대한 보안 패치를 정기적으로 적용하고, 신뢰할 수 있는 소스에서만 패키지를 다운로드 및 사용해야 합니다. 또한, 패키지의 업데이트와 패치 노트를 주기적으로 확인하여, 발견된 취약점에 대한 대응을 해야 합니다.\n\n이러한 취약점들은 애플리케이션 보안을 위협할 수 있으며, 적절한 방어 조치를 취해야 합니다.'
    # tmp_lines = [7, 16, 32, 60]
    # return jsonify({"result": response, "sourceCode": code, "url": code_url, "lines": lines})
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "너는 모든 프로그래밍 언어에 통달한 경력 40년 차의 프로그래머야\n다음 코드를 보고 코드 리뷰를 간단하지만 핵심 있게 해"},
            {"role": "user", "content": prompt}
            ],
    )
    tmp_lines = [line.replace("- **라인 번호**: ", "") for line in response.choices[0].message.content.split("\n") if line.startswith("- **라인 번호**: ")]
    lines = []
    for line in tmp_lines:
        for n in line.split(", "):
            lines.append(int(n))
            
    return jsonify({"result": response.choices[0].message.content, "sourceCode": code, "url": code_url, "lines": lines})

if __name__ == "__main__":
    app.run(debug=True)