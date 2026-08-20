from ollama import chat

messages=[
    {
        "role": "system",
        "content": (
        "You are Friday, a Windows desktop AI assistant. "
        "You have access to tools that can control the user's computer. "
        "When the user's request can be completed using an available tool, "
        "use that tool instead of explaining how to do it."
        )
    }
]

def askLocal(prompt, tools):
    toolMap ={}
    for tool in tools:
        toolMap[tool.__name__] = tool

    messages.append({"role": "user", "content": prompt})

    response = chat(
        model="qwen2.5:3b",
        messages=messages,
        tools=tools
    )
    messages.append(response.message) #chat history

    print("DEBUG RESPONSE:", response)

    if response.message.tool_calls:
        for toolCall in response.message.tool_calls:
            toolName = toolCall.function.name
            arguments = toolCall.function.arguments

            toolFunction = toolMap[toolName]
            toolFunction(**arguments)
    return response.message.content

