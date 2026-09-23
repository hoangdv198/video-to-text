import os
import json
import requests

def get_gemini_api_key(api_key=None):
    if api_key:
        return api_key
    for env_var in ["GEMINI_API_KEY", "GEMINI_A", "GEMINI_KEY"]:
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

def rewrite_script_with_gemini(transcript_text, api_key=None):
    key = get_gemini_api_key(api_key)
    if not key:
        print("⚠️ Không tìm thấy GEMINI_API_KEY.")
        return None

    print("\n🧠 Đang kết nối Gemini AI để phân tích và biến tấu kịch bản...")
    
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

    # Thử danh sách các model từ mới nhất (2.5-flash, 2.0-flash, 1.5-flash-latest, 1.5-flash-8b...)
    candidate_endpoints = [
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-8b:generateContent",
        "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent",
    ]

    last_err = None
    for endpoint in candidate_endpoints:
        url = f"{endpoint}?key={key}"
        try:
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
            res_data = response.json()
            if "candidates" in res_data and len(res_data["candidates"]) > 0:
                return res_data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                last_err = res_data
        except Exception as e:
            last_err = str(e)

    print(f"❌ Lỗi từ Gemini API: {last_err}")
    return None
