from flask import Blueprint, request, jsonify, send_file
from yt_dlp import YoutubeDL
import os
from datetime import datetime

youtube_bp = Blueprint('youtube', __name__)

DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@youtube_bp.route('/api/download/youtube', methods=['POST'])
def download_youtube():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "YouTube URL is missing"}), 400

    video_url = data.get('url')
    temp_dir = os.path.join(DOWNLOAD_DIR, f"yt_{datetime.now().strftime('%H%M%S')}")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Cookies file check
        cookie_path = os.path.join(os.getcwd(), 'cookies.txt')

        ydl_opts = {
            'format': 'best[ext=mp4]/best', # Bina FFmpeg ke best
            'outtmpl': os.path.join(temp_dir, '%(title).50s.%(ext)s'),
            'nocheckcertificate': True,
            'quiet': False,
            'noplaylist': True,
            'cookiefile': cookie_path if os.path.exists(cookie_path) else None, #
            
            # PoToken bypass aur latest YouTube patches
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'mweb'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
            
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Referer': 'https://www.google.com/',
            }
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            # Playlist links se bachne ke liye cleaning
            clean_url = video_url.split('&list=')[0] if '&list=' in video_url else video_url
            ydl.download([clean_url])
        
        files = os.listdir(temp_dir)
        if not files:
            return jsonify({"message": "YouTube blocked the extraction. Please update your cookies.txt"}), 403
            
        return send_file(os.path.join(temp_dir, files[0]), as_attachment=True)

    except Exception as e:
        print(f"!!! YOUTUBE DOWNLOAD ERROR: {str(e)}") #
        return jsonify({"message": f"Server Error: {str(e)}"}), 500
