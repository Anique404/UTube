from flask import Flask, render_template, request, jsonify, session
import os
import re
import yt_dlp

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/contact-us')
def contact():
    return render_template('contact-us.html')

@app.route('/privacy-and-policy')
def privacy_policy():
    return render_template('privacy.html')

@app.route('/terms-and-conditions')
def terms_conditions():
    return render_template('termsandconditions.html')


@app.route('/download', methods=['POST'])
def download():
    message = None

    if request.method == 'POST':
        url = request.form['url'].strip()
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        # Set yt_dlp options to save files in the Downloads folder
        ydl_opts = {
            'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),  # Output template
            'noplaylist': False,  # Allow playlist downloads
            'format': 'best',  # Download the best quality available
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if "playlist" in url:
                    playlist_info = ydl.extract_info(url, download=False)
                    message = f"Downloading playlist: {playlist_info['title']}"
                    ydl.download([url])
                    message += " - All videos downloaded successfully!"
                else:
                    if not re.match(r'https?://(?:www\.)?youtube\.com/watch\?v=.+|https?://youtu\.be/.+', url):
                        message = "Please enter a valid YouTube URL."
                        return render_template('homepage.html', message=message)

                    video_info = ydl.extract_info(url, download=True)
                    message = "Video successfully downloaded!"

        except Exception as e:
            message = f"An error occurred while downloading: {e}"

    return render_template('homepage.html', message=message)

@app.route('/progress')
def progress():
    return jsonify(progress=session.get('progress', 0))  # Return current progress

if __name__ == '__main__':
    app.run(debug=True)