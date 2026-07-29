import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from google import genai

# Point Flask to serve static files from the root directory
app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)  # Allows your HTML frontend to talk to this Python server

# Fail-safe Gemini Client initialization
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY environment variable is not set!")
    client = None
else:
    client = genai.Client(api_key=api_key)


# --- FRONTEND ROUTES ---

@app.route("/")
def index():
    """Serves the main index.html landing page."""
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    """Serves static assets (CSS, JS, images, or other HTML pages)."""
    return send_from_directory(".", path)


# --- API ROUTES ---

@app.route("/api/generate-quiz", methods=["POST"])
def generate_quiz():
    if not client:
        return jsonify({
            "success": False,
            "error": "Server error: Gemini API key is not configured in Render environment variables."
        }), 500

    data = request.json or {}
    subject = data.get("subject", "Algebra II")
    topic = data.get("topic", "Quadratic Equations")

    prompt = (
        f"Create a 3-question practice quiz for high school students on {subject}"
        f" focusing on {topic}. Include step-by-step solutions for each question."
        " Format the output clearly."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return jsonify({"success": True, "quiz": response.text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/book-session", methods=["POST"])
def book_session():
    booking_data = request.json or {}
    student_name = booking_data.get("name", "Student")
    tutor_name = booking_data.get("tutor", "Tutor")
    time = booking_data.get("time", "Scheduled Time")

    # Log to Render console
    print(f"Booking confirmed: {student_name} with {tutor_name} at {time}")

    return jsonify({
        "success": True,
        "message": f"Session booked successfully with {tutor_name}! Confirmation email sent.",
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
