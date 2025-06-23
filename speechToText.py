from gc import collect
from typing import Final
from torch.cuda import empty_cache, is_available as isCudaAvailable
from whisperx import load_model, load_audio, load_align_model, align

# Todo - Add Return Type
def SpeechToText(path: str):
    cudaSupported: Final = isCudaAvailable()
    device: Final = "cuda" if cudaSupported else "cpu"
    compute_type: Final = "float16" if cudaSupported else "float32"

    model: Final = load_model("base", device=device, compute_type=compute_type)
    audio: Final = load_audio(path)
    result = model.transcribe(audio, batch_size=16)
    
    collect()
    empty_cache()
    del model

    model_a, metadata = load_align_model(language_code=result["language"], device=device)
    result = align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    collect()
    empty_cache()
    del model_a

    # for segment in result["segments"]:
    #     for word in segment["words"]:
    #         print(f"{word['word']} ({word['start']:.2f}s - {word['end']:.2f}s)")

    return result["segments"]

    
