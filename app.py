# app.py
import streamlit as st
import os
import tempfile
from langdetect import detect

st.title("🎙️ English Accent Detector (Demo Mode)")
st.write("Paste a public video URL (YouTube or MP4), and get a simulated English accent classification.")

# Simulated accent detection based on fake transcript (no Whisper)
def fake_transcribe():
    return "Here's how to upload YouTube Shorts from your PC. Let's go. First, head to youtube.com..."

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
        st.success("Simulating transcription...")
        transcript = fake_transcribe()

        lang = detect(transcript)
        if lang != 'en':
            st.error("Detected language is not English.")
        else:
            accent, score = estimate_accent(transcript)
            st.subheader("Result")
            st.markdown(f"**Accent:** {accent}  \n**Confidence:** {score}%")
            st.markdown(f"**Transcript:** {transcript[:400]}...")

    except Exception as e:
        st.error(f"Error: {e}")
