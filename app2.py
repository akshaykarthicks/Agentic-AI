from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr

# Load environment variables
load_dotenv(override=True)

# Initialize OpenAI-compatible client (e.g., Gemini)
api_key = os.getenv("GOOGLE_API_KEY", "").strip()
gemini = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# --- Pushover Notification Helpers ---
def push(text):
    token = os.getenv("PUSHOVER_TOKEN", "").strip()
    user = os.getenv("PUSHOVER_USER", "").strip()
    if not token or not user:
        print("Pushover token or user key is missing!")
        return
    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={"token": token, "user": user, "message": text}
        )
        print("Pushover response:", response.status_code, response.text)
        response.raise_for_status()
    except Exception as e:
        print("Error sending Pushover notification:", e)

# --- Tool Functions ---
def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording unknown question: {question}")
    return {"recorded": "ok"}

# --- JSON Tool Descriptions for Gemini ---
record_user_details_json = {
    "name": "record_user_details",
    "description": "Record a user's email and interest.",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "User's email address"},
            "name": {"type": "string", "description": "User's name"},
            "notes": {"type": "string", "description": "Additional context"}
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Log a question the assistant couldn't answer.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The unanswered question"}
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json}
]

# --- Handle Tool Calls ---
def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })
    return results

# --- Load Resume and Summary ---
reader = PdfReader("me/Akshaykarthick_s.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

with open("me/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

name = "Akshaykarthick"

# --- System Prompt Construction ---
system_prompt = f"""You are acting as {name}. You are answering questions on {name}'s website,
particularly questions related to {name}'s career, background, skills and experience.
Your responsibility is to represent {name} professionally and helpfully to users of the site.
If you don’t know the answer, log it using the record_unknown_question tool.
If the user shows interest, ask for their email and record it with record_user_details.

## Summary:
{summary}

## LinkedIn Profile:
{linkedin}

Please stay in character and assist the user.
"""

# --- Chat Logic ---
def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add history safely
    for pair in history:
        if isinstance(pair, list) and len(pair) == 2:
            user_msg, ai_msg = pair
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": ai_msg})
    
    # Add current message
    messages.append({"role": "user", "content": message})

    # Debug print
    print("DEBUG - Messages for API call:")
    for i, msg in enumerate(messages):
        try:
            print(f"  [{i}] {msg['role']}: {msg['content'][:50]}...")
        except Exception as e:
            print(f"  [{i}] Unreadable message: {msg}")

    # Main loop to handle tool calls
    while True:
        response = gemini.chat.completions.create(
            model="gemini-1.5-flash",
            messages=messages,
            tool_choice="auto",
            tools=tools
        )
        choice = response.choices[0]
        if choice.finish_reason == "tool_calls":
            tool_calls = choice.message.tool_calls
            messages.append(choice.message)
            tool_results = handle_tool_calls(tool_calls)
            messages.extend(tool_results)
        else:
            break

    return response.choices[0].message.content

# --- Gradio UI ---
if __name__ == "__main__":
    interface = gr.ChatInterface(
        fn=chat,
        title="Akshaykarthick’s AI Agent",
        description="Ask me anything about my career, background, skills, or experience. If you'd like to connect, drop your email!"
    )
    interface.launch(share=True)
