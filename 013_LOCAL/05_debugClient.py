import asyncio, os
import sys
from mcp.server.fastmcp import FastMCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def full_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)

async def main():
    server_params = StdioServerParameters(command="python", args=[full_path("04_debugServer.py")])
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 아래 코드로 서버/클라 간 handshake가 이루어짐
            print("[CLIENT] 서버와 HS 전", file=sys.stderr)
            await session.initialize()
            print("[CLIENT] 서버와 HS 후", file=sys.stderr)

            tools = await session.list_tools().tools
            print("[CLIENT] 서버가 쓸 수 있는 도구 받아옴. 도구:", [t.name])

            result = await session.call_tool("hello", {"name": "John"})
            print(result.content[0].text)
    
if __name__ == "__main__":
    asyncio.run(main())