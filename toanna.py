import streamlit as st
import random
import math
import json
from datetime import datetime
import google.generativeai as genai

# ==================== CẤU HÌNH GEMINI (bắt buộc có key) ====================
# Cách lấy key miễn phí: https://aistudio.google.com/app/apikey (30 giây xong)
genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")  # ← Thay bằng key thật của bạn
model = genai.GenerativeModel('gemini-1.5-flash')

# ==================== CẤU HÌNH TRANG ====================
st.set_page_config(
    page_title="Gia sư Toán AI Bản Mường - Na Ư, Điện Biên",
    page_icon="🏔️",
    layout="wide"
)

# ==================== CSS ĐẸP NHƯ THỔ CẨM ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
    body {font-family: 'Nunito', sans-serif; background: #f0f4f8;}
    .header {background: linear-gradient(135deg, #1a237e, #3949ab); color:white; padding:30px; border-radius:20px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.3);}
    .title {font-size:3.2rem; font-weight:900; text-shadow: 3px 3px 0px #ff1744;}
    .pattern {height:15px; background: repeating-linear-gradient(45deg,#d32f2f,#d32f2f 15px,#ffeb3b 15px,#ffeb3b 30px,#388e3c 30px,#388e3c 45px,#1976d2 45px,#1976d2 60px);}
    .btn-ai {background:linear-gradient(to right,#ff1744,#d50000);color:white;border:none;border-radius:50px;padding:15px 30px;font-size:18px;font-weight:bold;}
    .correct {background:#e8f5e8;padding:20px;border-radius:15px;border-left:8px solid #4caf50;text-align:center;font-size:1.5rem;}
    .wrong {background:#ffebee;padding:20px;border-radius:15px;border-left:8px solid #f44336;}
    .hint {background:#fff8e1;padding:20px;border-radius:15px;border-left:8px solid #ffb300;}
    .hmong {background:#fce4ec;padding:20px;border-radius:15px;border-left:8px solid #e91e63;font-style:italic;}
</style>
""", unsafe_allow_html=True)

# ==================== DỮ LIỆU CHƯƠNG TRÌNH HỌC (giữ nguyên của bạn) ====================
CHUONG_TRINH_HOC = {
    "Lớp 1": {"Số học": ["Các số từ 0-10", "Phép cộng trừ trong 10"]},
    "Lớp 2": {"Số học": ["Phép cộng trừ trong 20", "Bảng nhân 2,5"]},
    "Lớp 3": {"Số học": ["Bảng nhân chia 6-9", "Phép chia có dư"]},
    "Lớp 4": {"Số học": ["Số lớn", "Phép nhân chia nhiều chữ số"]},
    "Lớp 5": {"Hình học": ["Diện tích tam giác", "Số thập phân"]},
    "Lớp 6": {"Đại số": ["ƯCLN - BCNN", "Số nguyên"]},
    "Lớp 7": {"Hình học": ["Tam giác", "Căn bậc hai"]},
    "Lớp 8": {"Đại số": ["Đa thức", "Hằng đẳng thức"]},
    "Lớp 9": {"Hình học": ["Tam giác vuông - Pythagoras", "Đường tròn", "Hệ phương trình"]},
    # Bạn có thể copy lại toàn bộ dữ liệu cũ vào đây
}

# ==================== HEADER ĐẸP + TRUY CẬP ====================
if 'visits' not in st.session_state:
    st.session_state.visits = 0
st.session_state.visits += 1

st.markdown(f"""
<div class="header">
    <h1 class="title">🏔️ GIA SƯ TOÁN AI BẢN MƯỜNG</h1>
    <h3>Trường PTDTBT TH&THCS Na Ư - Điện Biên</h3>
    <h2>👨‍🎓 Lượt học: {st.session_state.visits:,} học sinh</h2>
    <p>Ứng dụng AI dạy toán đầu tiên bằng tiếng Việt + tiếng H’Mông tại Điện Biên</p>
</div>
<div class="pattern"></div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR CHỌN BÀI ====================
with st.sidebar:
    st.image("https://i.imgur.com/9Z8Y9Kb.png", use_container_width=True)  # thay link ảnh trường bạn
    st.header("Chọn lớp & bài")
    lop = st.selectbox("Lớp", list(CHUONG_TRINH_HOC.keys()))
    chuong = st.selectbox("Chương", list(CHUONG_TRINH_HOC[lop].keys()))
    bai = st.selectbox("Bài học", CHUONG_TRINH_HOC[lop][chuong])

# ==================== HÀM SINH ĐỀ BẰNG GEMINI ====================
def sinh_de_ai(lop, bai):
    prompt = f"""
    Tạo 1 câu hỏi toán lớp {lop} theo đúng SGK Kết nối tri thức, chủ đề "{bai}".
    Yêu cầu:
    - Câu hỏi mới, khó vừa phải.
    - Có 4 đáp án trắc nghiệm (A,B,C,D), chỉ 1 đúng.
    - Có lời giải ngắn gọn + gợi ý tiếng H’Mông.
    Trả về đúng định dạng JSON sau, không thêm chữ thừa:
    {
        "cau_hoi": "Câu hỏi dạng LaTeX",
        "dap_an_dung": "A",
        "lua_chon": {"A": "...", "B": "...", "C": "...", "D": "..."},
        "loi_giai": "Giải thích ngắn gọn",
        "goi_y_hmong": "Gợi ý bằng tiếng H’Mông"
    }
    """
    try:
        response = model.generate_content(prompt)
        json_text = response.text.strip("```json").strip("```")
        return json.loads(json_text)
    except Exception as e:
        st.error("Gemini đang bận, thử lại sau 10 giây nhé!")
        return None

# ==================== NÚT TẠO ĐỀ ====================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### 📚 {bai}")
    if st.button("✨ TẠO CÂU HỎI BẰNG AI (Gemini)", type="primary", use_container_width=True):
        with st.spinner("AI đang tạo đề siêu hay cho các em bản Mường..."):
            de = sinh_de_ai(lop, bai)
            if de:
                st.session_state.de = de
                st.session_state.start_time = datetime.now()
        st.rerun()

    if "de" in st.session_state:
        de = st.session_state.de
        st.latex(de["cau_hoi"])

        # Hiển thị 4 đáp án
        with st.form("dap_an_form"):
            choice = st.radio("Chọn đáp án:", options=["A", "B", "C", "D"],
                            format_func=lambda x: f"{x}. {de['lua_chon'][x]}")
            submit = st.form_submit_button("✅ Kiểm tra")

            if submit:
                if choice == de["dap_an_dung"]:
                    st.balloons()
                    st.markdown('<div class="correct">🎉 CHÍNH XÁC! Yog lawm! Giỏi quá em ơi!</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="wrong">Chưa đúng rồi! Tsis yog lawm<br>Đáp án đúng là: <b>{de["dap_an_dung"]}</b></div>', unsafe_allow_html=True)

                # Gợi ý + tiếng H’Mông
                st.markdown("### 💡 Lời giải")
                st.info(de["loi_giai"])
                st.markdown('<div class="hmong">🗣️ Tiếng H’Mông:<br>' + de["goi_y_hmong"] + '</div>', unsafe_allow_html=True)

# Footer truyền cảm hứng
st.markdown("""
<div style='text-align:center; margin-top:50px; padding:30px; background:#1a237e; color:white; border-radius:20px;'>
    <h2>🌟 Sản phẩm dự thi Cuộc thi “Sáng tạo AI trong giáo dục” tỉnh Điện Biên 2025-2026</h2>
    <h3>Đưa trí tuệ nhân tạo đến từng bản làng – Vì một Điện Biên chuyển đổi số!</h3>
    <p>© 2025 Trường PTDTBT TH&THCS Na Ư - Bản Mường</p>
</div>
""", unsafe_allow_html=True)
