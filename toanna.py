import streamlit as st
import random
import math
import time
import os
import pandas as pd
import io
import base64
import re
from deep_translator import GoogleTranslator
from gtts import gTTS

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gia sư Toán AI - Bản Mường (Game Learning)",
    page_icon="🏔️",
    layout="wide"
)

# --- KHỞI TẠO BIẾN TRÒ CHƠI & LƯỢT TRUY CẬP ---
def update_visit_count():
    count_file = "visit_count.txt"
    if not os.path.exists(count_file):
        with open(count_file, "w") as f: f.write("5383")
        return 5383
    try:
        with open(count_file, "r") as f:
            content = f.read().strip()
            count = int(content) if content else 5383
    except: count = 5383
    count += 1
    with open(count_file, "w") as f: f.write(str(count))
    return count

if 'visit_count' not in st.session_state:
    st.session_state.visit_count = update_visit_count()
if 'user_coins' not in st.session_state:
    st.session_state.user_coins = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'history' not in st.session_state:
    st.session_state.history = []

# --- DỮ LIỆU CHƯƠNG TRÌNH HỌC ---
CHUONG_TRINH_HOC = {
    "Lớp 1": {"Các số phạm vi 10": ["Đếm số", "Cộng trừ"], "Hình học": ["Nhận biết hình"]},
    "Lớp 2": {"Phép cộng trừ (nhớ)": ["Cộng qua 10", "Trừ qua 10"]},
    "Lớp 6": {"Số tự nhiên": ["Lũy thừa", "Số nguyên tố"]},
    "Lớp 9": {"Căn bậc hai": ["Rút gọn biểu thức", "Giải hệ phương trình"]}
}

# --- PHONG CÁCH GIAO DIỆN (CSS) ---
st.markdown("""
<style>
    .game-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin-bottom: 20px;
    }
    .coin-text { font-size: 28px; font-weight: bold; color: #ffeb3b; }
    .streak-text { font-size: 18px; color: #ff5722; font-weight: bold; }
    .problem-box {
        background-color: white; padding: 30px; border-radius: 20px;
        border-top: 10px solid #d32f2f; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- HÀM HỖ TRỢ GAME ---
def get_rank_info(coins):
    if coins < 50: return "Tập sự 🛡️", "🐘 Voi Bản Mường"
    elif coins < 150: return "Thợ săn 🏹", "🐅 Hổ Rừng Già"
    elif coins < 300: return "Chiến binh 🦅", "🦅 Đại Bàng Núi"
    else: return "Trạng nguyên 🎓", "🐉 Rồng Na Ư"

def dich_sang_mong_giu_cong_thuc(text):
    try: return GoogleTranslator(source='vi', target='hmn').translate(text)
    except: return text

def text_to_speech_html(text):
    tts = gTTS(text=text.replace("$",""), lang='vi')
    fp = io.BytesIO(); tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    return f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

# --- LOGIC TẠO CÂU HỎI ---
def tao_de_toan_game(lop, bai):
    # Đây là nơi bạn đặt logic tạo đề từ file cũ
    a, b = random.randint(10, 50), random.randint(1, 9)
    de = f"Em hãy tính: ${a} + {b} = ?$"
    dap_an = a + b
    goi_y = f"Em hãy thực hiện phép cộng hàng đơn vị {a%10} + {b} trước nhé."
    return de, dap_an, goi_y

# --- GIAO DIỆN SIDEBAR ---
with st.sidebar:
    rank, pet = get_rank_info(st.session_state.user_coins)
    st.markdown(f"""
    <div class="game-card">
        <div style="font-size: 50px;">{pet.split()[0]}</div>
        <h3>{rank}</h3>
        <p>{pet}</p>
        <div class="coin-text">💰 {st.session_state.user_coins} Xu</div>
        <div class="streak-text">🔥 Chuỗi: {st.session_state.streak}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("📚 CHỌN BÀI HỌC")
    lop_chon = st.selectbox("Lớp:", list(CHUONG_TRINH_HOC.keys()))
    bai_chon = st.selectbox("Bài học:", CHUONG_TRINH_HOC[lop_chon][list(CHUONG_TRINH_HOC[lop_chon].keys())[0]])
    
    st.write(f"👥 Lượt truy cập: {st.session_state.visit_count}")

# --- GIAO DIỆN CHÍNH ---
st.title("🏫 Thử Thách Toán Học AI")

if 'game_q' not in st.session_state:
    st.session_state.game_q = None

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("✨ NHẬN CÂU HỎI MỚI (BẮT ĐẦU CHƠI)", type="primary"):
        de, da, gy = tao_de_toan_game(lop_chon, bai_chon)
        st.session_state.game_q = {"de": de, "da": da, "gy": gy}
        st.session_state.answered = False

    if st.session_state.game_q:
        st.markdown(f"""
        <div class="problem-box">
            <h2 style='color: #1e3c72;'>{st.session_state.game_q['de']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔊 Nghe đề bài"):
            st.markdown(text_to_speech_html(st.session_state.game_q['de']), unsafe_allow_html=True)

with col2:
    if st.session_state.game_q:
        st.subheader("✍️ Trả lời")
        user_ans = st.number_input("Kết quả của em:", value=0)
        
        if st.button("💎 NỘP BÀI"):
            if user_ans == st.session_state.game_q['da']:
                # Cộng điểm game
                bonus = 10 + (st.session_state.streak * 5)
                st.session_state.user_coins += bonus
                st.session_state.streak += 1
                
                st.balloons()
                st.success(f"CHÍNH XÁC! +{bonus} Xu 💰")
                st.session_state.game_q = None # Xóa câu cũ để sang câu mới
            else:
                st.session_state.streak = 0
                st.error("Chưa đúng rồi! Chuỗi thắng đã bị ngắt.")
                with st.expander("💡 Xem hướng dẫn"):
                    st.write(st.session_state.game_q['gy'])
                    st.info(f"🗣️ H'Mông: {dich_sang_mong_giu_cong_thuc(st.session_state.game_q['gy'])}")

# --- BẢNG XẾP HẠNG TẠM THỜI ---
st.markdown("---")
st.subheader("🏆 Thành tích trong phiên này")
if st.session_state.user_coins > 0:
    st.write(f"Bạn đang sở hữu danh hiệu: **{rank}**")
