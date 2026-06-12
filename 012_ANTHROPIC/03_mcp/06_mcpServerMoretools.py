from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-more")

@mcp.tool()
def add(a: int, b: int) -> int:
    """두 정수를 더함"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """두 정수를 곱함"""
    return a * b

@mcp.tool()
def word_count(text: str) -> int:
    """문자열의 단어 개수 반환"""
    return len(text.split())

if __name__ == "__main__":
    mcp.run()