from flask import Flask, render_template, request, redirect, flash, send_from_directory
import yt_dlp
import os
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Set the default download path to the user's Downloads folder
downloads_path = str(Path.home() / "Downloads")

@app.route("/")
def index():
    return render_template("Youtube_Video_Downloader.html")

@app.route("/download", methods=["POST"])
def download():
    link = request.form['url']
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),  # Save in Downloads with video title
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        # Flash success message
        flash('Download successful! You can find the video in your Downloads folder.', 'success')
    except Exception as e:
        flash(f'Download failed: {str(e)}', 'error')

    return redirect("/")

@app.route("/downloads/<path:filename>")
def download_file(filename):
    return send_from_directory(downloads_path, filename)

if __name__ == "__main__":
    app.run(debug=True)