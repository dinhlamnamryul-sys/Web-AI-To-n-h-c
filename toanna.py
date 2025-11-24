import streamlit as st
import random
import math
import time
import os
from deep_translator import GoogleTranslator
import google.generativeai as genai  # Gemini API (miễn phí 60 req/phút)
from gtts import gTTS  # Text-to-speech
import base64
from datetime import datetime

# ==================== CẤU HÌNH GEMINI AI (MIỄN PHÍ) ====================
# Đăng ký key miễn phí tại: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else "YOUR_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ==================== CẤU HÌNH TRANG ====================
st.set_page_config(
    page_title="🏔️ Gia sư Toán AI Bản Mường - Na Ư, Điện Biên",
    page_icon="🏔️",
    layout="wide"
)

# ==================== CSS THỔ CẨM H'MÔNG ĐẸP HƠN ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&family=Patrick+Hand&display=swap');
    .hmong-header {background: linear-gradient(135deg, #1a237e, #3949ab); color:white; padding:20px; border-radius:20px; text-align:center; box-shadow:0 10px 30px rgba(0,0,0,0.3);}
    .hmong-title {font-size:3rem; font-weight:900; text-shadow: 3px 3px 0px #ff1744;}
    .pattern {height:15px; background: repeating-linear-gradient(45deg,#d32f2f,#d32f2f 15px,#ffeb3b 15px,#ffeb3b 30px,#388e3c 30px,#388e3c 45px,#1976d2 45px,#1976d2 60px);}
    .visit-box {background:#00e676;color:black;padding:10px 25px;border-radius:50px;font-weight:bold;font-size:1.2rem;display:inline-block;margin:10px;}
    .stButton>button {background:linear-gradient(to right,#ff1744,#d50000);color:white;border-radius:50px;padding:15px;font-size:18px;font-weight:bold;}
    .success-box {background:#e8f5e8;padding:20px;border-radius:15px;border-left:8px solid #4caf50;}
    .hint-box {background:#fff3e0;padding:20px;border-radius:15px;border-left:8px solid #ff9800;}
    .hmong-box {background:#fce4ec;padding:20px;border-radius:15px;border-left:8px solid #e91e63;font-style:italic;}
</style>
""", unsafe_allow_html=True)

# ==================== DỮ LIỆU CHƯƠNG TRÌNH HỌC (giữ nguyên của bạn) ====================
CHUONG_TRINH_HOC = { ... }  # giữ nguyên như code cũ của bạn

# ==================== HÀM TẠO ÂM THANH ====================
def speak_vi(text):
    tts = gTTS(text=text, lang='vi', slow=False)
    tts.save("temp_vi.mp3")
    audio_bytes = open("temp_vi.mp3", "rb").read()
    return f'<audio autoplay="true" src="data:audio/mp3;base64,{base64.b64encode(audio_bytes).decode()}"></audio>'

def speak_hmong(text):
    tts = gTTS(text=text, lang='vi')  # gTTS chưa hỗ trợ H’Mông → dùng tiếng Việt giọng chậm
    tts.save("temp_hmong.mp3")
    tts.slow = True
    audio_bytes = open("temp_hmong.mp3", "rb").read()
    return f'<audio autoplay="true" src="data:audio/mp3;base64,{base64.b64encode(audio_bytes).decode()}"></audio>'

# ==================== AI SINH ĐỀ THÔNG MINH (Gemini) ====================
def ai_sinh_de_thong_minh(lop, bai_hoc):
    prompt = f"""
    Bạn là giáo viên toán giỏi nhất tỉnh Điện Biên.
    Hãy tạo 1 câu hỏi toán lớp {lop} theo đúng chương trình SGK Kết nối tri thức, chủ đề: "{bai_hoc}".
    Yêu cầu:
    - Câu hỏi phải mới, không trùng lặp.
    - Có đáp án chính xác.
    - Có 4 đáp án trắc nghiệm (nếu là trắc nghiệm).
    - Có gợi ý giải ngắn gọn bằng tiếng Việt và tiếng H’Mông.
    - Trả về JSON đúng định dạng sau, không thêm ký tự thừa:
    {
        "cau_hoi": "câu hỏi LaTeX",
        "loai": "mcq" hoặc "number",
        "dap_an": đáp án đúng,
        "lua_chon": ["A","B","C","D"] hoặc [],
        "goi_y_vi": "gợi ý tiếng Việt",
        "goi_y_hmong": "gợi ý tiếng H’Mông"
    }
    """
    try:
        response = model.generate_content(prompt)
        import json
        data = json.loads(response.text.strip("```json").strip("```"))
        return data
    except:
        # Fallback về hàm cũ nếu Gemini lỗi
        return None

# ==================== GIAO DIỆN CHÍNH ====================
st.markdown("""
<div class="hmong-header">
    <h1 class="hmong-title">🏔️ GIA SƯ TOÁN AI BẢN MƯỜNG</h1>
    <h3>Trường PTDTBT TH&THCS Na Ư - Điện Biên</h3>
    <div class="visit-box">👨‍🎓 Lượt học hôm nay: {visit_count}</div>
    <p>Ứng dụng AI dạy toán bằng tiếng Việt & tiếng H’Mông đầu tiên tại Điện Biên</p>
</div>
<div class="pattern"></div>
""", unsafe_allow_html=True)

# Sidebar chọn lớp
with st.sidebar:
    st.image("https://i.imgur.com/9Z8Y9Kb.png", width=200)  # ảnh trường Na Ư hoặc bản Mường
    st.header("🏫 Chọn bài học")
    lop = st.selectbox("Lớp", list(CHUONG_TRINH_HOC.keys()))
    chuong = st.selectbox("Chương", list(CHUONG_TRINH_HOC[lop].keys()))
    bai = st.selectbox("Bài", CHUONG_TRINH_HOC[lop][chuong])
    
    st.markdown("---")
    st.success("🚀 Được xây dựng bằng Gemini AI & Streamlit")
    st.info("Dành riêng cho học sinh dân tộc H’Mông tỉnh Điện Biên")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### 📚 {bai}")
    
    if st.button("✨ TẠO CÂU HỎI BẰNG AI (Gemini)", type="primary", use_container_width=True):
        with st.spinner("AI đang suy nghĩ..."):
            data = ai_sinh_de_thong_minh(lop, bai)
            if not data:
                st.error("AI đang nghỉ, dùng đề cũ nhé!")
                # fallback hàm cũ của bạn
            else:
                st.session_state.de = data
                st.session_state.time_start = datetime.now()
        st.rerun()

    if "de" in st.session_state:
        de = st.session_state.de
        st.markdown("### ❓ Câu hỏi")
        st.latex(de["cau_hoi"])
        
        # Phát âm câu hỏi
        if st.button("🔊 Nghe câu hỏi (Tiếng Việt)"):
            st.markdown(speak_vi(de["cau_hoi"].replace("$","").replace("\\","")), unsafe_allow_html=True)
        if st.button("🔊 Nghe tiếng H’Mông"):
            hmong_text = dich_sang_mong(de["cau_hoi"].replace("$","").replace("\\",""))
            st.markdown(speak_hmong(hmong_text), unsafe_allow_html=True)

        # Dịch H’Mông
        if st.button("🗣️ Dịch sang tiếng H’Mông"):
            translated = dich_sang_mong(de["cau_hoi"].replace("$","").replace("\\",""))
            st.info(f"**Tiếng H’Mông:** {translated}")

with col2:
    st.markdown("### ✍️ Trả lời")
    if "de" in st.session_state:
        with st.form("answer_form"):
            if de["loai"] == "mcq":
                answer = st.radio("Chọn đáp án", de["lua_chon"], index=None)
            else:
                answer = st.text_input("Nhập đáp án") if isinstance(de["dap_an"], str) else st.number_input("Nhập đáp án", value=None)
            
            submitted = st.form_submit_button("✅ Kiểm tra")
            if submitted:
                correct = (answer == de["dap_an"]) or (isinstance(answer, float) and abs(answer - de["dap_an"]) < 0.01)
                time_used = (datetime.now() - st.session_state.time_start).seconds
                
                if correct:
                    st.balloons()
                    st.markdown('<div class="success-box">🎉 CHÍNH XÁC! Yog lawm! 👏</div>', unsafe_allow_html=True)
                    st.markdown(speak_vi("Chính xác, giỏi quá!"), unsafe_allow_html=True)
                else:
                    st.error("Chưa đúng rồi! Tsis yog lawm 😢")
                    st.markdown(f"**Đáp án đúng:** {de['dap_an']}")
                
                # Gợi ý bằng AI
                st.markdown("### 💡 Gợi ý từ AI")
                st.info(de["goi_y_vi"])
                st.markdown('<div class="hmong-box">🗣️ ' + de["goi_y_hmong"] + '</div>', unsafe_allow_html=True)

# Footer truyền cảm hứng
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:20px; background:#1a237e; color:white; border-radius:20px;'>
    <h3>🌟 Toán học không còn là nỗi sợ của trẻ em bản Mường!</h3>
    <p>Sản phẩm dự thi Cuộc thi “Sáng tạo AI trong giáo dục” tỉnh Điện Biên 2025-2026</p>
    <p>Đưa AI đến từng bản làng - Vì một Điện Biên chuyển đổi số!</p>
</div>
""", unsafe_allow_html=True)
