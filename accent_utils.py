import os
import tempfile
import urllib.request
import whisper
import torchaudio
from langdetect import detect

import urllib.request
import tempfile
from moviepy.editor import VideoFileClip

def download_audio_direct(url):
    # دانلود فایل ویدیویی
    tmp_video = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    video_path = tmp_video.name
    urllib.request.urlretrieve(url, video_path)

    # استخراج صدا با moviepy و ذخیره به wav
    tmp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    audio_path = tmp_audio.name
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)

    clip.close()
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
    audio_path = download_audio_direct(video_url)
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    transcript = result["text"]
    lang = detect(transcript)

    os.remove(audio_path)

    if lang != 'en':
        return None

    accent, confidence = estimate_accent(transcript)
    return accent, confidence, transcript
