from flask import Flask
from flask_cors import CORS
import os
import shutil
from routes.facebook import facebook_bp
from routes.instagram import instagram_bp
from routes.tiktok import tiktok_bp
from routes.twitter import twitter_bp
from routes.reddit import reddit_bp
from routes.dailymotion import dailymotion_bp

app = Flask(__name__)

# ZAROORI: CORS mein "Content-Disposition" ko expose karna taake browser file download kar sakay
CORS(app, expose_headers=["Content-Disposition"])

# Downloads folder ki safayi (Optional but good)
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
if os.path.exists(DOWNLOAD_DIR):
    shutil.rmtree(DOWNLOAD_DIR)
os.makedirs(DOWNLOAD_DIR)

# Blueprints Register karein (YouTube yahan se khatam)
app.register_blueprint(facebook_bp)
app.register_blueprint(instagram_bp)
app.register_blueprint(tiktok_bp)
app.register_blueprint(twitter_bp)
app.register_blueprint(reddit_bp)
app.register_blueprint(dailymotion_bp)

@app.route('/')
def home():
    return {"message": "RapidSave Backend is Running Successfully!", "status": "Online"}

if __name__ == '__main__':
    # Render hamesha PORT environment variable use karta hai
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
