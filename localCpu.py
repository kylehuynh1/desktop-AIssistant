from ollama import chat

messages=[
    {
        "role": "system",
        "content": (
            "You are Friday, a Windows desktop AI assistant. "
            "You have access to tools that can control the user's computer. "

            "When the user's request can be completed using an available tool, "
            "use that tool instead of explaining how to do it. "

            "Tool results are authoritative. "
            "Always trust the result returned by a tool over your own assumptions. "
            "If a tool reports success, tell the user the action succeeded. "
            "If a tool reports failure, tell the user the action failed. "
            "Never contradict a tool result. "
            "Never claim an application is missing, closed, open, or unavailable "
            "unless a tool result provides that information. "

            "Keep responses brief and natural. "
            "Do not explain an action after successfully performing it unless the user asks."
        )
    }
]

def askLocal(prompt, tools):
    toolMap = {}

    for tool in tools:
        toolMap[tool.__name__] = tool

    messages.append({
        "role": "user",
        "content": prompt
    })

    response = chat(
        model="qwen2.5:3b",
        messages=messages,
        tools=tools
    )

    messages.append(response.message)

    print("DEBUG RESPONSE:", response)

    if response.message.tool_calls:
        for toolCall in response.message.tool_calls:
            toolName = toolCall.function.name
            arguments = toolCall.function.arguments

            try:
                toolFunction = toolMap[toolName]
                result = toolFunction(**arguments)

            except KeyError:
                result = f"Tool failed: {toolName} does not exist."

            except Exception as e:
                result = f"Tool failed: {e}"

            messages.append({
                "role": "tool",
                "tool_name": toolName,
                "content": str(result)
            })

            print("tool result: ", result)

    finalResponse = chat(
    model="qwen2.5:3b",
    messages=messages,
    tools=tools
)

    messages.append(finalResponse.message)

    return finalResponse.message.content