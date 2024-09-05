import streamlit as st
from moviepy.editor import AudioFileClip, concatenate_audioclips
import os
import tempfile

# Streamlit App
st.title("M4A Audio Tripling and Combining App")

# File Uploader to upload multiple M4A files
uploaded_files = st.file_uploader("Choose M4A files", accept_multiple_files=True, type=['m4a'])

if uploaded_files:
    # Button to start the process
    if st.button("Process and Combine Audio"):
        tripled_audio_clips = []
        st.write("Processing files...")

        for uploaded_file in uploaded_files:
            # Create a temporary file to store the uploaded file content
            with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_file_path = tmp_file.name

            # Load the audio file from the temporary path
            audio_clip = AudioFileClip(temp_file_path)

            # Triple the audio by concatenating it with itself 3 times
            tripled_audio = concatenate_audioclips([audio_clip, audio_clip, audio_clip])

            # Append the tripled audio to the list
            tripled_audio_clips.append(tripled_audio)

            # Remove the temporary file
            os.remove(temp_file_path)

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
