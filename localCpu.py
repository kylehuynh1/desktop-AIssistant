from ollama import chat

def testOpenApp(app: str):
    """Open an installed application on the user's Windows computer."""
    print(f"LOCAL TOOL CALLED: {app}")

def askLocal(prompt, tools):
    response = chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        tools=tools
    )
    return response

toolMap = {
    "testOpenApp": testOpenApp
}

response = askLocal(
    "yo can u throw spotify on",
    [testOpenApp]
)

toolCall = response.message.tool_calls[0]

toolName = toolCall.function.name
arguments = toolCall.function.arguments
app = arguments["app"]

toolFunction = toolMap[toolName]

toolFunction(**arguments)

print(toolName)
print(app)

