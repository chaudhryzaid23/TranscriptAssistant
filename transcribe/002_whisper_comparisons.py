import os
import tempfile
import os, tempfile
import statistics

from openai import OpenAI 

from envVars.env_vars import openaiKey
 

client = OpenAI(api_key=openaiKey)

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
    

def save_comparison_to_file(comparison, output_dir, filename):
    try:
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create full file path
        file_path = os.path.join(output_dir, filename)
        
        # Write dialogue to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(comparison)
            
        print(f"\n************ Comparison saved to {file_path} ******************")
    except Exception as e:
        print(f"Error saving comparison to file: {str(e)}")
 
 
MODEL =  'whisper-1'
LANGUAGE =  'en'
TEMP = 0.7


base_files_path = "../Files/data/"

transcription_file_path = base_files_path + "transcription/"
gt_text_folder_path = base_files_path + "text/"


score_list = []
for file in os.listdir("../Files/data/audio"):

    file_name = file.split(".")[0]
 
    transcribed_dialogue_file = transcription_file_path + f"{file_name}_transcribed_dialogue.txt"
    reference_dialogue_file = gt_text_folder_path + file_name + ".txt"

    with open(transcribed_dialogue_file, "r") as file:
        transcribed_dialogue = file.read()


    with open(reference_dialogue_file, "r") as file:
        reference_dialogue = file.read()

    # Compare and grade the dialogues
    comparison_result = compare_dialogues(transcribed_dialogue, reference_dialogue)
    print("\n************ Comparison Results ******************.\n", comparison_result)

    # Save transcribed dialogue to file
    output_dir = "../Files/data/comparisons"
    filename = "CAR0001_comparison_results.txt"
    save_comparison_to_file(comparison_result, output_dir, filename)

    score = int(comparison_result.split("Score: ")[1].split("\n")[0])
    print("\n************ Score ******************.\n", score)

    score_list.append(score)

# Calculate statistics
avg_score = statistics.mean(score_list)
std_dev = statistics.stdev(score_list) if len(score_list) > 1 else 0

# Save scores and statistics to file
with open("score_list.txt", "w") as file:
    for score in score_list:
        file.write(f"{score}\n")
    file.write("\n=== Statistics ===\n")
    file.write(f"Average Score: {avg_score:.2f}\n")
    file.write(f"Standard Deviation: {std_dev:.2f}\n")

