# routes/reddit.py
from flask import Blueprint, request, jsonify, send_file
from yt_dlp import YoutubeDL
import os
from datetime import datetime

reddit_bp = Blueprint('reddit', __name__)
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')

@reddit_bp.route('/api/download/reddit', methods=['POST'])
def download_reddit():
    data = request.get_json()
    url = data.get('url')
    
    temp_dir = os.path.join(DOWNLOAD_DIR, f"rd_{datetime.now().strftime('%H%M%S')}")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        ydl_opts = {
            # FIX: Sirf wahi format uthao jo pehle se merge ho (bina FFmpeg ke)
            'format': 'best[ext=mp4]/best', 
            'outtmpl': os.path.join(temp_dir, '%(title).50s.%(ext)s'),
            'nocheckcertificate': True,
            'quiet': False,
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        files = os.listdir(temp_dir)
        if not files:
            return jsonify({"message": "Reddit video could not be processed"}), 500
            
        return send_file(os.path.join(temp_dir, files[0]), as_attachment=True)
    except Exception as e:
        print(f"!!! REDDIT ERROR: {str(e)}")
        return jsonify({"message": str(e)}), 500