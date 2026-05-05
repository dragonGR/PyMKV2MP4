# PyMKV2MP4

A lightweight, zero-dependency Python CLI that converts MKV video files to MP4 format using **ffmpeg**. By default, both video and audio streams are **copied without re-encoding**, meaning the output is visually identical to the source and the conversion is near-instant.

This tool provides a reliable wrapper around ffmpeg with sensible defaults, robust error handling, and a clean command-line interface.

---

## Features

*   **Lossless by Default**: Copies video and audio streams directly. No quality degradation, no waiting for re-encoding.
*   **Smart Validation**: Checks for files, directories, and ffmpeg availability before execution.
*   **Flexible Codecs**: Override the default `copy` behavior with any ffmpeg-supported video or audio codec.
*   **Subtitle Control**: Copy, re-encode, or strip subtitle tracks entirely.
*   **Dry-Run Mode**: Preview the exact ffmpeg command before executing it.
*   **Overwrite Protection**: Prevents accidental data loss unless explicitly allowed with `-y`.
*   **Portable**: Built with the Python standard library. No `pip install` required.

---

## Requirements

| Dependency | Minimum Version | Notes |
| :--- | :--- | :--- |
| **Python** | 3.10+ | Uses modern union syntax (`|`) and `pathlib` |
| **ffmpeg** | 4.4+ | Must be in system `PATH` or specified manually |

### Checking your environment

```bash
# Verify Python
python3 --version

# Verify ffmpeg
ffmpeg -version | head -n 1
```

If **ffmpeg** is missing, install it via your package manager:
*   **Ubuntu/Debian**: `sudo apt install ffmpeg`
*   **macOS**: `brew install ffmpeg`
*   **Windows**: `winget install Gyan.FFmpeg`
*   **Arch**: `sudo pacman -S ffmpeg`

---

## Installation & Usage

Just clone the repository and run the script. No external Python packages are needed.

```bash
git clone https://github.com/dragonGR/PyMKV2MP4.git
cd PyMKV2MP4

# Optional: make executable on Linux/macOS
chmod +x main.py

# Basic usage
python main.py <input.mkv> <output.mp4> [options]
```

### Arguments

| Argument | Description |
| :--- | :--- |
| `input` | Path to the source MKV file. |
| `output` | Path where the MP4 file will be written. |

### Optional Flags

| Flag | Default | Description |
| :--- | :--- | :--- |
| `-v, --video-codec` | `copy` | Video codec to use. `copy` passes the stream through unchanged. |
| `-a, --audio-codec` | `copy` | Audio codec to use. |
| `-s, --subtitle-codec` | `copy` | Subtitle codec. Use `none` to remove subtitles. |
| `-y, --overwrite` | `False` | Overwrite the output file if it already exists. |
| `-n, --dry-run` | `False` | Print the generated ffmpeg command and exit. |
| `--ffmpeg-path` | `None` | Full path to the ffmpeg binary if not in your PATH. |
| `--verbose` | `False` | Enable debug-level logging. |
| `--quiet` | `False` | Suppress ffmpeg progress output. |

---

## Common Use Cases

### 1. Lossless Conversion (Default)
The fastest option. Video, audio, and subtitle streams are copied directly.
```bash
python main.py film.mkv film.mp4
```

### 2. Re-encode for Compatibility
Use this if the source codecs are not MP4-compatible (e.g., MPEG-2 video or DTS audio).
```bash
python main.py film.mkv film.mp4 -v libx264 -a aac
```

### 3. Hardware Acceleration
If your hardware supports it, you can significantly speed up re-encoding:
```bash
# NVIDIA GPU
python main.py film.mkv film.mp4 -v h264_nvenc

# Apple Silicon
python main.py film.mkv film.mp4 -v videotoolbox
```

### 4. Handling Subtitle Errors
Many MKVs use **PGS** subtitles which aren't supported in MP4. Either strip them or convert them to text-based format:
```bash
# Strip subtitles
python main.py film.mkv film.mp4 -s none

# Convert to MP4-compatible text
python main.py film.mkv film.mp4 -s mov_text
```

---

## Supported Codecs (Examples)

| Category | Codec | Description |
| :--- | :--- | :--- |
| **Video** | `copy` | Default. No quality loss, instant. |
| | `libx264` | H.264 / AVC. High compatibility. |
| | `libx265` | H.265 / HEVC. Better compression. |
| **Audio** | `copy` | Direct stream copy. |
| | `aac` | Standard for MP4. |
| | `ac3` | Dolby Digital. Good for surround sound. |
| **Subtitles**| `none` | Removes all subtitle tracks. |
| | `mov_text` | Standard MP4 subtitle format. |

---

## Troubleshooting

*   **"Subtitle codec ... is not supported"**: MP4 is stricter than MKV. Use `-s none` to remove them or `-s mov_text` to convert them.
*   **File not found**: Ensure your paths are correct. If using Windows, wrap paths in quotes if they contain spaces.
*   **Exit Code 1**: Check the output for error messages. This usually indicates a codec mismatch or a missing ffmpeg installation.
*   **No Color**: If your terminal doesn't support ANSI colors, set the environment variable `NO_COLOR=1`.
