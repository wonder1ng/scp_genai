import websockets, asyncio
from websockets.asyncio.server import ServerConnection
async def handle_client(websocket):
    await websocket.send("서버에 연결됨")
    print("웹소켓 요청 시마다 호출")
    try:
        async for message in websocket:
            await websocket.send(f"서버가 받은 메시지: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("클라이언트가 연결 종료함")

async def main():
    print("메인 함수")
    async with websockets.serve(handle_client, "localhost", 8000):
        print("웹소켓을 열었음: ws://localhost:8000")
        await asyncio.Future()  # 요청이 올 때까지 기다림


if __name__ == "__main__":
    asyncio.run(main())