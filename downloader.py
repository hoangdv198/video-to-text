import os
import requests

def download_tiktok_video(url, output_path="video.mp4"):
    """
    Tải video TikTok MP4 không logo chất lượng cao thông qua API TikWM.
    Hỗ trợ cả link rút gọn vt.tiktok.com và link đầy đủ tiktok.com/@user/video/...
    """
    print(f"🎬 Đang phân tích và tải video từ link: {url}")
    api_url = "https://www.tikwm.com/api/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    
    response = requests.post(api_url, data={"url": url}, headers=headers).json()
    
    if response.get("code") == 0:
        data = response["data"]
        video_url = data.get("play")
        title = data.get("title", "No Title")
        author = data.get("author", {}).get("nickname", "Unknown")
        
        print(f"📌 Tiêu đề: {title[:60]}...")
        print(f"👤 Kênh: {author}")
        
        if not video_url:
            raise Exception("Không tìm thấy đường dẫn video tải về!")
            
        print("⬇️ Đang tải dữ liệu MP4 về...")
        vid_res = requests.get(video_url, stream=True, headers=headers)
        with open(output_path, "wb") as f:
            for chunk in vid_res.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✅ Tải thành công! File lưu tại: {output_path} ({file_size_mb:.2f} MB)")
        return output_path
    else:
        raise Exception(f"Lỗi từ TikTok API: {response.get('msg')}")

if __name__ == "__main__":
    import sys
    test_url = sys.argv[1] if len(sys.argv) > 1 else "https://vt.tiktok.com/ZSb1qPTFo/"
    download_tiktok_video(test_url, "test_output.mp4")
