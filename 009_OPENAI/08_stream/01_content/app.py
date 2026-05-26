import os, json
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, Response, request, send_from_directory

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = Flask(__name__, static_folder="public")

@app.route("/")
def index():
    return send_from_directory("public", "index.html")

@app.route("/stream", methods=["POST"])
def stream():
    user_message = request.json.get("message", "")

    def generate_response():
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 친절한 AI도우미입니다."},
                {"role": "user", "content": user_message}
            ],
            stream=True
        )
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield f"data: {json.dumps({"content": content}, ensure_ascii=False)}\n\n"
        yield f"data: [DONE]\n\n"
        print("chunk")
        print(chunk)
    
    return Response(generate_response(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)
