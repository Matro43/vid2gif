#!/usr/bin/env python3
"""vid2gif - convert a video to a GIF using ffmpeg."""
import argparse
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Convert a video to a GIF")
    parser.add_argument("input", help="input video file")
    parser.add_argument("output", help="output GIF file")
    parser.add_argument("--fps", type=int, default=12, help="frames per second")
    parser.add_argument("--width", type=int, default=480, help="GIF width in pixels")
    parser.add_argument("--start", default="0", help="start time (seconds)")
    parser.add_argument("--duration", default=None, help="length in seconds")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        sys.exit("Error: ffmpeg is not installed.")

    filters = (
        f"fps={args.fps},scale={args.width}:-1:flags=lanczos,"
        "split[a][b];[a]palettegen[p];[b][p]paletteuse"
    )
    cmd = ["ffmpeg", "-y", "-ss", args.start, "-i", args.input]
    if args.duration:
        cmd += ["-t", args.duration]
    cmd += ["-vf", filters, args.output]

    subprocess.run(cmd, check=True)
    print(f"Done: {args.output}")


if __name__ == "__main__":
    main()
