
import subprocess
from pathlib import Path


def extract_audio(video_path: str, output_path: str) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        str(output),
    ]

    subprocess.run(command, check=True)

    print(f"Audio extracted: {output}")
