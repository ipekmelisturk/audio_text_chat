from flask import Flask, render_template, request, jsonify
from agents import agent_1_suggest_questions, agent_2_diagnose

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze_input", methods=["POST"])
def analyze_input():
    """
    API Route: Accepts text input, provides possible causes,
    and then suggests questions.
    """
    patient_input = request.form.get("message", "").strip()
    previous_questions = request.form.get("previous_questions", "[]")  # Get previous questions
    previous_questions = eval(previous_questions) if previous_questions else []

    if not patient_input:
        return jsonify({"error": "No input received"})

    try:
        print(f"Received patient input: {patient_input}")  # Debugging

        # Step 1: Get possible causes
        diagnosis = agent_2_diagnose(patient_input)
        print(f"Diagnosis returned: {diagnosis}")  # Debugging

        # Step 2: Get **NEW** suggested questions
        questions_data = agent_1_suggest_questions(patient_input, previous_questions)
        print(f"Suggested Questions returned: {questions_data}")  # Debugging

        return jsonify({
            "causes": diagnosis if diagnosis else [],  # ✅ Ensures no null values
            "questions": questions_data["questions"]  # ✅ Dynamic questions
        })

    except Exception as e:
        print(f"Error in /analyze_input: {e}")  # Debugging error
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
