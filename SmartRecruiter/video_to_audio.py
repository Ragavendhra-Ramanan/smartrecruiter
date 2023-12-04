import streamlit as st
from moviepy.editor import VideoFileClip
import soundfile as sf
from audio_to_text import convert_audio_to_text,generate_summary

# Streamlit app
def video_analyse():

    # Record audio and video
    video_file = st.file_uploader("Upload video file", type=["mp4", "avi", "mov"])

    if video_file:
        st.video(video_file, format="video/mp4", start_time=0)

        # Convert video to audio
        if st.button("Convert to Audio"):
            convert_video_to_audio(video_file)
#            st.audio(audio_data, format="audio/wav", start_time=0)

def convert_video_to_audio(video_file):
    # Save video file
    with open("temp_video.mp4", "wb") as f:
        f.write(video_file.getvalue())

    # Load video clip
    video_clip = VideoFileClip("temp_video.mp4")
    

    # Extract audio
    audio_data = video_clip.audio.to_soundarray()
    print(audio_data)
    sample_rate = video_clip.audio.fps

    # Save audio file
    sf.write("temp_audio.wav", audio_data, sample_rate)
    transcript=convert_audio_to_text("temp_audio.wav")
    st.write(f"{transcript}")
    generate_summary(transcript)





