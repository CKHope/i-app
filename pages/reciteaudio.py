import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_audioclips
import os

# Streamlit App
st.title("MP4 Audio Tripling and Combining App")

# File Uploader to upload multiple files
uploaded_files = st.file_uploader("Choose MP4 files", accept_multiple_files=True, type=['mp4'])

if uploaded_files:
    # Button to start the process
    if st.button("Process and Combine Audio"):
        tripled_audio_clips = []
        st.write("Processing files...")

        for uploaded_file in uploaded_files:
            # Save the file temporarily
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.read())

            # Load the video file
            clip = VideoFileClip(uploaded_file.name)

            # Extract the audio
            audio = clip.audio

            # Triple the audio by concatenating it with itself 3 times
            tripled_audio = concatenate_audioclips([audio, audio, audio])

            # Append the tripled audio to the list
            tripled_audio_clips.append(tripled_audio)

            # Remove the temporarily saved file
            os.remove(uploaded_file.name)

        # Concatenate all the tripled audio clips into one final audio file
        final_audio_clip = concatenate_audioclips(tripled_audio_clips)

        # Output file name
        output_audio_file = "combined_audio_output.mp3"
        
        # Write the final audio to a file
        final_audio_clip.write_audiofile(output_audio_file)

        # Provide a download link for the final audio
        with open(output_audio_file, "rb") as file:
            st.download_button("Download Combined Audio", file, file_name=output_audio_file)

        # Close all clips to free memory
        for audio_clip in tripled_audio_clips:
            audio_clip.close()

        # Clean up the output file
        os.remove(output_audio_file)
        st.success("Audio processing complete!")
