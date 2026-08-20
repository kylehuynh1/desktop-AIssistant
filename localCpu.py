from ollama import chat, Client

def askLocal(prompt, tools):
    toolMap ={}
    for tool in tools:
        toolMap[tool.__name__] = tool

    for tool in tools:
        print("TOOL NAME:", tool.__name__)
        print("TOOL DOC:", tool.__doc__)
        print("ANNOTATIONS:", tool.__annotations__)

    response = chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Friday, a Windows desktop AI assistant. "
                    "You have access to tools that can control the user's computer. "
                    "When the user's request can be completed using an available tool, "
                    "use that tool instead of explaining how to do it."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        tools=tools
    )

    if response.message.tool_calls:
        for toolCall in response.message.tool_calls:
            toolName = toolCall.function.name
            arguments = toolCall.function.arguments

            toolFunction = toolMap[toolName]
            toolFunction(**arguments)
    return response.message.content

