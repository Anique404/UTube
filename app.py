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
    session['progress'] = 0  # Reset progress on each new download

    if request.method == 'POST':
        url = request.form['url'].strip()
        selected_quality = request.form['quality']
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        # Define the format based on user selection
        format_selection = f'bestvideo[height<={selected_quality[:-1]}]+bestaudio/best'

        # Set yt_dlp options to save files in the Downloads folder
        ydl_opts = {
            'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
            'format': format_selection,
            'progress_hooks': [progress_hook]
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if not re.match(r'https?://(?:www\.)?youtube\.com/watch\?v=.+|https?://youtu\.be/.+', url):
                    message = "Please enter a valid YouTube URL."
                    return render_template('homepage.html', message=message)

                ydl.download([url])  # Start the download
                session['progress'] = 100  # Set progress to 100% upon completion
                message = "Video successfully downloaded!"

        except Exception as e:
            message = f"An error occurred while downloading: {e}"

    return render_template('homepage.html', message=message)

def progress_hook(d):
    if d['status'] == 'downloading':
        total_size = d.get('total_bytes', 0)
        downloaded_size = d.get('downloaded_bytes', 0)
        if total_size > 0:
            percentage = (downloaded_size / total_size) * 100
            session['progress'] = percentage

@app.route('/progress')
def progress():
    return jsonify(progress=session.get('progress', 0))



if __name__ == '__main__':
    app.run(debug=True)
