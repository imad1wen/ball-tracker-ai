from video_processor import process_video
from flask import send_file, request, Flask, render_template
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

    # معالجة الفيديو
    output_path = process_video(video_path)

    # إرسال الملف الناتج للمستخدم
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    
