import sys
from mcp.server.fastmcp import FastMCP
from mcp.client.stdio import stdio_client

mcp = FastMCP("HelloWorld")

@mcp.tool()
def hello(name: str) -> str:
    # 일반 print(sys.stdid)는 입력으로 인식해 오류 발생
    # sys.stderr로 입력해 오인 방지
    print(f"[SERVER] hello 함수 호출됨: name={name}", file=sys.stderr)
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(f"[SERVER] 서버가 시작됨", file=sys.stderr)
    mcp.run()