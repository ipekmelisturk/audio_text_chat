from flask import Flask, render_template, request, jsonify
from audio_record import record_audio
from audio_to_text import save_audio, transcribe_audio
from chat_agent import chat_with_agent

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process_audio_and_chat", methods=["POST"])
def process_audio_and_chat():
    """
    Handles audio recording, transcription, and chatbot responses.
    """
    try:
        duration = int(request.form.get("duration", 5))

        # Step 1: Record Audio
        audio_data = record_audio(duration)

        # Step 2: Save the Audio File
        file_name = "recorded_audio.wav"
        save_audio(file_name, audio_data)

        # Step 3: Transcribe Audio
        transcription = transcribe_audio(file_name)

        # Step 4: Get Chat Response
        chat_response = chat_with_agent(transcription)

        return jsonify({
            "transcription": transcription,
            "chat_response": chat_response
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
