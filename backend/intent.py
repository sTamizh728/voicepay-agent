import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)

client = genai.Client()  # reads GEMINI_API_KEY from .env
MODEL = os.getenv("GEMINI_MODEL")

# The "tools" Gemini may choose from. Gemini only picks one and fills
# the details - it can never run them. Our Python code decides what to do.
send_money = types.FunctionDeclaration(
    name="send_money",
    description="The user wants to send money to a person.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "recipient_name": types.Schema(type="STRING", description="Name of the person, e.g. 'Sam'"),
            "amount": types.Schema(type="NUMBER", description="Amount to send, e.g. 20"),
            "currency": types.Schema(type="STRING", description="Currency code, default USD"),
        },
        required=["recipient_name", "amount"],
    ),
)

show_history = types.FunctionDeclaration(
    name="show_history",
    description="The user wants to see or understand their recent payments.",
    parameters=types.Schema(type="OBJECT", properties={}),
)

SYSTEM_RULES = (
    "You are VoicePay Agent, a payment assistant. "
    "Understand what the user wants and call the matching tool. "
    "If the name or amount is missing or unclear, do NOT guess: "
    "ask a short question instead."
)


def understand(user_text):
    """Turn what the user said into an intent dict, or a question back."""
    response = client.models.generate_content(
        model=MODEL,
        contents=user_text,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_RULES,
            tools=[types.Tool(function_declarations=[send_money, show_history])],
        ),
    )
    if response.function_calls:
        call = response.function_calls[0]
        return {"action": call.name, **dict(call.args)}
    return {"action": "ask_user", "message": response.text}