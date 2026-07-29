import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)  # Allows your HTML frontend to talk to this Python server

# Initialize the Gemini client (reads from Render environment variables)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


@app.route("/api/generate-quiz", methods=["POST"])
def generate_quiz():
  data = request.json
  subject = data.get("subject", "Algebra II")
  topic = data.get("topic", "Quadratic Equations")

  prompt = (
      f"Create a 3-question practice quiz for high school students on {subject}"
      f" focusing on {topic}. Include step-by-step solutions for each question."
      " Format the output clearly."
  )

  try:
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return jsonify({"success": True, "quiz": response.text})
  except Exception as e:
    return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/book-session", methods=["POST"])
def book_session():
  booking_data = request.json
  student_name = booking_data.get("name")
  tutor_name = booking_data.get("tutor")
  time = booking_data.get("time")

  # Here is where you would integrate:
  # 1. Twilio/SendGrid to email/text confirmation
  # 2. Google Calendar API to create the invite & Google Meet link

  print(
      f"Booking confirmed: {student_name} with {tutor_name} at {time}"
  )  # Logs to Render console

  return jsonify({
      "success": True,
      "message": (
          f"Session booked successfully with {tutor_name}! Confirmation"
          " email sent."
      ),
  })


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
