import os
import json
import requests

def get_gemini_api_key(api_key=None):
    # 1. Key truyen truc tiep qua CLI
    if api_key:
        return api_key

    # 2. Key tu bien moi truong
    for env_var in ["GEMINI_API_KEY", "GEMINI_A", "GEMINI_KEY"]:
        if os.getenv(env_var):
            return os.getenv(env_var)

    # 3. Key tu Google Colab Secrets (userdata)
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
    """
    Su dung Google Gemini 1.5 Flash (hoan toan mien phi) de phan tich
    va bien tau kich ban thoai video thanh 3 goc kich ban TikTok/Shorts moi.
    """
    key = get_gemini_api_key(api_key)
    if not key:
        print("⚠️ Khong tim thay GEMINI_API_KEY.")
        print("💡 Meo: Anh co the truyen truc tiep: --api_key 'AIzaSy...' hoac them vao Colab Secrets.")
        return None

    print("\n🧠 Dang ket noi Gemini 1.5 Flash AI de phan tich va bien tau kich ban...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    
    prompt = f"""
Ban la mot chuyen gia sang tao noi dung TikTok & Video Ngan trieu view hang dau.
Duoi day la noi dung loi thoai boc bang tu video goc:
---
"{transcript_text}"
---

Hay phan tich va viet lai thanh 3 kich ban bien tau moi me, hap dan, chuan phong cach TikTok (giu chan nguoi xem trong 3s dau, danh trung noi dau, thuc day mua hang tu nhien):

1. **PHAN TICH VIDEO GOC**:
- Goc tiep can (Angle) & Noi dau (Pain point) chinh.
- Diem manh & Diem can cai thien.

2. **KICH BAN 1: PHONG CACH TAM SU / TRAI NGHIEM DOI THUONG (Storytelling)**
- Tieu de & Hook 3s dau (Gay to mo / dong cam).
- Kich ban chi tiet: Phan canh quay + Loi thoai.
- Loi keu goi hanh dong (CTA).

3. **KICH BAN 2: PHONG CACH DRAMA / BOC PHOT / GAY TRANH CAI (Controversial Hook)**
- Tieu de & Hook 3s dau (Cuc soc, pha vo niem tin cu).
- Kich ban chi tiet: Phan canh quay + Loi thoai.
- Loi keu goi hanh dong (CTA).

4. **KICH BAN 3: PHONG CACH CHUYEN GIA / BAC SI TU VAN (Expert / Authority)**
- Tieu de & Hook 3s dau (Danh vao kien thuc khoa hoc / suc khoe).
- Kich ban chi tiet: Phan canh quay + Loi thoai.
- Loi keu goi hanh dong (CTA).

Viet bang tieng Viet tu nhien, ngat nghi ro rang, chuan phong cach noi chuyen cua Creator.
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
            print(f"❌ Loi tu Gemini API: {res_data}")
            return None
    except Exception as e:
        print(f"❌ Loi ket noi API: {e}")
        return None
