import os
import urllib.parse
import urllib.request

def generate_image(prompt: str, output_path: str = "scene.jpg", model: str = "flux", width: int = 1024, height: int = 1024):
    """
    Tạo ảnh AI chất lượng cao bằng FLUX.1 (hoàn toàn miễn phí, không cần API key).
    Tự động tải về output_path.
    """
    print(f"🎨 Đang tạo ảnh AI với model {model.upper()}...")
    print(f"📝 Prompt: {prompt}")
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model={model}&width={width}&height={height}&nologo=true"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as resp:
            with open(output_path, "wb") as f:
                f.write(resp.read())
        size_kb = os.path.getsize(output_path) / 1024
        print(f"✅ Đã tạo và lưu ảnh thành công: {output_path} ({size_kb:.1f} KB)")
        return output_path
    except Exception as e:
        print(f"❌ Lỗi tạo ảnh: {e}")
        return None

if __name__ == "__main__":
    import sys
    test_p = sys.argv[1] if len(sys.argv) > 1 else "A high-end ergonomic cervical pillow on a modern luxury bed, 8k, photorealistic"
    generate_image(test_p, "test_flux.jpg")
