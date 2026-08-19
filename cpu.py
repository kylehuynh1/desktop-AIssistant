from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def askGEM(prompt):
    instructions = """
    You are Friday, a helpful and friendly AI assistant. You will answer questions and provide information in a clear and concise manner. 
    Please be polite and professional in your responses.
    
    If the user wants to open an application, respond with:
    ACTION: open_app
    TARGET: application_name

    if not , respond with a normal answer to the user's question like so: 
    ACTION: respond
    TARGET: your_response
    """

    fullPrompt = f"""
    {instructions}
    User: {prompt}
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=fullPrompt
    )
    lines = response.text.splitlines()
    action = lines[0].split(":")[1].strip()
    target = lines[1].split(":")[1].strip()

    return action, target
