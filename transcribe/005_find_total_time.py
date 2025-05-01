import os
from pydub import AudioSegment
from datetime import timedelta

def get_audio_duration(file_path):
    try:
        audio = AudioSegment.from_mp3(file_path)
        return len(audio) / 1000.0  # Convert milliseconds to seconds
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return 0

def format_time(seconds):
    return str(timedelta(seconds=int(seconds)))

def main():
    audio_folder = "../Files/data/audio"
    total_duration = 0
    file_durations = []
    
    print("\n=== Audio Duration Analysis ===")
    
    # Process each MP3 file
    for filename in os.listdir(audio_folder):
        if filename.endswith(".mp3"):
            file_path = os.path.join(audio_folder, filename)
            duration = get_audio_duration(file_path)
            total_duration += duration
            file_durations.append((filename, duration))
    
    # Sort files by duration
    file_durations.sort(key=lambda x: x[1], reverse=True)
    
    # Print results
    print(f"\nTotal number of MP3 files: {len(file_durations)}")
    print(f"Total duration: {format_time(total_duration)}")
    print(f"Average duration per file: {format_time(total_duration/len(file_durations))}")
    
    print("\nTop 5 longest files:")
    for filename, duration in file_durations[:5]:
        print(f"- {filename}: {format_time(duration)}")
    
    print("\nTop 5 shortest files:")
    for filename, duration in file_durations[-5:]:
        print(f"- {filename}: {format_time(duration)}")

if __name__ == "__main__":
    main()
