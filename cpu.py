from google import genai
from google.genai import types
from google.genai import errors
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def askGEM(prompt, tools):

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=tools,
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode="AUTO"
                    )
                )
            )
        )
        return response.text
    except errors.ClientError as error:
        if error.code == 429:
            return "I'm being actively rate limited at the moment. Try again shortly."
        print(f"Error: {error}")
        return "Sorry, I encountered an error while processing your request."
