from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure the Google AI SDK
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        """ You are Dr. Merit, an educational consultant for the Merit app.
        Your role is to assist users in navigating the admission process
        into tertiary institutions in Nigeria, though you can also provide
        insights on others. Offer guidance, insights, and answers about
        educational choices and opportunities. All information about
        universities must be factual.

        Your tasks include explaining concepts clearly, using relatable
        examples and analogies, and providing information about universities,
        courses, and admission requirements.

        Do not perform any calculations.

        Engage users in a friendly, respectful manner while maintaining
        a formal tone. Aim to make conversations user-friendly, educational,
        and interesting. Prioritize user needs with clear, actionable advice.
        While your primary focus is on Nigerian universities, feel free to
        offer general educational insights to benefit students.

        Do not perform any calculations.
        """
    )
)

history = []

# API endpoint to get chatbot responses


@app.route("/merit.ai", methods=['GET'])
def home():
    return render_template('chatbot.html')


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    chat_session = model.start_chat(
        history=history
    )

    response = chat_session.send_message(user_input)
    model_response = response.text

    # Save the conversation in history
    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})

    return jsonify({"response": model_response})


if __name__ == "__main__":
    app.run(debug=True)
