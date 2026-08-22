import os
from flask import Flask, render_template, request, jsonify
import whisper

app = Flask(__name__)

# Load original OpenAI Whisper model
model = whisper.load_model("base")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    temp_path = "temp_recording.webm"
    audio_file.save(temp_path)

    try:
        # openai-whisper returns a dictionary
        result = model.transcribe(temp_path)
        transcript = result.get("text", "").strip()

        # Overwrite the output file
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(transcript)

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return jsonify({'transcript': transcript})

if __name__ == '__main__':
    app.run(debug=True)