import streamlit as st
import os
import yt_dlp
import tempfile
from langdetect import detect
from faster_whisper import WhisperModel

st.title("🎙️ English Accent Detector")
st.write("Paste a public YouTube or MP4 URL and detect the English accent.")

@st.cache_resource
def load_model():
    return WhisperModel("base", device="cpu", compute_type="int8")

model = load_model()

def download_audio(url):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
        audio_path = tmp_audio.name

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    os.rename("downloaded_audio.wav", audio_path)
    return audio_path

def estimate_accent(text):
    text = text.lower()
    if "mate" in text or "g'day" in text:
        return "Australian", 85
    elif "gonna" in text or "wanna" in text or "gotta" in text:
        return "American", 80
    elif "shall" in text or "cheers" in text:
        return "British", 75
    else:
        return "Uncertain English", 60

url = st.text_input("Enter a YouTube or MP4 URL:")

if st.button("Analyze Accent") and url:
    try:
        st.info("Downloading and extracting audio...")
        audio_file = download_audio(url)

        st.success("Transcribing with Whisper...")
        segments, _ = model.transcribe(audio_file)
        transcript = "".join([seg.text for seg in segments])

        lang = detect(transcript)
        if lang != 'en':
            st.error("Detected language is not English.")
        else:
            accent, score = estimate_accent(transcript)
            st.subheader("Result")
            st.markdown(f"**Accent:** {accent}  \n**Confidence:** {score}%")
            st.markdown(f"**Transcript:** {transcript[:400]}...")

        os.remove(audio_file)
    except Exception as e:
        st.error(f"Error: {e}")
