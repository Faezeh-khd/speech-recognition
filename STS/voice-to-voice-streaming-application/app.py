# To build a voice-to-voice streaming application with LLM support, you’ll follow the outlined steps, implementing each component using Python libraries and integrating the functionality. Below is a complete implementation in Python, which can be executed in a Jupyter notebook. This project will involve:

# 1.  Saving and playing voice created by Google Text-to-Speech (gTTS).
# 2.  Using a microphone to record voice.
# 3. Converting the recorded voice to text through speech-to-text (STT).
# 4. Converting the text to voice through text-to-speech (TTS).
# 5. Making a voice-to-voice stream.
# 6. Integrating an LLM to respond to voice input with voice output.
# 7. Building a web interface using Streamlit.


# pip install gtts pydub speech_recognition simpleaudio google-generativeai python-dotenv streamlit

import os
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
from IPython.display import Audio
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Path to store voice files
path = "../data/voice/"
os.makedirs(path, exist_ok=True)

# 1. Save and play voice created by Google Text-to-Speech (gTTS)
def text_to_audio(text, filename):
    tts = gTTS(text)
    file_path = os.path.join(path, filename)
    tts.save(file_path)
    return file_path

def play_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    play(audio)

# 2. Use microphone to record voice
def record_audio(duration=4):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"Recording for {duration} seconds...")
        recorded_audio = recognizer.listen(source, timeout=duration)
        print("Done recording.")
    return recorded_audio

# 3. Convert the recorded voice to text through speech-to-text (STT)
def audio_to_text(audio):
    recognizer = sr.Recognizer()
    try:
        print("Recognizing the text...")
        text = recognizer.recognize_google(audio, language="en-US")
        print("Decoded Text: {}".format(text))
    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand the audio."
    except sr.RequestError:
        text = "Could not request results from Google Speech Recognition service."
    return text

# 4. Convert the text to voice through text-to-speech (TTS)
def text_to_speech(text):
    tts = gTTS(text)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")
    play(audio_segment)

# 5. Make a voice-to-voice stream
def voice_to_voice():
    recorded_audio = record_audio()
    text = audio_to_text(recorded_audio)
    text_to_speech(text)

# 6. Integrate an LLM to respond to voice input with voice output
load_dotenv()
GOOGLE_API_KEY = "GOOGLE_API_KEY"
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
gemini_pro = genai.GenerativeModel(model_name="models/gemini-2.0-flash")


def respond_by_gemini(input_text, role_text, instructions_text):
    final_prompt = [
        "ROLE: " + role_text,
        "INPUT_TEXT: " + input_text,
        instructions_text,
    ]
    response = gemini_pro.generate_content(
        final_prompt,
        stream=True,
    )
    response_list = []
    for chunk in response:
        response_list.append(chunk.text)
    response_text = "".join(response_list)
    return response_text

def llm_voice_response():
    role = 'You are an intelligent assistant to chat on the topic: `{}`.'
    topic = 'The future of artificial intelligence'
    role_text = role.format(topic)
    instructions = 'Respond to the INPUT_TEXT briefly in chat style. Respond based on your knowledge about `{}` in brief chat style.'
    instructions_text = instructions.format(topic)
    
    recorded_audio = record_audio()
    text = audio_to_text(recorded_audio)
    response_text = text
    if text not in ["Google Speech Recognition could not understand the audio.", "Could not request results from Google Speech Recognition service."]:
        response_text = respond_by_gemini(text, role_text, instructions_text)
    text_to_speech(response_text)

# 7. Build a Web interface for the LLM-supported voice assistant
def main():
    # Streamlit setup with custom CSS
    st.set_page_config(page_title="LLM-Supported Voice Assistant", layout="wide")
    
    st.markdown("""
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .main {background-color: #f5f5f5;}
            .container {max-width: 800px; margin: auto; padding-top: 50px;}
            .title {font-family: 'Arial', sans-serif; color: #333333; margin-bottom: 30px;}
            .btn {background-color: #4CAF50; color: white; border: none; padding: 10px 20px; cursor: pointer; font-size: 16px;}
            .btn:hover {background-color: #45a049;}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='container'><h1 class='title'>LLM-Supported Voice Assistant</h1></div>", unsafe_allow_html=True)
    
    st.write("This is a voice assistant with LLM support. Speak to the microphone, and the assistant will respond.")
    
    if st.button("Record and Get Response", key="record_btn"):
        st.write("Listening...")
        llm_voice_response()
        st.write("Done.")
    
    st.markdown("<div class='container'><h5>Press the button and speak to the microphone. The assistant will generate a response based on the input and speak it out loud.</h5></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
    
    
# streamlit run app.py