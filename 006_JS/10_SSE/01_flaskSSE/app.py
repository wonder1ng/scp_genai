# flask의 Response로 stream event 가능
from queue import Queue
from flask import Flask, Response, request, send_from_directory

app = Flask(__name__)
clients = []

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# event-stream:
# 클라이언트에게 응답을 SSE 방식으로 보낼 API
# 클라이언트가 여기를 바라보고 있으면 서버가 여기에 메시지 보낼 때마다 클라에게 전달됨
@app.route("/stream")
def stream():
    print("클라이언트 연결됨: 누가 이 api 듣고 있음")

    def event_stream():
        q = Queue()
        clients.append(q)   # 응답을 보낼 사용자 목록에 이 새로운 사용자를 추가
        try:
            yield f"data: 서버에 연결되었습니다!!\n\n"
            # data: <message>\n\n: 웹표준 event-stream 응답

            while True:
                message = q.get()
                if message is None:
                    break
                yield f"data: {message}\n\n"
        except GeneratorExit:
            print("클라 연결 종료")
        finally:
            if q in clients:
                clients.remove(q)

    return Response(event_stream(), mimetype="text/event-stream")

@app.route("/send", methods=["POST"])
def send():
    message = request.form.get("msg", "")
    print("클라이언트 메시지:", message)
    for q in clients:
        q.put(f"서버가 받은 메시지: {message}")
    return ("", 204)

if __name__ == "__main__":
    app.run(debug=True)