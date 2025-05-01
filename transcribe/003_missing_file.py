import os

def compare_folders(transcription_path, reference_path):
    try:
        # Get list of files in both folders
        transcription_files = set(f.split(".txt")[0] for f in os.listdir(transcription_path) if f.endswith(".txt"))
        reference_files = set(f.split(".txt")[0] for f in os.listdir(reference_path) if f.endswith(".txt"))
        
        # Find missing files
        missing_in_transcription = reference_files - transcription_files
        missing_in_reference = transcription_files - reference_files
        
        # Print results
        print("\n=== File Comparison Results ===")
        
        if missing_in_transcription:
            print("\nFiles missing in transcription folder:")
            for file in sorted(missing_in_transcription):
                print(f"- {file}")
        else:
            print("\nNo files missing in transcription folder")
            
        if missing_in_reference:
            print("\nFiles missing in reference folder:")
            for file in sorted(missing_in_reference):
                print(f"- {file}")
        else:
            print("\nNo files missing in reference folder")
            
        # Print matching files
        matching_files = transcription_files.intersection(reference_files)
        print(f"\nTotal matching files: {len(matching_files)}")
        print("\nMatching files:")
        for file in sorted(matching_files):
            print(f"- {file}")
            
        return matching_files
        
    except Exception as e:
        print(f"Error comparing folders: {str(e)}")
        return set()

if __name__ == "__main__":
    base_files_path = "../Files/data/"
    transcription_file_path = base_files_path + "transcription/"
    gt_text_folder_path = base_files_path + "text/"
    
    # Compare folders and get matching files
    matching_files = compare_folders(transcription_file_path, gt_text_folder_path)
