import os
import json
import requests

def rewrite_script_with_gemini(transcript_text: str, api_key: str = None) -> dict:
    """
    Sử dụng Google Gemini 1.5 Flash (hoàn toàn miễn phí) để phân tích
    và biến tấu kịch bản thoại video thành 3 góc kịch bản TikTok/Shorts mới.
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        print("⚠️ Không tìm thấy GEMINI_API_KEY. Vui lòng cung cấp key hoặc đặt biến môi trường.")
        return None

    print("\n🧠 Đang kết nối Gemini 1.5 Flash AI để phân tích và biến tấu kịch bản...")
    
    # Endpoint Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    
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
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096
        }
    }

    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        res_data = response.json()
        
        if "candidates" in res_data and len(res_data["candidates"]) > 0:
            result_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
            return result_text
        else:
            print(f"❌ Lỗi từ Gemini API: {res_data}")
            return None
    except Exception as e:
        print(f"❌ Lỗi kết nối API: {e}")
        return None
