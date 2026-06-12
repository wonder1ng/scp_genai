import asyncio, os
import sys
from mcp.server.fastmcp import FastMCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def full_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)

async def main():
    # server_params = StdioServerParameters(command="python", args=[full_path("02_mcpServer.py")])
                                            # "python"은 어떤 python 환경이 실행될지 모름
    server_params = StdioServerParameters(command=sys.executable, args=[full_path("02_mcpServer.py")])
                                            # sys.executable은 지금 실행 중인 것
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 아래 코드로 서버/클라 간 handshake가 이루어짐
            await session.initialize()
            # 이제부터 실제로 서버에 호출
            result = await session.call_tool("hello", {"name": "John"})
            print(result.content[0].text)
    
if __name__ == "__main__":
    asyncio.run(main())