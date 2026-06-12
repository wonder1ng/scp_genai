from datetime import datetime
import sys
from mcp.server.fastmcp import FastMCP
from mcp.client.stdio import stdio_client

# 기본 port = 8000
mcp = FastMCP("my-http-mcp-server", port=5555)
mcp = FastMCP("my-http-mcp-server")

@mcp.tool()
def hello(name: str) -> str:
    """사용자에게 인사말을 생성하는 도구
        매개변수:
            name(str): 이사할 대상의 이름
        반환값:
            str: "Hello, {name}!" 형태의 인사말
    """
    return f"Hello, {name}!"

@mcp.tool()
def add(a: int, b: int) -> int:
    """두 정수를 더함"""
    return a + b

@mcp.tool()
def now() -> str:
    """두 정수를 곱함"""
    return datetime.now().strftime("지금 시간은 %Y-%m-%d %H:%M:%S 입니다.")


@mcp.tool()
def word_count(text: str) -> int:
    """문자열의 단어 개수 반환"""
    return len(text.split())


if __name__ == "__main__":
    # stdio -> http 서버로 전환
    mcp.run(transport="streamable-http")