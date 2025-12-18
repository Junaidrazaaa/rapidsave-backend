# routes/dailymotion.py
from flask import Blueprint, request, jsonify, send_file
from yt_dlp import YoutubeDL
import os
from datetime import datetime # Check karein ye line hai ya nahi

dailymotion_bp = Blueprint('dailymotion', __name__)
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')

@dailymotion_bp.route('/api/download/dailymotion', methods=['POST'])
def download_dailymotion():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "URL is missing"}), 400
        
    url = data.get('url')
    temp_dir = os.path.join(DOWNLOAD_DIR, f"dm_{datetime.now().strftime('%H%M%S')}")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(temp_dir, '%(title).50s.%(ext)s'),
            'nocheckcertificate': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        files = os.listdir(temp_dir)
        if not files: return jsonify({"message": "Download failed"}), 500
        
        return send_file(os.path.join(temp_dir, files[0]), as_attachment=True)
    except Exception as e:
        print(f"!!! DAILYMOTION ERROR: {str(e)}") # VS Code Terminal mein check karein
        return jsonify({"message": str(e)}), 500