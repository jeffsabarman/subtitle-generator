
import subprocess
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # script is in src/, so go up one level
FONTS_DIR = PROJECT_ROOT / "fonts"

VIDEO_W, VIDEO_H = 1080, 1920


def burn_subtitles(
    video_path: str,
    subtitle_path: str,
    output_path: str,
) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    subtitle = Path(subtitle_path).resolve().as_posix()

    # Escape characters that have special meaning in FFmpeg filters
    subtitle = subtitle.replace("\\", "\\\\")
    subtitle = subtitle.replace(":", "\\:")

    # video_height = 1920
    # safe_bottom_px = 480   # distance from the video bottom to the text's bottom edge
    # safe_side_px = 65

    # scale = 288 / video_height
    # margin_v = round(safe_bottom_px * scale)   # 72
    # margin_side = round(safe_side_px * scale)  # 10

    # style = {
    #     "Alignment": 2,            # bottom-center (legacy numbering)
    #     "FontName": "Sunny Brunch",
    #     "FontSize": 40,
    #     "PrimaryColour": "&H00FFFFFF&",
    #     "Outline": 0,
    #     "Shadow": 4,
    #     "BackColour": "&H4D000000&",
    #     "MarginV": margin_v,
    #     "MarginL": margin_side,
    #     "MarginR": margin_side,
    # }

    style = {
        "Alignment": 2,
        # "FontName": "Sunny Brunch",
        "FontName": "Tao Baso",
        "FontSize": 80,
        "PrimaryColour": "&H00FFFFFF&",
        "Outline": 0,
        "Shadow": 4,
        "BackColour": "&H4D000000&",
        "MarginV": 480,
        "MarginL": 65,
        "MarginR": 65,
    }

    # Join into "Key=Value,Key=Value,..."
    force_style = ",".join(f"{k}={v}" for k, v in style.items())
    def srt_to_ass(srt_path, ass_path, width, height):
        """Convert SRT to ASS and set the canvas to the real video size."""
        subprocess.run(["ffmpeg", "-y", "-i", str(srt_path), str(ass_path)], check=True)
        text = Path(ass_path).read_text(encoding="utf-8")
        text = re.sub(r"PlayResX:.*", f"PlayResX: {width}", text)
        text = re.sub(r"PlayResY:.*", f"PlayResY: {height}", text)
        Path(ass_path).write_text(text, encoding="utf-8")

    ass_file = Path(subtitle).with_suffix(".ass")
    srt_to_ass(subtitle, ass_file, VIDEO_W, VIDEO_H)

    vf = (
        # f"subtitles=filename={subtitle}"
        f"subtitles=filename={ass_file.as_posix()}"
        f":fontsdir={FONTS_DIR.as_posix()}"
        f":force_style='{force_style}'"
    )


    command = [
        str(Path("/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg")),
        "-y",
        "-i", video_path,
        # "-vf", f"subtitles=filename={subtitle}:fontsdir={FONTS_DIR.as_posix()}:force_style='Alignment={alignment},FontName={fontName},FontSize={fontSize}'",
        "-vf", vf,
        "-map", "0:v:0",
        "-map", "0:a:0",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_path,
    ]

    print("Running FFmpeg...")

    subprocess.run(command, check=True)

    print(f"Video exported: {output}")
