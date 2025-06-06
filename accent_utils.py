import os
import tempfile
import yt_dlp
import whisper
from langdetect import detect

def download_audio_youtube(url):
    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    audio_path = tmp_wav.name
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    os.rename("audio.wav", audio_path)
    return audio_path

def estimate_accent(text):
    text = text.lower()
    american = ["gonna", "wanna", "gotta", "dude", "awesome", "bro", "kinda", "y’all"]
    british = ["shall", "cheers", "mate", "bloody", "brilliant", "rubbish", "fancy", "flat"]
    australian = ["g'day", "mate", "no worries", "arvo", "reckon", "heaps", "how ya going"]

    am = sum(word in text for word in american)
    br = sum(word in text for word in british)
    au = sum(word in text for word in australian)

    if au > max(am, br): return "Australian", 85
    elif am > max(br, au): return "American", 80
    elif br > max(am, au): return "British", 75
    else: return "Uncertain English", 60

def run_accent_detection(video_url):
    audio_path = download_audio_youtube(video_url)
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    transcript = result["text"]
    os.remove(audio_path)
    return transcript
