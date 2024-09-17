import subprocess
import os
import sys

def check_file_exists(file_path):
    """Check if the specified file exists."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

def build_ffmpeg_command(input_file, output_file):
    """Construct the ffmpeg command to convert MKV to MP4 with no quality loss."""
    return [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-strict', 'experimental',
        output_file
    ]

def run_ffmpeg_command(command):
    """Execute the ffmpeg command and handle potential errors."""
    print(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Conversion completed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as error:
        print("Error during conversion:")
        print(error.stderr)

def convert_mkv_to_mp4(input_file, output_file):
    """Convert an MKV video to MP4 format with no quality loss."""
    check_file_exists(input_file)
    command = build_ffmpeg_command(input_file, output_file)
    run_ffmpeg_command(command)

def main():
    """Main function to handle script execution."""
    if len(sys.argv) != 3:
        print("Usage: python convert_mkv_to_mp4.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        convert_mkv_to_mp4(input_file, output_file)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
