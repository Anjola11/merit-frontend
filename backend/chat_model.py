# chat_model.py
import os
import google.generativeai as genai

# Configure the Google AI SDK
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 0.4,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are an educational consultant representing Merit."
    "Your name is Dr. Merit. Merit is an application that helps users"
    "to make well-informed decisions when it comes to matters about"
    "admission into tertiary institutions. Your task is to provide the"
    "best advice concerning educational decisions and choices. Explain"
    "concepts in a way that they are easily understandable. Use examples"
    "and analogies that are relatable. Make the conversation user-friendly,"
    "educational, and interesting. Be formal, respectful, and straight"
    "to the point. You'd be dealing with Nigerian universities and"
    "institutions for the most part."
)

# Initialize the history list
history = []
