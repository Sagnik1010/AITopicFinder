import os
import re
import subprocess

# Ensure output folder exists
os.makedirs("audios", exist_ok=True)

# List of video files (you can also use os.listdir("videos") if all are in 'videos/')
video_files = [
    'Arrays Introduction Java Complete Placement Course Lecture #10 [].mp4',
    'Basics of Time Complexity and Space Complexity Java #2 [].mp4',
    'Conditional Statements  If else, Switch Break  Complete Java Placement Course  #3 [].mp4',
    'Functions Methods Java Complete Placement Course Lecture #4 [].mp4',
    'Introduction to Java Language #1 [].mp4',
    'Loops in Java  Placement Full Course Lecture  #5 [].mp4',
    'Sorting in Java Bubble Sort Selection Sort Insertion #6 [].mp4',
    'Strings Lecture #12 [].mp4',
    'videoplayback  #7 [].mp4'
]

for file in video_files:
    # Try to extract lecture/tutorial number using regex
    match = re.search(r"#(\d+)", file)
    tutorial_number = match.group(1) if match else "unknown"

    # Clean filename: remove [] and extra symbols, replace spaces with underscores
    clean_name = re.sub(r"[\[\]#]", "", file)   # remove [] and #
    clean_name = os.path.splitext(clean_name)[0]  # remove .mp4
    clean_name = "_".join(clean_name.split())     # replace spaces with underscores

    # Output mp3 filename
    output_file = f"audios/{tutorial_number}_{clean_name}.mp3"

    # Run ffmpeg
    subprocess.run([
        "ffmpeg",
        "-i", f"videos/{file}",
        "-q:a", "0",   # best audio quality
        "-map", "a",    # only extract audio
        output_file
    ])

    print(f"✅ Converted: {file} → {output_file}")
