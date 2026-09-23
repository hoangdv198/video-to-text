import os
import re
import requests
import subprocess
from urllib.parse import urlparse

def is_tiktok_url(url: str) -> bool:
    netloc = urlparse(url).netloc.lower()
    return "tiktok.com" in netloc

def is_youtube_url(url: str) -> bool:
    netloc = urlparse(url).netloc.lower()
    return "youtube.com" in netloc or "youtu.be" in netloc

def download_tiktok_via_api(url: str, output_path: str = "video.mp4") -> str:
    """Tải TikTok không logo qua TikWM API"""
    print(f"🎬 [TikTok] Đang phân tích link qua TikWM API: {url}")
    api_url = "https://www.tikwm.com/api/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    res = requests.post(api_url, data={"url": url}, headers=headers).json()
    if res.get("code") == 0:
        data = res["data"]
        video_url = data.get("play")
        title = data.get("title", "")
        author = data.get("author", {}).get("nickname", "")
        print(f"📌 Tiêu đề: {title[:60]}")
        print(f"👤 Kênh: {author}")
        if not video_url:
            raise Exception("Không tìm thấy đường link video!")
        
        r = requests.get(video_url, stream=True, headers=headers)
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        return output_path
    else:
        raise Exception(f"TikWM API error: {res.get('msg')}")

def download_generic_media(url: str, output_path: str = "video.mp4") -> str:
    """
    Dùng yt-dlp để tải hầu hết các nền tảng: YouTube, Facebook, Instagram, Twitter/X, Douyin...
    Tự động trích xuất định dạng tốt nhất (MP4).
    """
    print(f"🎬 [Universal Media] Đang tải qua yt-dlp: {url}")
    # Nếu là youtube hoặc các trang khác, ưu tiên lấy mp4 chất lượng tốt nhất
    cmd = [
        "yt-dlp",
        "--no-check-certificates",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "-o", output_path,
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(output_path):
        return output_path
    else:
        # Fallback thử lấy format bất kỳ
        cmd_fallback = ["yt-dlp", "--no-check-certificates", "-o", output_path, url]
        subprocess.run(cmd_fallback, check=True)
        return output_path

def download_video(url: str, output_path: str = "video.mp4") -> str:
    """
    Hàm tổng quát: Tự động phân loại link TikTok, YouTube, Facebook, hoặc link web khác
    để dùng phương pháp tải tối ưu nhất.
    """
    # Xoá file cũ nếu tồn tại
    if os.path.exists(output_path):
        os.remove(output_path)

    if is_tiktok_url(url):
        try:
            return download_tiktok_via_api(url, output_path)
        except Exception as e:
            print(f"⚠️ TikWM gặp lỗi ({e}), chuyển sang dùng yt-dlp fallback...")
            return download_generic_media(url, output_path)
    else:
        return download_generic_media(url, output_path)

if __name__ == "__main__":
    import sys
    test_url = sys.argv[1] if len(sys.argv) > 1 else "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    download_video(test_url, "test_download.mp4")
