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

def rewrite_script_with_gemini(transcript_text, api_key=None):
    key = get_gemini_api_key(api_key)
    if not key:
        print("⚠️ Không tìm thấy GEMINI_API_KEY.")
        return None

    models_to_try = [
        "gemini-3.1-pro-preview",
        "gemini-3-flash-preview",
        "gemini-3.1-flash-lite-preview",
        "gemini-2.5-flash",
    ]

    prompt = f"""
Bạn là một chuyên gia tối ưu và viết lại kịch bản video ngắn (TikTok/Reels/Shorts) chuyển đổi cao.
Dưới đây là lời thoại gốc bóc băng từ video:
---
"{transcript_text}"
---

YÊU CẦU QUAN TRỌNG:
- BẮT BUỘC GIỮ NGUYÊN KHUNG SƯỜN & MẠCH Ý GỐC: Đi đúng thứ tự từng luận điểm, tính năng, thông số và trải nghiệm như video gốc đã nói (không sáng tác thêm nhân vật hay bối cảnh lạ, không làm mất sườn bài).
- MỤC TIÊU: "Thay da đổi thịt" lời thoại trên chính khung xương đó để video tự nhiên hơn, bắt tai hơn, giật hook mở đầu bén hơn và tăng tỉ lệ giữ chân người xem.

Hãy xuất ra:
1. **KHUNG SƯỜN Ý CHÍNH CỦA VIDEO GỐC** (Tóm tắt các bước theo mạch video gốc).

2. **BẢN BIẾN TẤU 1: PHONG CÁCH TỰ NHIÊN, GẦN GŨI (Conversational - Như bạn thân khuyên nhau)**
- Giữ 100% mạch ý gốc.
- Viết lại câu từ mềm mại, chân thật, tự nhiên như lời nói thường ngày.

3. **BẢN BIẾN TẤU 2: PHONG CÁCH NĂNG LƯỢNG CAO, BẮT TREND (High Energy / Fast Paced)**
- Giữ 100% mạch ý gốc.
- Hook mở đầu dứt khoát, nhịp điệu nhanh, câu từ ngắn gọn, gãy gọn, kích thích nghe tiếp.

4. **BẢN BIẾN TẤU 3: PHONG CÁCH TỐI ƯU CHUYỂN ĐỔI (Conversion Focus - Bán hàng mượt mà)**
- Giữ 100% mạch ý gốc.
- Nhấn mạnh sâu vào cảm giác thỏa mãn và giải pháp chấm dứt nỗi đau đau mỏi vai gáy.

(Mỗi bản đều chia rõ từng đoạn tương ứng với sườn gốc kèm gợi ý hành động/cảnh quay thực tế).
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }

    last_err = None
    for model_name in models_to_try:
        print(f"🧠 Đang kết nối Gemini AI ({model_name})...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
        try:
            res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}).json()
            if "candidates" in res and len(res["candidates"]) > 0:
                print(f"✅ Kết nối thành công với {model_name}!")
                return res["candidates"][0]["content"]["parts"][0]["text"]
            else:
                last_err = res
        except Exception as e:
            last_err = str(e)

    print(f"❌ Lỗi từ Gemini API: {last_err}")
    return None
