import os
import tempfile
import urllib.request
import whisper
from langdetect import detect
from moviepy.editor import VideoFileClip
import yt_dlp

def is_youtube_url(url):
    return "youtube.com" in url or "youtu.be" in url

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
        raise RuntimeError("Audio extraction from YouTube failed")

    return audio_path

def download_audio_direct(url):
    tmp_video = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    video_path = tmp_video.name
    urllib.request.urlretrieve(url, video_path)

    tmp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    audio_path = tmp_audio.name

    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()
    os.remove(video_path)
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
    if is_youtube_url(video_url):
        audio_path = download_audio_youtube(video_url)
    else:
        audio_path = download_audio_direct(video_url)

    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    transcript = result["text"]
    os.remove(audio_path)

    lang = detect(transcript)
    if lang != 'en':
        return None

    accent, confidence = estimate_accent(transcript)
    return accent, confidence, transcript
