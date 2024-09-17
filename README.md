# PyMKV2MP4

This is a Python script that converts MKV video files to MP4 format with no quality loss.
It utilizes **``ffmpeg``**, a powerful multimedia processing tool, to perform the conversion.
This script provides a simple and efficient way to convert video formats while preserving the original quality.

## Features
- Lossless Conversion: Converts MKV to MP4 without re-encoding, preserving the original quality.
- User-Friendly: Clear command-line interface with colored output for better readability.
- Error Handling: Graceful error reporting and handling.

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
