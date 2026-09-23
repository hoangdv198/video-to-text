import argparse
import os
import glob
from downloader import download_tiktok_video
from transcriber import transcribe_audio_or_video

def main():
    parser = argparse.ArgumentParser(description="Tự động tải video TikTok và bóc băng phụ đề bằng Faster-Whisper")
    parser.add_argument("--url", type=str, help="Link video TikTok (vt.tiktok.com hoặc tiktok.com/@user/video/...)")
    parser.add_argument("--file", type=str, help="Đường dẫn file video/audio có sẵn trên máy để bóc băng trực tiếp")
    parser.add_argument("--model", type=str, default="large-v3", help="Kích thước model Whisper (large-v3, medium, small)")
    parser.add_argument("--device", type=str, default="cuda", help="cuda hoặc cpu")
    parser.add_argument("--output_video", type=str, default="video.mp4", help="Tên file video tải về")
    parser.add_argument("--output_srt", type=str, default="subtitles.srt", help="Tên file srt xuất ra")
    
    args = parser.parse_args()
    
    input_file = args.file
    
    # 1. Xác định file đầu vào
    if not input_file:
        # Kiểm tra xem có file snaptik nào người dùng upload lên thư mục hiện tại không
        local_files = glob.glob("snaptikvn_*.mp4") + glob.glob("*.mp4")
        if args.url:
            input_file = download_tiktok_video(args.url, args.output_video)
        elif local_files:
            input_file = local_files[0]
            print(f"🎯 Tự động phát hiện file video có sẵn: {input_file}")
        else:
            print("❌ Vui lòng cung cấp --url hoặc --file!")
            return
            
    # 2. Tiến hành bóc băng
    transcribe_audio_or_video(
        input_path=input_file,
        output_srt=args.output_srt,
        model_size=args.model,
        device=args.device
    )

if __name__ == "__main__":
    main()
