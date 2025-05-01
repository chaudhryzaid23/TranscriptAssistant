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
                {"role": "user", "content": f"Convert this transcript into a dialogue format with clear speaker labels for both the speaker and the listener:\n\n{transcript}"}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during dialogue conversion: {str(e)}")
        return None

def compare_dialogues(transcribed_dialogue, reference_dialogue):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """You are a dialogue comparison expert. Compare the transcribed dialogue with the reference dialogue and provide:
                1. A score between 0-100 based on:
                   - Content accuracy (40%)
                   - Speaker identification accuracy (30%)
                   - Dialogue structure and flow (30%)
                2. A brief explanation of the score
                3. Key differences found
                Format your response as:
                Score: [number]
                Explanation: [brief explanation]
                Differences: [list key differences]"""},
                {"role": "user", "content": f"""Compare these two dialogues and provide a score and analysis:

Transcribed Dialogue:
{transcribed_dialogue}

Reference Dialogue:
{reference_dialogue}"""}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during dialogue comparison: {str(e)}")
        return None

def save_dialogue_to_file(dialogue, output_dir, filename):
    try:
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create full file path
        file_path = os.path.join(output_dir, filename)
        
        # Write dialogue to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(dialogue)
            
        print(f"\n************ Dialogue saved to {file_path} ******************")
    except Exception as e:
        print(f"Error saving dialogue to file: {str(e)}")
 
 
MODEL =  'whisper-1'
LANGUAGE =  'en'
TEMP = 0.7

 
text = transcribe_audio_for_whisper(MODEL, LANGUAGE, TEMP, audio_file="../Files/data/audio/RES0120.mp3")
# print("************ Transcription completed ******************.\n", text)

# Convert to dialogue
transcribed_dialogue = convert_to_dialogue(text)
print("\n************ Dialogue format ******************.\n", transcribed_dialogue)

reference_dialogue_file = "../Files/data/text/RES0120.txt"

with open(reference_dialogue_file, "r") as file:
    reference_dialogue = file.read()

# print("\n************ Reference dialogue ******************.\n", reference_dialogue)

# Compare and grade the dialogues
comparison_result = compare_dialogues(transcribed_dialogue, reference_dialogue)
print("\n************ Comparison Results ******************.\n", comparison_result)

# Save transcribed dialogue to file
output_dir = "../Files/data/transcription"
filename = "RES0120.txt"
save_dialogue_to_file(transcribed_dialogue, output_dir, filename)
