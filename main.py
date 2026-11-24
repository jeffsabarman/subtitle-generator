
import json
from pathlib import Path

from src.audio import extract_audio
from src.transcribe import transcribe_audio
from src.subtitles import group_words
from src.srt import generate_srt
from src.video import burn_subtitles

# To update
INDEX = 23


# VIDEO_PATH = "input/test_subs.mp4"
VIDEO_PATH = f"input/{INDEX}/temp.mp4"
AUDIO_PATH = f"output/{INDEX}/audio.wav"
TRANSCRIPT_PATH = f"output/{INDEX}/transcript.json"
RESULT_PATH = f"output/{INDEX}/result.mp4"
SUBTITLE_PATH = f"output/{INDEX}/subtitles.srt"
# SUBS_JSON_PATH = "output/{INDEX}/subtitles.json"

def generate_subs():
    # Step 1: Extract audio
    extract_audio(VIDEO_PATH, AUDIO_PATH)

    # Step 2: Transcribe and align
    result = transcribe_audio(AUDIO_PATH)

    print(">>>>>>>>>>>> AFTER TRANSCRIBE AUDIO <<<<<<<<<<<")

    # Step 4: Group words into subtitles
    subtitles = group_words(result)

    # Step 5: Save subtitle segments
    # with open("output/subtitles.json", "w", encoding="utf-8") as file:
    with open(TRANSCRIPT_PATH, "w", encoding="utf-8") as file:
        json.dump(subtitles, file, indent=2, ensure_ascii=False)

    print(f"Transcript saved: {TRANSCRIPT_PATH}")
    print("Subtitles generated!")

    # Step 6: Generate SRT file
    srt_content = generate_srt(subtitles)

    with open(SUBTITLE_PATH, "w", encoding="utf-8") as file:
        file.write(srt_content)

    print(f"SRT file generated: {SUBTITLE_PATH}")


def main():
    Path(f"output/{INDEX}").mkdir(exist_ok=True)

    # generate_subs()
    # print("\n"*5)
    # print(">>>>>>>>> SUBSSSS SRT GENERATED <<<<<<<<<")

    # Step 7: Burn subtitles into video
    burn_subtitles(
        VIDEO_PATH,
        SUBTITLE_PATH,
        RESULT_PATH,
    )


if __name__ == "__main__":
    main()
