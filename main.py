from flask import Flask, render_template, request, send_file
import os
from video_processor import process_video

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video = request.files["video"]
        input_path = os.path.join(UPLOAD_FOLDER, video.filename)
        output_path = os.path.join(PROCESSED_FOLDER, "result_" + video.filename)
        video.save(input_path)
        process_video(input_path, output_path)
        return send_file(output_path, as_attachment=True)
    return render_template("index.html")
