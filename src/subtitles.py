# def group_words(
#     transcript: dict,
#     max_chars: int = 42,
#     max_duration: float = 2.5,
#     pause_threshold: float = 0.45,
# ):
#     words = transcript.get("word_segments", [])

#     subtitles = []
#     current_words = []

#     def save_group():
#         if not current_words:
#             return

#         subtitles.append({
#             "start": current_words[0]["start"],
#             "end": current_words[-1]["end"],
#             "text": " ".join(
#                 word["word"] for word in current_words
#             ).strip()
#         })

#         current_words.clear()

#     for word in words:
#         if not current_words:
#             current_words.append(word)
#             continue

#         previous = current_words[-1]

#         current_text = " ".join(
#             item["word"] for item in current_words
#         )

#         candidate_text = f"{current_text} {word['word']}"

#         pause = word["start"] - previous["end"]
#         duration = word["end"] - current_words[0]["start"]

#         sentence_finished = previous["word"].endswith(
#             (".", "?", "!")
#         )

#         should_split = (
#             len(candidate_text) > max_chars
#             or duration > max_duration
#             or pause > pause_threshold
#             or sentence_finished
#         )

#         if should_split:
#             save_group()

#         current_words.append(word)

#     save_group()

#     return subtitles


def group_words(
    transcript: dict,
    max_words: int = 5,
    # min_words: int = 3,
    max_duration: float = 1.8,
    pause_threshold: float = 0.4,
):
    words = transcript.get("word_segments", [])

    subtitles = []
    current_words = []

    # def save_group():
    #     if not current_words:
    #         return

    #     subtitles.append({
    #         "start": current_words[0]["start"],
    #         "end": current_words[-1]["end"],
    #         "text": " ".join(
    #             word["word"].strip() for word in current_words
    #         ),
    #     })

    #     current_words.clear()
    def save_group():
        if not current_words:
            return

        subtitles.append({
            "start": current_words[0]["start"],
            "end": current_words[-1]["end"],
            "text": " ".join(
                word["word"].strip() for word in current_words
            ),
            "words": current_words.copy(),
        })

        current_words.clear()

    # for word in words:
    #     if not current_words:
    #         current_words.append(word)
    #         continue

    #     previous = current_words[-1]

    #     pause = word["start"] - previous["end"]
    #     duration = word["end"] - current_words[0]["start"]

    #     sentence_finished = previous["word"].strip().endswith(
    #         (".", "?", "!")
    #     )

    #     should_split = (
    #         len(current_words) >= max_words
    #         or duration >= max_duration
    #         or pause >= pause_threshold
    #         or sentence_finished
    #     )

    #     if should_split and len(current_words) >= min_words:
    #         save_group()

    #     current_words.append(word)
    for word in words:
        if not current_words:
            current_words.append(word)
            continue

        previous = current_words[-1]

        pause = word["start"] - previous["end"]
        duration = word["end"] - current_words[0]["start"]

        sentence_finished = previous["word"].strip().endswith(
            (".", "?", "!")
        )

        should_split = (
            sentence_finished
            or len(current_words) >= max_words
            or duration >= max_duration
            or pause >= pause_threshold
        )

        if should_split:
            save_group()

        current_words.append(word)

    save_group()

    return subtitles
