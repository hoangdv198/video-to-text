import os
import json
import requests

def get_gemini_api_key(api_key=None):
    if api_key:
        return api_key
    if os.getenv("GEMINI_API_KEY"):
        return os.getenv("GEMINI_API_KEY")
    try:
        from google.colab import userdata
        for key_name in ["GEMINI_API_KEY", "GEMINI_A", "GEMINI_KEY"]:
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
        print("Khong tim thay GEMINI_API_KEY. Vui long cung cap key qua --api_key, bien moi truong, hoac muc Secrets tren Colab.")
        return None

    print("\nDang ket noi Gemini 1.5 Flash AI de phan tich va bien tau kich ban...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    
    prompt = f"""
Ban la mot chuyen gia sang tao noi dung TikTok & Video Ngan trieu view.
Day la loi thoai boc bang tu video goc:
---
"{transcript_text}"
---

Hay phan tich va viet lai thanh 3 kich ban bien tau moi me, chuan phong cach TikTok:
1. PHAN TICH VIDEO GOC (Goc tiep can, noi dau, diem manh/yeu)
2. KICH BAN 1: PHONG CACH TAM SU / TRAI NGHIEM DOI THUONG (Storytelling - Hook 3s, phan canh, loi thoai, CTA)
3. KICH BAN 2: PHONG CACH DRAMA / BOC PHOT / GAY TRANH CAI (Controversial Hook - Hook 3s, phan canh, loi thoai, CTA)
4. KICH BAN 3: PHONG CACH CHUYEN GIA / BAC SI TU VAN (Authority - Hook 3s, phan canh, loi thoai, CTA)
Viet bang tieng Viet tu nhien, ngat nghi ro rang.
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }

    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        res_data = response.json()
        if "candidates" in res_data and len(res_data["candidates"]) > 0:
            return res_data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"Loi tu Gemini API: {res_data}")
            return None
    except Exception as e:
        print(f"Loi ket noi API: {e}")
        return None
