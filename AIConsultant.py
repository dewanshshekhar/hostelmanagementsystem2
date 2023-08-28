import openai
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import pydub.playback

# Set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"

# Initialize recognizer
recognizer = sr.Recognizer()

# Simulated database of responses
database = {
    "hello": "Hello! How can I assist you with your hostel inquiries?",
    "room": "We offer various room options, including single and shared rooms.",
    # Add more responses here
}

# Function to convert speech to text
def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("User:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
            return ""
        except sr.RequestError:
            print("Sorry, could not request results.")
            return ""

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text)
    tts.save("output.mp3")
    sound = AudioSegment.from_mp3("output.mp3")
    pydub.playback.play(sound)

# Function to get AI response from database or OpenAI model
def get_ai_response(message):
    if message in database:
        return database[message]
    else:
        # If not found in database, use OpenAI model
        messages = [{"role": "system", "content": "You are a Hostel Consultant for KR Mangalam University"}]
        messages.append({"role": 'user', "content": message})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages, temperature=0.5
        )
