import os
import tempfile
import os, tempfile

from openai import OpenAI 

from envVars.env_vars import openaiKey
 

client = OpenAI(api_key=openaiKey)
 
 
def transcribe_audio_for_whisper(MODEL, LANGUAGE,TEMPERATURE,audio_file):
    try:
        if audio_file is None:
            print("************ No audio file received for transcribing ******************.")
        with open(audio_file, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model=MODEL,
                file=f,
                language=LANGUAGE,
                temperature=TEMPERATURE,
            )
            text = transcript.text.strip()
            return text
    except Exception as e:
        print(f"Error during transcription: {str(e)}")

def convert_to_dialogue(transcript):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts transcripts into dialogue format. Format the dialogue with clear speaker labels and proper punctuation."},
                {"role": "user", "content": f"Convert this transcript into a dialogue format with clear speaker labels:\n\n{transcript}"}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during dialogue conversion: {str(e)}")
        return None
 
 
MODEL =  'whisper-1'
LANGUAGE =  'en'
TEMP = 0.7

 
text = transcribe_audio_for_whisper(MODEL, LANGUAGE, TEMP, audio_file="../Files/data/audio/CAR0001.mp3")
print("************ Transcription completed ******************.\n", text)

# Convert to dialogue
dialogue = convert_to_dialogue(text)
print("\n************ Dialogue format ******************.\n", dialogue)

reference_text_file = "../Files/data/clean_text/CAR0001.txt"

with open(reference_text_file, "r") as file:
    reference_text = file.read()

print("\n************ Reference text ******************.\n", reference_text)
