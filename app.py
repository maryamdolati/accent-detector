import streamlit as st
from langdetect import detect
from accent_utils import run_accent_detection, estimate_accent

st.title("🎙️ Accent Detection from YouTube")
url = st.text_input("Enter a YouTube video URL")

if st.button("Analyze"):
    if url:
        with st.spinner("Processing..."):
            transcript = run_accent_detection(url)
            if detect(transcript) != "en":
                st.warning("Language is not English.")
            else:
                accent, conf = estimate_accent(transcript)
                st.success(f"Accent: {accent} ({conf}%)")
                st.text_area("Transcript", transcript[:500] + "...")
    else:
        st.warning("Please enter a URL.")
