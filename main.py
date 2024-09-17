import subprocess
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_file_exists(file_path):
    """Check if the specified file exists."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

def build_ffmpeg_command(input_file, output_file, video_codec='copy', audio_codec='copy'):
    """Construct the ffmpeg command to convert MKV to MP4 with no quality loss."""
    return [
        'ffmpeg',
        '-i', input_file,
        '-c:v', video_codec,
        '-c:a', audio_codec,
        '-strict', 'experimental',
        output_file
    ]

def run_ffmpeg_command(command):
    """Execute the ffmpeg command and handle potential errors."""
    logger.info(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logger.info("Conversion completed successfully.")
        logger.debug(result.stdout)
    except subprocess.CalledProcessError as error:
        logger.error("Error during conversion:")
        logger.error(error.stderr)
        sys.exit(1)

def check_file_size(file_path):
    """Check if the file size is greater than 0."""
    if os.path.getsize(file_path) == 0:
        raise ValueError(f"File '{file_path}' is empty.")

def convert_mkv_to_mp4(input_file, output_file, video_codec='copy', audio_codec='copy'):
    """Convert an MKV video to MP4 format with no quality loss."""
    check_file_exists(input_file)
    command = build_ffmpeg_command(input_file, output_file, video_codec, audio_codec)
    run_ffmpeg_command(command)
    check_file_size(output_file)

def main():
    """Main function to handle script execution."""
    if len(sys.argv) not in [3, 5]:
        print("Usage: python convert_mkv_to_mp4.py <input_file> <output_file> [video_codec] [audio_codec]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    video_codec = sys.argv[3] if len(sys.argv) > 3 else 'copy'
    audio_codec = sys.argv[4] if len(sys.argv) > 4 else 'copy'

    try:
        convert_mkv_to_mp4(input_file, output_file, video_codec, audio_codec)
    except FileNotFoundError as e:
        logger.error(e)
        sys.exit(1)
    except ValueError as e:
        logger.error(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
