import inspect
import mcp
from mcp import ClientSession
from mcp.server.fastmcp import FastMCP
from importlib.metadata import version

print(f"MCP version: {version("mcp")}")

print("\nMCP 문서\n=========")
print(inspect.getdoc(FastMCP))
print("\nFastMCP.sse_app 문서\n=========")
print(inspect.getdoc(FastMCP.sse_app))

print("\nClientSession 문서\n=========")
print(inspect.getdoc(ClientSession))
print(inspect.getdoc(ClientSession.initialize))