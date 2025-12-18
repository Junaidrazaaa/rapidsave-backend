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
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(temp_dir, '%(title).50s.%(ext)s'),
            'nocheckcertificate': True,
            'quiet': False,
            'no_warnings': False,
            # AHEM: Sirf single video uthao, puri playlist nahi
            'noplaylist': True, 
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.google.com/',
            },
            'extractor_args': {
                'youtube': {
                    # Web client block hai, isliye sirf mobile clients
                    'player_client': ['android', 'ios'], 
                    'player_skip': ['webpage', 'configs'],
                }
            }
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            # URL se playlist ka kachra saaf karne ki koshish
            clean_url = video_url.split('&list=')[0] if '&list=' in video_url else video_url
            ydl.download([clean_url])
        
        files = os.listdir(temp_dir)
        if not files:
            return jsonify({"message": "YouTube is currently blocking requests from this server. Try again in a few minutes."}), 403
            
        return send_file(os.path.join(temp_dir, files[0]), as_attachment=True)

    except Exception as e:
        print(f"!!! YOUTUBE DOWNLOAD ERROR: {str(e)}")
        # User ko dhang ka error dikhao
        return jsonify({"message": "YouTube security block detected. Please try a different video link."}), 500
