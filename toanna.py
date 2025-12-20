import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import base64
import sys

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Học Python cùng AI - Bản Mường",
    page_icon="💻",
    layout="wide"
)

# --- KHỞI TẠO BIẾN (SESSION STATE) ---
if 'user_coins' not in st.session_state:
    st.session_state.user_coins = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

# --- DỮ LIỆU BÀI HỌC (MẪU) ---
BAI_HOC = {
    "Bài 1: Làm quen": {
        "mota": "Lệnh in ra màn hình",
        "code_mau": "print('Xin chào Na Ư!')"
    },
    "Bài 2: Biến số": {
        "mota": "Lưu trữ dữ liệu",
        "code_mau": "ten_truong = 'Na Ư'\nso_hoc_sinh = 45\nprint(ten_truong)\nprint(so_hoc_sinh)"
    },
    "Bài 3: Phép toán": {
        "mota": "Cộng trừ nhân chia",
        "code_mau": "a = 10\nb = 5\ntong = a + b\nprint('Tổng là:', tong)"
    },
    "Bài 4: Vòng lặp For": {
        "mota": "Lặp lại hành động",
        "code_mau": "for i in range(5):\n    print('Mình yêu Tin học', i)"
    }
}

# --- CÁC HÀM CHỨC NĂNG ---

def get_rank_info(coins):
    """Xếp hạng dựa trên số xu"""
    if coins < 50: return "Tập sự 👶", "Gà con chăm chỉ"
    elif coins < 150: return "Trợ lý nhỏ 🛠️", "Sóc rừng nhanh nhẹn"
    elif coins < 300: return "Kỹ sư Code 🚀", "Đại bàng núi"
    else: return "Trạng Nguyên AI 👑", "Rồng thiêng Na Ư"

def text_to_speech_html(text):
    """Chuyển văn bản thành giọng nói"""
    try:
        tts = gTTS(text=text, lang='vi')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        return f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
    except: return ""

def goi_gemini(code_input, yeu_cau, api_key):
    """Hàm gọi AI Gemini 1.5 Flash"""
    try:
        genai.configure(api_key=api_key)
        # SỬ DỤNG MODEL 1.5 FLASH (Mới nhất, nhanh, free tier tốt)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Bạn là một thầy giáo dạy Tin học lớp 9 tại vùng cao Việt Nam. 
        Học sinh vừa viết đoạn code Python sau:
        ```python
        {code_input}
        ```
        Yêu cầu của học sinh: {yeu_cau}
        
        Hãy trả lời theo cấu trúc sau:
        1. 🧐 **Nhận xét:** Đúng hay sai? Nếu sai thì sai ở đâu (giải thích thật dễ hiểu).
        2. 💡 **Giải thích:** Code này hoạt động như thế nào (dùng ngôn ngữ tự nhiên).
        3. 🗣️ **Tiếng H'Mông:** Dịch một câu thông điệp khích lệ hoặc từ khóa quan trọng trong code sang tiếng H'Mông (Ví dụ: "Cố lên" -> "Ua siab", "Học tốt" -> "Kawm zoo").
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi kết nối AI: {e}. (Hãy kiểm tra lại API Key nhé!)"

# --- GIAO DIỆN: THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Cài đặt")
    
    # Nhập API Key
    api_key_input = st.text_input("🔑 Nhập Gemini API Key", type="password", help="Nhập key từ Google AI Studio")
    if api_key_input:
        st.session_state.api_key_configured = True
    
    st.markdown("---")
    
    # Hiển thị Rank
    rank, pet = get_rank_info(st.session_state.user_coins)
    st.markdown(f"""
    <div style="background-color: #262730; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #4CAF50;">
        <h2>{rank}</h2>
        <p>Linh vật: <b>{pet}</b></p>
        <h1 style="color: #FFD700;">{st.session_state.user_coins} 💰</h1>
        <p>Chuỗi thắng: {st.session_state.streak} 🔥</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("📚 Sổ tay Code")
    bai_chon = st.selectbox("Chọn bài mẫu:", list(BAI_HOC.keys()))
    if st.button("Dán code mẫu này"):
        st.session_state.code_input = BAI_HOC[bai_chon]["code_mau"]
        st.rerun()

# --- GIAO DIỆN: MÀN HÌNH CHÍNH ---
st.title("🏫 Phòng Lab Tin Học 9 - Na Ư")
st.caption(f"Bài đang chọn: {bai_chon} - {BAI_HOC[bai_chon]['mota']}")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("⌨️ Nhập Code Python")
    
    # Khu vực nhập code (có hỗ trợ lấy từ session state nếu chọn bài mẫu)
    default_code = st.session_state.get('code_input', "print('Chao lop 9A!')")
    code_input = st.text_area("Viết code vào đây:", value=default_code, height=300)
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        btn_run = st.button("▶️ CHẠY CODE", type="primary", use_container_width=True)
    with col_b2:
        btn_ai = st.button("🤖 AI GIẢI THÍCH", use_container_width=True)

    # Xử lý: Chạy Code (Exec)
    if btn_run:
        st.markdown("### 🖥️ Kết quả chạy:")
        try:
            # Bắt đầu bắt output
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            
            # Chạy code an toàn trong phạm vi cục bộ
            exec(code_input, {})
            
            # Lấy output và trả lại stdout
            sys.stdout = old_stdout
            ket_qua = redirected_output.getvalue()
            
            if ket_qua:
                st.code(ket_qua)
                st.success("Chương trình chạy thành công!")
                st.balloons()
                st.session_state.user_coins += 2 # Cộng ít điểm khi chạy đúng
            else:
                st.info("Chương trình chạy nhưng không in gì ra màn hình cả (Thiếu lệnh print?)")
                
        except Exception as e:
            sys.stdout = old_stdout # Trả lại stdout nếu lỗi
            st.error(f"⚠️ Lỗi cú pháp: {e}")

with col2:
    st.subheader("💬 Trợ lý ảo (Gemini)")
    
    if btn_ai:
        if not st.session_state.api_key_configured:
            st.warning("⚠️ Vui lòng nhập API Key ở thanh bên trái trước!")
        else:
            with st.spinner("Thầy giáo AI đang xem bài..."):
                phan_hoi = goi_gemini(code_input, "Giải thích và sửa lỗi giúp em", api_key_input)
                st.markdown(f"""
                <div style="background-color: #f0f2f6; color: black; padding: 15px; border-radius: 10px; border-left: 5px solid #FF4B4B;">
                    {phan_hoi}
                </div>
                """, unsafe_allow_html=True)
                
                # Cộng điểm nhiều khi chịu khó học hỏi
                st.session_state.user_coins += 5
                st.session_state.streak += 1
                st.toast("Cộng +5 Xu vì tinh thần học hỏi! 🎓")
                
                # Đọc to kết quả (nếu muốn) - Uncomment dòng dưới để bật
                # st.markdown(text_to_speech_html(phan_hoi[:200]), unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Ứng dụng hỗ trợ học tập môn Tin học 9 - Chương trình GDPT mới.")

