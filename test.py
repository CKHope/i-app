import os
from pydub import AudioSegment
import glob
import sys

# Fix encoding issue
sys.stdout.reconfigure(encoding='utf-8')

# Define the folder paths
input_folder = "./audio"
output_folder = "mp3output"
tripled_output_folder = "tripled_mp3output"
combined_output_file = "combined_tripled.mp3"

# Create the output and tripled output folders if they don't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

if not os.path.exists(tripled_output_folder):
    os.makedirs(tripled_output_folder)

# Step 1: Convert each .m4a file to .mp3
m4a_files = glob.glob(os.path.join(input_folder, "*.m4a"))

for m4a_file in m4a_files:
    # Load the audio file
    audio = AudioSegment.from_file(m4a_file, format="m4a")
    
    # Get the base filename without extension
    base_filename = os.path.splitext(os.path.basename(m4a_file))[0]
    
    # Set the output mp3 file path
    mp3_output_path = os.path.join(output_folder, f"{base_filename}.mp3")
    
    # Export the audio as mp3
    audio.export(mp3_output_path, format="mp3")
    
    print(f"Converted {m4a_file} to {mp3_output_path}")

# Step 2: Triple each .mp3 file and combine
mp3_files = glob.glob(os.path.join(output_folder, "*.mp3"))

for mp3_file in mp3_files:
    # Load the mp3 file
    audio = AudioSegment.from_file(mp3_file, format="mp3")
    
    # Triple the audio by concatenating it three times
    tripled_audio = audio + audio + audio
    
    # Set the tripled mp3 output file path
    base_filename = os.path.splitext(os.path.basename(mp3_file))[0]
    tripled_mp3_output_path = os.path.join(tripled_output_folder, f"{base_filename}_tripled.mp3")
    
    # Export the tripled audio as mp3
    tripled_audio.export(tripled_mp3_output_path, format="mp3")
    
    print(f"Tripled {mp3_file} and saved as {tripled_mp3_output_path}")

# Step 3: Combine all tripled mp3 files into a single file
combined_audio = AudioSegment.empty()

tripled_mp3_files = glob.glob(os.path.join(tripled_output_folder, "*.mp3"))

for tripled_mp3_file in tripled_mp3_files:
    # Load the tripled mp3 file
    audio = AudioSegment.from_file(tripled_mp3_file, format="mp3")
    
    # Append the audio to the combined_audio segment
    combined_audio += audio
    
    print(f"Added {tripled_mp3_file} to the combined audio")

# Export the combined audio as a single mp3 file
combined_audio.export(combined_output_file, format="mp3")

print(f"All tripled mp3 files have been combined into {combined_output_file}.")
