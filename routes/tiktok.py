# routes/tiktok.py
from flask import Blueprint, request, jsonify, send_file
from yt_dlp import YoutubeDL
import os
from datetime import datetime

tiktok_bp = Blueprint('tiktok', __name__)
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')

@tiktok_bp.route('/api/download/tiktok', methods=['POST'])
def download_tiktok():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "TikTok URL is missing"}), 400
        
    url = data.get('url')
    temp_dir = os.path.join(DOWNLOAD_DIR, f"tt_{datetime.now().strftime('%H%M%S')}")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(temp_dir, '%(title).50s.%(ext)s'),
            'nocheckcertificate': True,
            'quiet': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        files = os.listdir(temp_dir)
        if not files: return jsonify({"message": "TikTok download failed"}), 500
        
        return send_file(os.path.join(temp_dir, files[0]), as_attachment=True)
    except Exception as e:
        print(f"!!! TIKTOK ERROR: {str(e)}")
        return jsonify({"message": str(e)}), 500