import streamlit as st
from pydub import AudioSegment
import os
import tempfile

# Streamlit App
st.title("M4A Audio Tripling and Combining App (Online with ffmpeg-python)")

# File Uploader to upload multiple M4A files
uploaded_files = st.file_uploader("Choose M4A files", accept_multiple_files=True, type=['m4a'])

if uploaded_files:
    # Button to start the process
    if st.button("Process and Combine Audio"):
        combined_audio = AudioSegment.empty()  # Initialize an empty audio segment
        st.write("Processing files...")

        for uploaded_file in uploaded_files:
            # Create a temporary file to store the uploaded file content
            with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_file_path = tmp_file.name

            # Load the audio file from the temporary path using pydub and ffmpeg
            audio = AudioSegment.from_file(temp_file_path, format="m4a")

            # Triple the audio by concatenating it with itself 3 times
            tripled_audio = audio + audio + audio

            # Append the tripled audio to the combined audio
            combined_audio += tripled_audio

            # Remove the temporary file
            os.remove(temp_file_path)

        # Output file name
        output_audio_file = "combined_audio_output.mp3"

        # Export the final combined audio to an mp3 file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_out_file:
            combined_audio.export(tmp_out_file.name, format="mp3")
            output_audio_file = tmp_out_file.name

        # Provide a download link for the final audio
        with open(output_audio_file, "rb") as file:
            st.download_button("Download Combined Audio", file, file_name="combined_audio_output.mp3")

        # Clean up the output file
        os.remove(output_audio_file)
        st.success("Audio processing complete!")
