# routes/facebook.py
from flask import Blueprint, request, jsonify, send_file
from yt_dlp import YoutubeDL
import os
from datetime import datetime

facebook_bp = Blueprint('facebook', __name__)

# Local testing ke liye downloads folder
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@facebook_bp.route('/api/download/facebook', methods=['POST'])
def download_facebook():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "URL is missing"}), 400

    video_url = data.get('url')
    
    # Folder path local Windows ke hisab se
    temp_dir = os.path.join(DOWNLOAD_DIR, f"fb_{datetime.now().strftime('%H%M%S')}")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(temp_dir, '%(title).50s.%(ext)s'),
            'nocheckcertificate': True,
            'quiet': False, # Console mein download progress dekhne ke liye True ki jagah False
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        files = os.listdir(temp_dir)
        if not files:
            return jsonify({"message": "File could not be saved locally"}), 500
            
        return send_file(os.path.join(temp_dir, files[0]), as_attachment=True)

    except Exception as e:
        # Yeh terminal mein error print karega
        print(f"!!! FACEBOOK DOWNLOAD ERROR: {str(e)}")
        return jsonify({"message": str(e)}), 500