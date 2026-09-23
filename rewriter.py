import os
import json
import requests

def get_gemini_api_key(api_key=None):
    if api_key:
        return api_key
    for env_var in ["GEMINI_API_KEY", "GEMINI_A", "GEMINI A", "GEMINI_KEY"]:
        if os.getenv(env_var):
            return os.getenv(env_var)
    try:
        from google.colab import userdata
        for key_name in ["GEMINI_API_KEY", "GEMINI_A", "GEMINI A", "GEMINI_KEY"]:
            try:
                k = userdata.get(key_name)
                if k:
                    return k
            except Exception:
                pass
    except Exception:
        pass
    return None

def get_available_gemini_model(key):
    """
    Tự động truy vấn trực tiếp từ Google API xem tài khoản này được cấp những model nào.
    Tránh 100% lỗi 404 do lệch tên model hoặc lệch version API!
    """
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
        res = requests.get(list_url, timeout=10).json()
        models = res.get("models", [])
        
        # Lọc các model hỗ trợ generateContent
        supported = [
            m["name"] for m in models 
            if "generateContent" in m.get("supportedGenerationMethods", [])
        ]
        
        # Ưu tiên flash -> pro -> bất kỳ model nào có
        for pref in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-pro"]:
            for name in supported:
                if pref in name:
                    return name # Dạng: models/gemini-...
                    
        if supported:
            return supported[0]
    except Exception as e:
        print(f"⚠️ Không tự động dò được danh sách model ({e}), dùng mặc định.")
    
    return "models/gemini-1.5-flash-latest"

def rewrite_script_with_gemini(transcript_text, api_key=None):
    key = get_gemini_api_key(api_key)
    if not key:
        print("⚠️ Không tìm thấy GEMINI_API_KEY.")
        return None

    # 1. Tự động tìm model chính xác tuyệt đối từ Google
    model_name = get_available_gemini_model(key)
    # Loại bỏ tiền tố 'models/' nếu có để lắp vào URL chuẩn
    clean_model_name = model_name.replace("models/", "")
    print(f"\n🧠 Đang kết nối Gemini AI (Model: {clean_model_name}) để phân tích và biến tấu kịch bản...")
    
    prompt = f"""
Bạn là một chuyên gia sáng tạo nội dung TikTok & Video Ngắn (Shorts/Reels) triệu view hàng đầu.
Dưới đây là nội dung lời thoại bóc băng từ một video gốc:
---
"{transcript_text}"
---

Hãy phân tích và viết lại thành 3 kịch bản biến tấu mới mẻ, hấp dẫn, chuẩn phong cách TikTok (giữ chân người xem trong 3s đầu, đánh trúng nỗi đau, thúc đẩy mua hàng tự nhiên):

1. **PHÂN TÍCH VIDEO GỐC**:
- Góc tiếp cận (Angle) & Nỗi đau (Pain point) chính.
- Điểm mạnh & Điểm cần cải thiện.

2. **KỊCH BẢN 1: PHONG CÁCH TÂM SỰ / TRẢI NGHIỆM ĐỜI THƯỜNG (Storytelling)**
- Tiêu đề & Hook 3s đầu (Gây tò mò / đồng cảm).
- Kịch bản chi tiết: Phân cảnh quay + Lời thoại.
- Lời kêu gọi hành động (CTA).

3. **KỊCH BẢN 2: PHONG CÁCH DRAMA / BÓC PHỐT / GÂY TRANH CÃI (Controversial Hook)**
- Tiêu đề & Hook 3s đầu (Cực sốc, phá vỡ niềm tin cũ).
- Kịch bản chi tiết: Phân cảnh quay + Lời thoại.
- Lời kêu gọi hành động (CTA).

4. **KỊCH BẢN 3: PHONG CÁCH CHUYÊN GIA / BÁC SĨ TƯ VẤN (Expert / Authority)**
- Tiêu đề & Hook 3s đầu (Đánh vào kiến thức khoa học / sức khỏe).
- Kịch bản chi tiết: Phân cảnh quay + Lời thoại.
- Lời kêu gọi hành động (CTA).

Viết bằng tiếng Việt tự nhiên, ngắt nghỉ rõ ràng, chuẩn phong cách nói chuyện của Creator.
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model_name}:generateContent?key={key}"
    try:
        r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}).json()
        if "candidates" in r and len(r["candidates"]) > 0:
            return r["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"❌ Lỗi từ Gemini API: {r}")
            return None
    except Exception as e:
        print(f"❌ Lỗi kết nối API: {e}")
        return None
