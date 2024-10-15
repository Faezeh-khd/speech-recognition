from google.colab import files

# Upload an audio file
uploaded = files.upload()

# List uploaded files (ensure it's a .wav file)
for filename in uploaded.keys():
    print(f'Uploaded file: {filename}')



import subprocess

# Define the model, scorer, and audio file paths
model_path = "deepspeech-0.9.3-models.pbmm"
scorer_path = "deepspeech-0.9.3-models.scorer"
audio_file = "audio.wav"  # Use the resampled audio file

# Run the DeepSpeech inference
output = subprocess.run(['deepspeech', '--model', model_path, '--scorer', scorer_path, '--audio', audio_file],
                        capture_output=True, text=True)

# Print the transcribed text
print("Transcription: ", output.stdout)
