from fastmcp import Client
import asyncio

client = Client("http://localhost:8000") # client if we are hosting server online
# client = Client(server/mcp) if we are hosting server locally, we can directly import the server/mcp and use it to create client

"""
Other option for more servers-
config = {
    "mcpServers": {
        "weather": {
            "url": "https://weather-api.example.com/mcp"
        },
        "assistant": {
            "command": "python",
            "args": ["./assistant_server.py"]
        }
    }
}

client = Client(config)
"""

async def call_tool(tool_name: str, tool_function_args: dict = {}):
    async with client:
        response = await client.call_tool(tool_name, tool_function_args) #within {} are func args if any
        print(response)

asyncio.run(call_tool())