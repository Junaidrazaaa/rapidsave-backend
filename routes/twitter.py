# routes/twitter.py
from flask import Blueprint, request, jsonify, send_file
from yt_dlp import YoutubeDL
import os
from datetime import datetime

twitter_bp = Blueprint('twitter', __name__)
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')

@twitter_bp.route('/api/download/twitter', methods=['POST'])
def download_twitter():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "Twitter URL is missing"}), 400
        
    url = data.get('url').replace('x.com', 'twitter.com')
    temp_dir = os.path.join(DOWNLOAD_DIR, f"tw_{datetime.now().strftime('%H%M%S')}")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(temp_dir, '%(title).30s.%(ext)s'),
            'nocheckcertificate': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        files = os.listdir(temp_dir)
        if not files: return jsonify({"message": "Twitter download failed"}), 500
        
        return send_file(os.path.join(temp_dir, files[0]), as_attachment=True)
    except Exception as e:
        print(f"!!! TWITTER ERROR: {str(e)}")
        return jsonify({"message": str(e)}), 500