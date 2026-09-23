import os
from faster_whisper import WhisperModel

def format_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def transcribe_audio_or_video(input_path, output_srt="subtitles.srt", model_size="large-v3", device="cuda"):
    """
    Bóc băng file video/audio bằng faster-whisper.
    device='cuda' khi chạy trên Colab GPU (T4), tự động fallback sang 'cpu' nếu không có GPU.
    """
    print(f"🚀 Khởi tạo Faster-Whisper ({model_size}) trên thiết bị: {device}...")
    try:
        compute_type = "float16" if device == "cuda" else "int8"
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
    except Exception as e:
        print(f"⚠️ Cảnh báo thiết bị ({e}), chuyển sang chạy CPU...")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"🎙️ Bắt đầu bóc băng: {input_path}...")
    segments, info = model.transcribe(
        input_path,
        language="vi",
        beam_size=1,
        vad_filter=True,
        condition_on_previous_text=False
    )

    print(f"Detected language: {info.language} ({info.language_probability:.2f})")
    print("\n--- NỘI DUNG LỜI THOẠI ---")
    
    with open(output_srt, "w", encoding="utf-8") as srt:
        for i, seg in enumerate(segments, 1):
            start = format_timestamp(seg.start)
            end = format_timestamp(seg.end)
            text = seg.text.strip()
            print(f"[{start} -> {end}] {text}")
            srt.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    print(f"\n🎉 Đã xuất file phụ đề: {output_srt}")
    return output_srt
