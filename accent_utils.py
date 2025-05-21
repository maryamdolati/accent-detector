import os
import tempfile
import yt_dlp
import whisper
from langdetect import detect

def download_audio_youtube(url):
    tmp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(tmp_dir, "audio.wav")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(tmp_dir, 'audio.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if not os.path.exists(audio_path):
        raise RuntimeError("Audio extraction failed")

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
    lang = detect(transcript)
    os.remove(audio_path)

    if lang != 'en':
        return None

    accent, confidence = estimate_accent(transcript)
    return accent, confidence, transcript
