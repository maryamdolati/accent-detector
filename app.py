import streamlit as st
from accent_utils import run_accent_detection

st.title("🎙️ English Accent Detector")
st.write("Paste a YouTube or direct video link below to detect the English accent.")

video_url = st.text_input("Enter Video URL")

if st.button("Analyze"):
    if video_url:
        with st.spinner("Processing..."):
            result = run_accent_detection(video_url)
            if result:
                accent, confidence, transcript = result
                st.success("✅ Accent Detected")
                st.markdown(f"**Accent:** {accent}")
                st.markdown(f"**Confidence:** {confidence}%")
                st.text_area("Transcript (Preview)", transcript[:300])
            else:
                st.error("The spoken language is not English.")
    else:
        st.warning("Please enter a video URL.")
