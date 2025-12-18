from flask import Blueprint, request, jsonify, send_file
from yt_dlp import YoutubeDL
import os
from datetime import datetime

youtube_bp = Blueprint('youtube', __name__)

# Local downloads folder creation
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@youtube_bp.route('/api/download/youtube', methods=['POST'])
def download_youtube():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "YouTube URL is missing"}), 400

    video_url = data.get('url')
    
    # Unique folder for this download
    temp_dir = os.path.join(DOWNLOAD_DIR, f"yt_{datetime.now().strftime('%H%M%S')}")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        ydl_opts = {
            # Bina FFmpeg ke best format
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(temp_dir, '%(title).50s.%(ext)s'),
            'nocheckcertificate': True,
            'quiet': False,
            'no_warnings': False,
            # Enhanced headers to mimic a real browser
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            },
            # iOS and Android clients bypass many restrictions
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android'],
                    'player_skip': ['webpage', 'configs'],
                }
            }
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        files = os.listdir(temp_dir)
        if not files:
            # Clear error message for frontend
            return jsonify({"message": "YouTube blocked the request or the link is invalid. Please try again."}), 400
            
        return send_file(os.path.join(temp_dir, files[0]), as_attachment=True)

    except Exception as e:
        # Logs mein error check karne ke liye
        print(f"!!! YOUTUBE DOWNLOAD ERROR: {str(e)}")
        return jsonify({"message": "Server error while processing YouTube video."}), 500
