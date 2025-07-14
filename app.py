from flask import Flask, request, jsonify, render_template
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "YouTube Downloader API",
        "usage": "/download?url=VIDEO_URL"
    })

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    output_filename = f"{uuid.uuid4()}.mp4"
    output_path = os.path.join("/tmp", output_filename)

    try:
        subprocess.run([
            "yt-dlp", "-f", "best", "-o", output_path, url
        ], check=True)

        return jsonify({
            "message": "Downloaded successfully!",
            "file_saved_to": output_path
        })
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Download failed", "details": str(e)}), 500

@app.route("/docs")
def docs():
    return render_template("docs.html")
