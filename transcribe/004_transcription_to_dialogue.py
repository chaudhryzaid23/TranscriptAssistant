import os

from openai import OpenAI

from envVars.env_vars import openaiKey


client = OpenAI(api_key=openaiKey)

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
    

def save_dialogue_to_file(dialogue, output_dir, filename):
    try:
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


score_list = []
for file in os.listdir("../Files/data/audio"):

    file_name = file.split(".")[0]

    print(f"************ Transcription to Dialogue for {file_name} ******************")
    transcribed_dialogue_file = transcription_file_path + file_name + ".txt"
    output_dialogue_file = out_dialogue_folder_path + file_name + ".txt"

    with open(transcribed_dialogue_file, "r") as file:
        print(f"************ Transcription for {file_name} ******************")
        transcribed_dialogue = file.read()
    
    dialogue = convert_to_dialogue(transcribed_dialogue)

    save_dialogue_to_file(dialogue, out_dialogue_folder_path, file_name + ".txt")
    
    
    