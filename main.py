#!/usr/bin/env python3
"""Convert MKV files to MP4 using ffmpeg."""

import argparse
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


class UserError(Exception):
    """Expected errors that should be reported cleanly to the user."""


def _color(text: str, code: str) -> str:
    if os.environ.get("NO_COLOR") or not sys.stdout.isatty():
        return text
    return f"\033[{code}m{text}\033[0m"


def _red(text: str) -> str:
    return _color(text, "31")


def _green(text: str) -> str:
    return _color(text, "32")


def _yellow(text: str) -> str:
    return _color(text, "33")


def locate_ffmpeg(path: Path | None) -> Path:
    if path is not None:
        if path.is_file():
            return path
        raise UserError(f"ffmpeg not found at specified path: {path}")
    exe = shutil.which("ffmpeg")
    if exe is None:
        raise UserError(
            "ffmpeg not found in PATH. Install ffmpeg or use --ffmpeg-path."
        )
    return Path(exe)


def ensure_input_valid(path: Path) -> None:
    if not path.exists():
        raise UserError(f"Input file not found: {path}")
    if not path.is_file():
        raise UserError(f"Not a file: {path}")
    if path.suffix.lower() != ".mkv":
        logger.warning(
            "Input lacks .mkv extension (%s); continuing anyway", path.suffix
        )


def ensure_output_valid(path: Path, overwrite: bool) -> None:
    if path.exists():
        if overwrite:
            logger.warning("Overwriting: %s", path)
        else:
            raise UserError(f"Output exists: {path} (use -y to overwrite)")
    if not path.parent.exists():
        raise UserError(f"Output directory does not exist: {path.parent}")


def build_ffmpeg_cmd(
    ffmpeg: Path,
    src: Path,
    dst: Path,
    vcodec: str,
    acodec: str,
    scodec: str | None,
    overwrite: bool,
) -> list[str]:
    cmd = [str(ffmpeg), "-hide_banner"]
    if overwrite:
        cmd.append("-y")
    cmd.extend(["-i", str(src)])
    cmd.extend(["-c:v", vcodec])
    cmd.extend(["-c:a", acodec])
    if scodec is None:
        cmd.append("-sn")
    else:
        cmd.extend(["-c:s", scodec])
    cmd.extend(["-map_metadata", "0", "-map_chapters", "0"])
    cmd.append(str(dst))
    return cmd


def execute(cmd: list[str], quiet: bool) -> None:
    logger.debug("Command: %s", " ".join(cmd))
    if quiet:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise UserError(f"ffmpeg failed:\n{result.stderr}")
        return
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        raise UserError(f"ffmpeg exited with code {exc.returncode}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pymkv2mp4",
        description="Convert MKV to MP4. "
        "Streams are copied by default without re-encoding.",
    )
    parser.add_argument("input", type=Path, help="Input MKV file")
    parser.add_argument("output", type=Path, help="Output MP4 file")
    parser.add_argument(
        "-v",
        "--video-codec",
        default="copy",
        metavar="CODEC",
        help="Video codec (default: copy)",
    )
    parser.add_argument(
        "-a",
        "--audio-codec",
        default="copy",
        metavar="CODEC",
        help="Audio codec (default: copy)",
    )
    parser.add_argument(
        "-s",
        "--subtitle-codec",
        default="copy",
        metavar="CODEC",
        help="Subtitle codec. Use 'none' to strip (default: copy)",
    )
    parser.add_argument(
        "-y", "--overwrite", action="store_true", help="Overwrite output without prompting"
    )
    parser.add_argument(
        "-n", "--dry-run", action="store_true", help="Print the ffmpeg command and exit"
    )
    parser.add_argument(
        "--ffmpeg-path", type=Path, metavar="PATH", help="Path to ffmpeg executable"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")

    args = parser.parse_args(argv)

    if args.quiet and args.verbose:
        parser.error("--quiet and --verbose are mutually exclusive")

    level = (
        logging.DEBUG
        if args.verbose
        else logging.WARNING
        if args.quiet
        else logging.INFO
    )
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    try:
        ffmpeg = locate_ffmpeg(args.ffmpeg_path)
        ensure_input_valid(args.input)
        ensure_output_valid(args.output, args.overwrite)

        sub = None if args.subtitle_codec.lower() == "none" else args.subtitle_codec

        cmd = build_ffmpeg_cmd(
            ffmpeg,
            args.input,
            args.output,
            args.video_codec,
            args.audio_codec,
            sub,
            args.overwrite,
        )

        if args.dry_run:
            print(" ".join(cmd))
            return 0

        execute(cmd, args.quiet)
        print(_green(f"Converted: {args.output}"))
        return 0

    except UserError as exc:
        print(_red(f"Error: {exc}"), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print(_yellow("\nInterrupted"), file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
