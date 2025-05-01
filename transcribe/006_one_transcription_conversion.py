import os

from openai import OpenAI

from envVars.env_vars import openaiKey


client = OpenAI(api_key=openaiKey)

def convert_to_dialogue(transcript):
    print("Converting transcript to dialogue")
    if not transcript or not isinstance(transcript, str):
        print("Error: Invalid transcript input")
        return None
        
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts transcripts into dialogue format. Format the dialogue with clear speaker labels and proper punctuation."},
                {"role": "user", "content": f"Convert this transcript into a dialogue format with clear speaker labels for both the speaker and the listener:\n\n{transcript}"}
            ],
            temperature=0.7
        )

        dialogue = response.choices[0].message.content.strip()
        if not dialogue:
            print("Error: Empty dialogue generated")
            return None
            
        print("Dialogue converted successfully")
        return dialogue
        
    except Exception as e:
        print(f"Error during dialogue conversion: {str(e)}")
        return None
    

def save_dialogue_to_file(dialogue, output_dir, filename):
    try:
        if not dialogue or not isinstance(dialogue, str):
            print("Error: Invalid dialogue input")
            return
            
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        print("Saving dialogue to file")
        # Create full file path
        file_path = os.path.join(output_dir, filename)
        
        # Write dialogue to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(dialogue)
            
        print(f"\n************ Transcription to Dialogue saved to {file_path} ******************")
    except Exception as e:
        print(f"Error saving transcription to dialogue to file: {str(e)}")
    

base_files_path = "../Files/data/"

transcription_file_path = base_files_path + "transcription/"
out_dialogue_folder_path = base_files_path + "outputdialogue/"


file_name = "CAR0001"

print(f"************ Transcription to Dialogue for {file_name} ******************")
transcribed_dialogue_file = transcription_file_path + file_name + ".txt"
output_dialogue_file = out_dialogue_folder_path + file_name + ".txt"

try:
    with open(transcribed_dialogue_file, "r") as file:
        print(f"************ Reading transcription for {file_name} ******************")
        transcribed_dialogue = file.read()
        
        if not transcribed_dialogue:
            print(f"Error: Empty transcription file for {file_name}")
            
        # Convert to dialogue
        dialogue = convert_to_dialogue(transcribed_dialogue)
        if dialogue:
            save_dialogue_to_file(dialogue, out_dialogue_folder_path, file_name + ".txt")
        else:
            print(f"Error: Failed to convert transcription to dialogue for {file_name}")
            
except Exception as e:
    print(f"Error processing file {file_name}: {str(e)}")
    
    
    