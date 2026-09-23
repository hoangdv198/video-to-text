import argparse
import os
import glob
import sys
import importlib

# Reload rewriter và image_generator tránh cache
for mod in ["rewriter", "image_generator"]:
    if mod in sys.modules:
        importlib.reload(sys.modules[mod])

from downloader import download_video
from transcriber import transcribe_audio_or_video
import rewriter
import image_generator

def main():
    parser = argparse.ArgumentParser(description="Tự động tải video, bóc băng, biến tấu kịch bản và sinh ảnh phân cảnh bằng FLUX AI")
    parser.add_argument("--url", type=str, help="Link video (TikTok, YouTube, Facebook, Instagram...)")
    parser.add_argument("--file", type=str, help="Đường dẫn file video/audio có sẵn trên máy để bóc băng trực tiếp")
    parser.add_argument("--model", type=str, default="large-v3", help="Kích thước model Whisper (large-v3, medium, small)")
    parser.add_argument("--device", type=str, default="cuda", help="cuda hoặc cpu")
    parser.add_argument("--output_video", type=str, default="video.mp4", help="Tên file video tải về")
    parser.add_argument("--output_srt", type=str, default="subtitles.srt", help="Tên file srt xuất ra")
    parser.add_argument("--rewrite", action="store_true", help="Bật tính năng biến tấu kịch bản bằng Gemini AI")
    parser.add_argument("--api_key", type=str, help="Google Gemini API Key (hoặc set biến môi trường GEMINI_API_KEY)")
    parser.add_argument("--output_script", type=str, default="kich_ban_bien_tau.txt", help="Tên file lưu kịch bản biến tấu")
    parser.add_argument("--gen_image", type=str, help="Tạo ảnh AI với model FLUX.1 từ mô tả prompt")
    parser.add_argument("--image_output", type=str, default="anh_phan_canh.jpg", help="Tên file ảnh xuất ra")
    
    args = parser.parse_args()
    
    # 0. Nếu chỉ yêu cầu tạo ảnh
    if args.gen_image:
        image_generator.generate_image(args.gen_image, output_path=args.image_output)
        if not args.url and not args.file:
            return

    input_file = args.file
    
    # 1. Xác định file đầu vào
    if not input_file:
        if args.url:
            input_file = download_video(args.url, args.output_video)
        else:
            local_files = glob.glob("snaptikvn_*.mp4") + glob.glob("*.mp4")
            if local_files:
                input_file = local_files[0]
                print(f"🎯 Tự động phát hiện file video có sẵn: {input_file}")
            else:
                print("❌ Vui lòng cung cấp --url hoặc --file hoặc --gen_image!")
                return
            
    # 2. Bóc băng âm thanh
    srt_file = transcribe_audio_or_video(
        input_path=input_file,
        output_srt=args.output_srt,
        model_size=args.model,
        device=args.device
    )

    # 3. Biến tấu kịch bản nếu bật cờ --rewrite
    if args.rewrite:
        print("\n" + "="*50)
        print("✍️ ĐANG TIẾN HÀNH BIẾN TẤU KỊCH BẢN BẰNG GEMINI AI...")
        print("="*50)
        
        full_transcript = []
        if os.path.exists(srt_file):
            with open(srt_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line.isdigit() or "-->" in line or not line:
                        continue
                    full_transcript.append(line)
                    
        transcript_text = " ".join(full_transcript)
        
        if not transcript_text:
            print("⚠️ Không tìm thấy nội dung lời thoại để biến tấu.")
            return

        new_scripts = rewriter.rewrite_script_with_gemini(transcript_text, api_key=args.api_key)
        
        if new_scripts:
            print("\n" + "*"*20 + " KẾT QUẢ BIẾN TẤU KỊCH BẢN " + "*"*20)
            print(new_scripts)
            print("*"*66)
            
            with open(args.output_script, "w", encoding="utf-8") as f:
                f.write(new_scripts)
            print(f"\n🎉 Đã lưu toàn bộ kịch bản biến tấu vào file: {args.output_script}")

if __name__ == "__main__":
    main()
