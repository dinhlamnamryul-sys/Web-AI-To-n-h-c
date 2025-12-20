import streamlit as st
import random
import os
import google.generativeai as genai
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import base64

# --- CẤU HÌNH API GEMINI ---
# Bạn cần thay thế 'YOUR_API_KEY' bằng key thực tế của bạn
# Để an toàn, nên dùng st.secrets trong thực tế
api_key = st.sidebar.text_input("Nhập Gemini API Key", type="password")
if api_key:
    genai.configure(api_key=api_key)

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Trợ lý Tin học 9 - Bản Mường",
    page_icon="💻",
    layout="wide"
)

# --- KHỞI TẠO BIẾN TRÒ CHƠI & LƯỢT TRUY CẬP ---
if 'user_coins' not in st.session_state:
    st.session_state.user_coins = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'code_history' not in st.session_state:
    st.session_state.code_history = []

# --- DỮ LIỆU CHƯƠNG TRÌNH TIN HỌC 9 (PYTHON) ---
CHUONG_TRINH_HOC = {
    "Bài 1: Làm quen": {"Hello World": "In ra màn hình câu chào", "Biến số": "Khái niệm biến nhớ"},
    "Bài 2: Cấu trúc rẽ nhánh": {"If...Else": "Câu lệnh điều kiện", "So sánh": "Các phép so sánh"},
    "Bài 3: Vòng lặp": {"For": "Lặp với số lần biết trước", "While": "Lặp với điều kiện"},
}

# --- PHONG CÁCH GIAO DIỆN (CSS) ---
st.markdown("""
<style>
    .game-card {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin-bottom: 20px;
    }
    .ai-response {
        background-color: #f0f2f6; padding: 20px; border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    .stTextArea textarea {
        background-color: #262730;
        color: #00ff00; /* Màu chữ code kiểu hacker */
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- HÀM HỖ TRỢ GAME & AI ---
def get_rank_info(coins):
    if coins < 50: return "Lập trình viên tập sự 👶", "💻 Máy tính cũ"
    elif coins < 150: return "Coder triển vọng 🚀", "🚀 Laptop Gaming"
    elif coins < 300: return "Kỹ sư phần mềm 🛠️", "☁️ Cloud Server"
    else: return "Chuyên gia AI 🤖", "🧠 Siêu máy tính Na Ư"

def text_to_speech_html(text):
    try:
        tts = gTTS(text=text, lang='vi')
        fp = io.BytesIO(); tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        return f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
    except: return ""

def goi_gemini_giai_thich(code_input, yeu_cau):
    """Hàm gửi code lên Gemini để xử lý"""
    if not api_key:
        return "⚠️ Em chưa nhập API Key! Hãy nhập ở thanh bên trái nhé."
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        # Prompt kỹ thuật (Prompt Engineering) để AI đóng vai giáo viên
        prompt = f"""
        Bạn là một trợ lý ảo dạy lập trình Python cho học sinh lớp 9 vùng cao (dễ hiểu, thân thiện).
        Học sinh đang hỏi về đoạn code sau:
        ```python
        {code_input}
        ```
        Yêu cầu: {yeu_cau}
        Hãy trả lời ngắn gọn, vui vẻ. Nếu code lỗi, hãy chỉ ra lỗi sai và gợi ý sửa (đừng sửa hết ngay).
        Cuối cùng, hãy dịch một câu tóm tắt quan trọng nhất sang tiếng H'Mông.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi kết nối AI: {e}"

# --- GIAO DIỆN SIDEBAR ---
with st.sidebar:
    rank, pet = get_rank_info(st.session_state.user_coins)
    st.markdown(f"""
    <div class="game-card">
        <div style="font-size: 50px;">{rank.split()[0]}</div>
        <h3>{rank}</h3>
        <p>{pet}</p>
        <div class="coin-text">💰 {st.session_state.user_coins} Bit</div>
        <div class="streak-text">🔥 Chuỗi: {st.session_state.streak}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("📚 MENU BÀI HỌC")
    bai_lon = st.selectbox("Chủ đề:", list(CHUONG_TRINH_HOC.keys()))
    bai_nho = st.selectbox("Bài chi tiết:", list(CHUONG_TRINH_HOC[bai_lon].keys()))
    st.info(f"Nội dung: {CHUONG_TRINH_HOC[bai_lon][bai_nho]}")

# --- GIAO DIỆN CHÍNH ---
st.title("💻 Phòng Lab Tin Học 9 - AI Assistant")
st.caption("Gõ code Python vào bên dưới, Trợ lý AI sẽ giúp em kiểm tra và giải thích!")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("⌨️ Khung Soạn Thảo (Code Editor)")
    # Code mẫu mặc định
    default_code = "print('Chao mung cac ban den voi Na U!')\n# Em hay thu tinh tong 2 so tai day"
    user_code = st.text_area("Nhập code Python của em:", value=default_code, height=300)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        check_btn = st.button("🔍 Nhờ AI Sửa Lỗi/Giải Thích", type="primary")
    with col_btn2:
        run_btn = st.button("▶️ Chạy thử (Giả lập)")

with col2:
    st.subheader("🤖 Trợ lý Robot AI")
    
    if check_btn and user_code:
        with st.spinner("Robot đang đọc code của em..."):
            # Gọi hàm AI
            ai_reply = goi_gemini_giai_thich(user_code, "Giải thích code và tìm lỗi sai (nếu có)")
            
            st.markdown(f'<div class="ai-response">{ai_reply}</div>', unsafe_allow_html=True)
            
            # Logic cộng điểm đơn giản khi tương tác
            st.session_state.user_coins += 5
            st.session_state.streak += 1
            st.toast("Cộng +5 Bit vào tài khoản! 💰")

    elif run_btn:
        # Giả lập chạy code (Streamlit không chạy trực tiếp code user vì lý do bảo mật, 
        # nhưng có thể dùng exec() với rủi ro cao hoặc hiển thị kết quả giả định từ AI)
        try:
            # LƯU Ý: Dùng exec() trong môi trường thật rất nguy hiểm. 
            # Ở đây dùng output từ AI để giả lập kết quả chạy thì an toàn hơn.
            # Nhưng để demo đơn giản, tôi dùng capture stdout
            import sys
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            exec(user_code)
            sys.stdout = old_stdout
            ket_qua = redirected_output.getvalue()
            st.success("Kết quả chạy chương trình:")
            st.code(ket_qua)
        except Exception as e:
            st.error(f"Chương trình bị lỗi rồi: {e}")

# --- PHẦN GIẢI TRÍ / KIẾN THỨC ---
st.markdown("---")
st.info("💡 Mẹo nhỏ: Em có thể hỏi Robot cách dùng vòng lặp `for` để vẽ hình tam giác đấy!")
