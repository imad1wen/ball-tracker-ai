from video_processor import process_video
from flask import send_file
from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return 'لم يتم اختيار فيديو', 400

    video = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)

    return f'✅ تم رفع الفيديو بنجاح: {video.filename}'

if __name__ == '__main__':
    app.run(debug=True)
