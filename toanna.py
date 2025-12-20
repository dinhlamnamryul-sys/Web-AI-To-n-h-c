import streamlit as st
import google.generativeai as genai
import sys
import io
import time

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Học Python Lớp 9 - AI Fast",
    page_icon="⚡",
    layout="wide"
)

# --- KHỞI TẠO BIẾN (SESSION STATE) ---
if 'user_coins' not in st.session_state:
    st.session_state.user_coins = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

# --- DỮ LIỆU BÀI HỌC ---
BAI_HOC = {
    "Bài 1: Hello World": {
        "mota": "Lệnh in ra màn hình đầu tiên",
        "code_mau": "print('Xin chào lớp 9A!')"
    },
    "Bài 2: Biến số": {
        "mota": "Lưu trữ dữ liệu vào bộ nhớ",
        "code_mau": "ten = 'Na Ư'\ntuoi = 15\nprint('Trường:', ten)\nprint('Tuổi:', tuoi)"
    },
    "Bài 3: Tính toán": {
        "mota": "Cộng trừ nhân chia cơ bản",
        "code_mau": "a = 10\nb = 5\ntong = a + b\nprint('Tổng hai số là:', tong)"
    },
    "Bài 4: Vòng lặp For": {
        "mota": "Lặp lại hành động",
        "code_mau": "print('Đếm số:')\nfor i in range(1, 6):\n    print('Số thứ:', i)"
    }
}

# --- HÀM GỌI AI (CHẾ ĐỘ STREAMING) ---
def stream_gemini(code_input, yeu_cau, api_key):
    """Hàm này trả về từng từ một (Generator) thay vì trả cả đoạn"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Bạn là giáo viên Tin học lớp 9 thân thiện.
        Học sinh viết code:
        ```python
        {code_input}
        ```
        Yêu cầu: {yeu_cau}
        
        Hãy trả lời ngắn gọn, chia thành các ý:
        1. ✅ Nhận xét (Đúng/Sai)
        2. 📖 Giải thích code chạy thế nào (Dễ hiểu)
        3. 💡 Gợi ý sửa hoặc nâng cao
        """
        
        # stream=True là chìa khóa để chạy nhanh
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
                
    except Exception as e:
        yield f"⚠️ Lỗi kết nối: {str(e)}"

# --- SIDEBAR (THANH BÊN) ---
with st.sidebar:
    st.header("⚙️ Cài đặt")
    api_key_input = st.text_input("🔑 Nhập API Key", type="password")
    if api_key_input:
        st.session_state.api_key_configured = True
    
    st.markdown("---")
    st.subheader("🏆 Bảng Vàng")
    st.write(f"💰 Xu tích lũy: **{st.session_state.user_coins}**")
    st.write(f"🔥 Chuỗi thắng: **{st.session_state.streak}**")
    
    st.markdown("---")
    st.subheader("📚 Chọn Bài Mẫu")
    bai_chon = st.selectbox("Bài học:", list(BAI_HOC.keys()))
    if st.button("📝 Nạp code mẫu"):
        st.session_state.code_input = BAI_HOC[bai_chon]["code_mau"]
        st.rerun()

# --- GIAO DIỆN CHÍNH ---
st.header("⚡ Trợ lý Python Lớp 9 (AI Tốc Độ Cao)")
st.caption(f"Đang học: {BAI_HOC[bai_chon]['mota']}")

col1, col2 = st.columns([1.3, 1])

with col1:
    st.subheader("⌨️ Nhập Code")
    default_text = st.session_state.get('code_input', "print('Xin chào!')")
    code_input = st.text_area("Code của em:", value=default_text, height=350)
    
    c1, c2 = st.columns(2)
    with c1:
        btn_run = st.button("▶️ CHẠY CODE", type="primary", use_container_width=True)
    with c2:
        btn_ai = st.button("🤖 AI GIẢI THÍCH", use_container_width=True)

    # XỬ LÝ CHẠY CODE
    if btn_run:
        st.write("---")
        st.markdown("**🖥️ Kết quả chạy:**")
        try:
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            
            # Chạy code
            exec(code_input, {})
            
            sys.stdout = old_stdout
            ket_qua = redirected_output.getvalue()
            
            if ket_qua.strip():
                st.code(ket_qua)
                st.success("Tuyệt vời! Code chạy tốt.")
                st.session_state.user_coins += 2
            else:
                st.warning("⚠️ Code chạy xong nhưng không hiện gì cả!")
                st.info("💡 Gợi ý: Em nhớ dùng lệnh `print(...)` nhé.")
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"❌ Lỗi: {e}")

with col2:
    st.subheader("💬 Phản hồi AI")
    
    # Khung chứa nội dung AI
    chat_container = st.container(border=True)
    
    if btn_ai:
        if not st.session_state.api_key_configured:
            st.warning("⚠️ Hãy nhập API Key trước nhé!")
        else:
            with chat_container:
                # Dùng st.write_stream để hiển thị hiệu ứng gõ chữ
                try:
                    stream_obj = stream_gemini(code_input, "Giải thích code", api_key_input)
                    st.write_stream(stream_obj)
                    
                    # Cộng điểm
                    st.session_state.user_coins += 5
                    st.toast("Đã cộng +5 Xu! 🎓")
                except Exception as e:
                    st.error("Lỗi khi gọi AI.")
    else:
        with chat_container:
            st.write("🤖 *Thầy giáo AI đang chờ em hỏi bài...*")

# --- FOOTER ---
st.markdown("---")
st.caption("Phiên bản v3: Tối ưu tốc độ phản hồi (Streaming Response).")

