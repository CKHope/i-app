import os
from pydub import AudioSegment
import streamlit as st
import io
import glob

# Function to convert, triple, and combine audio files
def process_audio(uploaded_files):
    # Define folder paths
    output_folder = "mp3output"
    tripled_output_folder = "tripled_mp3output"
    combined_output_file = "combined_tripled.mp3"

    # Create the output and tripled output folders if they don't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if not os.path.exists(tripled_output_folder):
        os.makedirs(tripled_output_folder)

    combined_audio = AudioSegment.empty()
    
    for uploaded_file in uploaded_files:
        # Read the file
        audio = AudioSegment.from_file(uploaded_file, format="m4a")
        
        # Convert to mp3
        mp3_output_path = os.path.join(output_folder, f"{uploaded_file.name}.mp3")
        audio.export(mp3_output_path, format="mp3")
        
        # Triple the audio
        mp3_audio = AudioSegment.from_file(mp3_output_path, format="mp3")
        tripled_audio = mp3_audio + mp3_audio + mp3_audio
        
        # Save tripled audio
        tripled_mp3_output_path = os.path.join(tripled_output_folder, f"{uploaded_file.name}_tripled.mp3")
        tripled_audio.export(tripled_mp3_output_path, format="mp3")
        
        # Combine tripled audio
        tripled_audio_file = AudioSegment.from_file(tripled_mp3_output_path, format="mp3")
        combined_audio += tripled_audio_file

    # Export the combined audio
    combined_audio.export(combined_output_file, format="mp3")
    
    return combined_output_file

# Streamlit app
st.title("M4A to MP3 Conversion and Combining App")

st.write("Upload your M4A files here:")

# File uploader
uploaded_files = st.file_uploader("Choose M4A files", type=["m4a"], accept_multiple_files=True)

if uploaded_files:
    # Process files and show progress
    with st.spinner('Processing...'):
        combined_file = process_audio(uploaded_files)
    
    # Provide download link for the combined file
    with open(combined_file, "rb") as f:
        st.download_button(
            label="Download Combined MP3",
            data=f,
            file_name="combined_tripled.mp3",
            mime="audio/mp3"
        )
    
    st.success('Processing complete!')
