
import torch
import whisperx
import ctranslate2
import transformers


def transcribe_audio(audio_path: str, model_name: str = "base"):




    print("PyTorch:", torch.__version__)
    print("MPS available:", torch.backends.mps.is_available())
    print("Transformers:", transformers.__version__)
    print("CTranslate2:", ctranslate2.__version__)

    print(
        "CTranslate2 MPS support:",
        ctranslate2.get_supported_compute_types("mps")
    )



    # # Use Apple Silicon GPU when available
    # device = "mps" if torch.backends.mps.is_available() else "cpu"

    # # MPS uses float32; CPU uses int8
    # # compute_type = "float32" if device == "mps" else "int8"
    # compute_type = "float16" if device == "mps" else "int8"
    device = "cpu"
    compute_type = "int8"

    print("\n"*5)
    print(f"Using device: {device}")
    print(f"Using model: {model_name}")
    print("\n"*5)

    # Load speech recognition model
    print("\n"*5)
    print("Loading WhisperX model...")
    print("\n"*5)

    model = whisperx.load_model(
        model_name,
        device=device,
        compute_type=compute_type,
    )
    print("\n"*5)
    print("ASR device:", model.model.model.device)
    print("ASR compute type:", model.model.model.compute_type)
    print("\n"*5)

    # Load audio
    print("\n"*5)
    print("Loading audio...")
    print("\n"*5)

    audio = whisperx.load_audio(audio_path)

    # Transcribe speech
    print("\n"*5)
    print("Transcribing audio...")
    print("\n"*5)

    result = model.transcribe(
        audio,
        batch_size=1,
        language="en",
    )

    # Load alignment model
    print("Loading alignment model...")

    align_model, metadata = whisperx.load_align_model(
        language_code=result["language"],
        device=device,
    )

    # Generate word-level timestamps
    print("Aligning word timestamps...")

    result = whisperx.align(
        result["segments"],
        align_model,
        metadata,
        audio,
        device,
    )

    print("Transcription completed!")

    return result
