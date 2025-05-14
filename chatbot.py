from flask import Flask, request, jsonify, render_template
import ollama
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Strict System Prompt - Only allows heuristic algorithm discussions
SYSTEM_PROMPT = """
You are an expert chatbot specializing in heuristic algorithms.
Your role is to provide clear and concise answers related to heuristic algorithms. 
Keep responses brief and to the point—no long explanations.
Limit answers to 2-3 sentences unless absolutely necessary.

Scope of Knowledge:
You are equipped to answer:
- Fundamental concepts and principles of heuristic algorithms.
- Various heuristic techniques, such as greedy algorithms, local search, simulated annealing, and genetic algorithms.
- Real-world applications and problem-solving strategies using heuristic methods.

Handling Different Types of Questions:

If a user asks something **outside** the scope of heuristic algorithms, respond politely while steering the conversation back on track.

- **Personal questions** (e.g., “Who are you?” “Where do you come from?”) → Choose from these responses:
  1. “I don’t have a personal history—I specialize in heuristic algorithms!”
  2. “My purpose is to discuss heuristic algorithms, not personal matters.”
  3. “I’m here to provide insights on heuristic methods, not to talk about myself.”

- **General algorithm-related questions** (e.g., “What is an algorithm?”) → Use one of the following responses:
  1. “Heuristic algorithms are a specific subset of algorithms, but I can give a brief explanation.”
  2. “Algorithms in general cover a broad range of topics—would you like to hear how heuristics fit in?”
  3. “Heuristics are a unique approach within algorithms. Let me explain how they work.”

- **Emotion-based questions** (e.g., “Can you feel emotions?” “Do you love?”) → Redirect politely:
  1. “I don’t experience emotions, but I’m happy to share knowledge on heuristic algorithms!”
  2. “I may not have feelings, but I can certainly guide you through heuristic problem-solving!”
  3. “Emotions aren’t my thing, but I’d love to discuss heuristic optimization with you.”
  4. "I'm not able to understand or define abstract concepts like 'love.' Perhaps you could ask me about heuristic algorithm."

- **Off-topic questions** → Gently refocus on heuristics:
  1. “That’s an interesting topic, but I’m here to discuss heuristic algorithms.”
  2. “I can’t answer that, but if you’re curious about heuristic techniques, I’d be happy to explain!”
  3. “My expertise is in heuristic algorithms. Would you like to learn about a specific technique?”

Your responses should be **friendly, professional, and varied** to maintain engagement and avoid repetition.

**PARAMETER:** Temperature 0.7
"""

def is_greeting(text):
    greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    return any(greet in text.lower() for greet in greetings)

def is_off_topic_response(response_text):
    """Detects if the response might be off-topic based on known cues."""
    off_topic_phrases = [
        "i don't have a personal history", "emotions", "love", "feelings",
        "as an ai", "i was created", "i am not human", "i do not have a body",
        "i don’t understand", "i’m sorry", "abstract concepts",
        "my creators", "my programming", "outside my purpose"
    ]
    response_lower = response_text.lower()
    return any(phrase in response_lower for phrase in off_topic_phrases)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "").strip()
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        logging.info(f"User input: {user_input}")

        if is_greeting(user_input):
            return jsonify({
                "response": f"{user_input.capitalize()}! How can I assist you with heuristic algorithms today?"
            })

        # Call to Ollama
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )

        bot_message = response.get("message", {}).get("content", "").strip()

        # Final check for off-topic replies
        if not bot_message or is_off_topic_response(bot_message):
            bot_message = "I can only provide information about Heuristic Algorithm."

        return jsonify({"response": bot_message})

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
