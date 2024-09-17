# PyMKV2MP4

This is a Python script that converts MKV video files to MP4 format with no quality loss.
It utilizes **``ffmpeg``**, a powerful multimedia processing tool, to perform the conversion.
This script provides a simple and efficient way to convert video formats while preserving the original quality.

## Features
- Lossless Conversion: Converts MKV to MP4 without re-encoding, preserving the original quality.
- User-Friendly: Clear command-line interface with colored output for better readability.
- Error Handling: Graceful error reporting and handling.

## Codec Options
By default, the script uses the ``copy`` codec for both video and audio, meaning that no re-encoding occurs.
However, you can specify different video and audio codecs as needed.

## Supported Video Codecs
- ``copy``: Directly copies the video stream without re-encoding (lossless).
- ``libx264``: Popular for MP4 output; provides excellent compression while maintaining quality.
- ``libx265``: More efficient compression compared to libx264, but may require more processing power.
- ``mpeg4``: An older codec, but compatible with many devices.

## Supported Audio Codecs

- ``copy``: Directly copies the audio stream without re-encoding (lossless).
- ``aac``: Commonly used with MP4 files and provides good quality at lower bitrates.
- ``mp3``: Widely compatible, but lower quality compared to AAC for the same bitrate.
- ``ac3``: Often used for surround sound systems (Dolby Digital).

## Advanced Usage with Codec Options
You can specify custom video and audio codecs when running the script. For example:

```shell
python main.py <input_file> <output_file> <video_codec> <audio_codec>
```

## Example 1: Use libx264 for video and aac for audio
```shell
python main.py /home/test/file.mkv /home/test/file.mp4 libx264 aac
```

## Example 2: Use copy for both video and audio (default behavior)
```shell
python main.py /home/test/file.mkv /home/test/file.mp4 copy copy
```

## Example 3: Use libx265 for video and mp3 for audio
```shell
python main.py /home/test/file.mkv /home/test/file.mp4 libx265 mp3
```

## Example 4: Use mpeg4 for video and ac3 for audio
```shell
python main.py /home/test/file.mkv /home/test/file.mp4 mpeg4 ac3
```

In each case, replace the placeholders **``<input_file>``**, **``<output_file>``**, **``<video_codec>``**, and **``<audio_codec>``** with the appropriate file paths and codec names.

## Requirements
- **``Python 3.x``**: Make sure you have **``Python3.x``** installed.
- **``ffmpeg``**: The script relies on **``ffmpeg``** for video processing.

## Installation
1. Clone the Repository:
```shell
git clone https://github.com/dragonGR/PyMKV2MP4.git
cd PyMKV2MP4
```
Ensure **``ffmpeg``** is installed on your system.

## Usage
To convert an MKV video file to MP4, use the following command:
```shell
python main.py <input_file> <output_file>
```

Replace **``<input_file>``** with the path to your MKV file and **``<output_file>``** with the desired path for the MP4 output.

## Example
```shell
python main.py /home/test/file.mkv /home/test/file.mp4
```
