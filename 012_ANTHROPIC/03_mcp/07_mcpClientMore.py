import asyncio, sys, os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def full_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)

async def main():
    # params = StdioServerParameters(command="python", args=["06_mcpServerMoretools.py"])
    params = StdioServerParameters(command=sys.executable, args=[full_path("06_mcpServerMoretools.py")])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = (await session.list_tools()).tools
            
            print("[CLIENT] 서버가 쓸 수 있는 도구 받아옴. 도구:", [t.name for t in tools])

            result = await session.call_tool("add", {"a": 3, "b": 5})
            print("add 결과:", result)
            
            result = await session.call_tool("add", {"a": 3, "b": 5})
            print("add 결과:", result)

if __name__ == "__main__":
    asyncio.run(main())