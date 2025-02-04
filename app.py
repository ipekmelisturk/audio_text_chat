from flask import Flask, render_template, request, jsonify
from agents import agent_1_suggest_questions, agent_2_diagnose
from audio_record import record_audio
from audio_to_text import save_audio, transcribe_audio
import os
import numpy as np
import tempfile

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze_input", methods=["POST"])
def analyze_input():
    """
    Process either a text input or transcribed audio input.
    """
    patient_input = request.form.get("message", "").strip()

    if not patient_input:
        return jsonify({"error": "No input received"}), 400

    diagnosis = agent_2_diagnose(patient_input)
    print(f"Diagnosis returned: {diagnosis}")  # Debugging

    questions_data = agent_1_suggest_questions(patient_input, [])

    return jsonify({
        "causes": diagnosis if diagnosis else [],
        "questions": questions_data["questions"]
    })


@app.route("/process_audio", methods=["POST"])
def process_audio():
    """
    Receives an audio file, transcribes it, and processes it.
    """
    if "audio" not in request.files:
        return jsonify({"error": "No audio file received"}), 400

    audio_file = request.files["audio"]
    temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    audio_file.save(temp_audio_path)

    transcription = transcribe_audio(temp_audio_path)

    return analyze_input({"message": transcription})

if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)
