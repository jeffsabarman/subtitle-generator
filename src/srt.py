import re 

def format_timestamp(seconds: float) -> str:
    milliseconds = round(seconds * 1000)

    hours = milliseconds // 3_600_000
    milliseconds %= 3_600_000

    minutes = milliseconds // 60_000
    milliseconds %= 60_000

    seconds = milliseconds // 1000
    milliseconds %= 1000

    return (
        f"{hours:02}:"
        f"{minutes:02}:"
        f"{seconds:02},"
        f"{milliseconds:03}"
    )


# def generate_srt(subtitles: list) -> str:
#     entries = []

#     for index, subtitle in enumerate(subtitles, start=1):
#         start = format_timestamp(subtitle["start"])
#         end = format_timestamp(subtitle["end"])
#         text = subtitle["text"]

#         entry = (
#             f"{index}\n"
#             f"{start} --> {end}\n"
#             f"{text}"
#         )

#         entries.append(entry)
    
#     return "\n\n".join(entries) + "\n"

# def generate_srt(subtitles: list) -> str:
#     entries = []
#     index = 1

#     for subtitle in subtitles:
#         text = subtitle["text"]

#         # Skip the series introduction
#         if "Welcome to my series" in text:
#             continue

#         # Skip "Around London" but retain "where I'm on"
#         if "Around London" in text:
#             words = subtitle["words"]

#             where_word = next(
#                 (
#                     word for word in words
#                     if word["word"].strip().lower() == "where"
#                 ),
#                 None,
#             )

#             if where_word:
#                 subtitle_start = where_word["start"]

#                 # Remove everything before "where"
#                 text = " ".join(
#                     word["word"].strip()
#                     for word in words[
#                         words.index(where_word):
#                     ]
#                 )
#             else:
#                 continue
#         else:
#             subtitle_start = subtitle["start"]

#         start = format_timestamp(subtitle_start)
#         end = format_timestamp(subtitle["end"])

#         entry = (
#             f"{index}\n"
#             f"{start} --> {end}\n"
#             f"{text}"
#         )

#         entries.append(entry)
#         index += 1

#     return "\n\n".join(entries) + "\n"

def generate_srt(subtitles: list) -> str:
    entries = []
    index = 1

    final_subtitles = []

    for subtitle in subtitles:
        text = subtitle["text"]

        # Skip the series introduction
        if "Welcome to my series" in text:
            continue

        # Remove "Around London" but retain "where I'm on"
        start = subtitle["start"]

        if "Around London" in text:
            words = subtitle["words"]

            where_index = next(
                (
                    i for i, word in enumerate(words)
                    if word["word"].strip().lower() == "where"
                ),
                None,
            )

            if where_index is None:
                continue

            start = words[where_index]["start"]
            text = " ".join(
                word["word"].strip()
                for word in words[where_index:]
            )

        final_subtitles.append({
            "start": start,
            "end": subtitle["end"],
            "text": text,
        })

    # Merge subtitles containing only one word into the previous subtitle
    merged_subtitles = []

    for subtitle in final_subtitles:
        if len(subtitle["text"].split()) == 1 and merged_subtitles:
            merged_subtitles[-1]["text"] += " " + subtitle["text"]
            merged_subtitles[-1]["end"] = subtitle["end"]
        else:
            merged_subtitles.append(subtitle.copy())

    # Generate final SRT
    for subtitle in merged_subtitles:
        # Remove punctuation from final subtitle text
        # text = re.sub(r"[^\w\s']", "", subtitle["text"])
        # Remove period from final subtitle text
        text = subtitle["text"].replace(".", "")

        start = format_timestamp(subtitle["start"])
        end = format_timestamp(subtitle["end"])

        entry = (
            f"{index}\n"
            f"{start} --> {end}\n"
            f"{text}"
        )

        entries.append(entry)
        index += 1

    return "\n\n".join(entries) + "\n"

