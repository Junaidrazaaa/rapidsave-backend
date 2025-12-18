# api.py
from flask import Flask
from flask_cors import CORS
import os

from routes.facebook import facebook_bp
from routes.youtube import youtube_bp
from routes.instagram import instagram_bp
from routes.tiktok import tiktok_bp
from routes.twitter import twitter_bp
from routes.reddit import reddit_bp
from routes.dailymotion import dailymotion_bp

app = Flask(__name__)

# SAB SE AHEM: CORS ko poore application aur saare routes par apply karein
CORS(app, resources={r"/api/*": {"origins": "*"}}) 

app.register_blueprint(facebook_bp)
app.register_blueprint(youtube_bp)
app.register_blueprint(instagram_bp)
app.register_blueprint(tiktok_bp)
app.register_blueprint(twitter_bp)
app.register_blueprint(reddit_bp)
app.register_blueprint(dailymotion_bp)

@app.route('/')
def home():
    return "All Systems Online!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=5000, host='0.0.0.0')