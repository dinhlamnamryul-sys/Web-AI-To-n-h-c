import streamlit as st
import google.generativeai as genai
import sys
import io
import time

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Học Lập Trình Python Lớp 9",
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

# --- DỮ LIỆU BÀI HỌC (Nội dung chung) ---
BAI_HOC = {
    "Bài 1: Hello World": {
        "mota": "Lệnh in ra màn hình đầu tiên",
        "code_mau": "print('Xin chào các bạn!')\nprint('Chúc một ngày tốt lành')"
    },
    "Bài 2: Biến số": {
        "mota": "Lưu trữ dữ liệu vào bộ nhớ",
        "code_mau": "ten_truong = 'THCS Ngôi Sao'\nnam_hoc = 2025\nprint('Trường:', ten_truong)\nprint('Năm học:', nam_hoc)"
    },
    "Bài 3: Tính toán": {
        "mota": "Cộng trừ nhân chia cơ bản",
        "code_mau": "chieu_dai = 20\nchieu_rong = 10\ndien_tich = chieu_dai * chieu_rong\nprint('Diện tích hình chữ nhật là:', dien_tich)"
    },
    "Bài 4: Vòng lặp For": {
        "mota": "Lặp lại hành động",
        "code_mau": "print('Đếm ngược:')\nfor i in range(10, 0, -1):\n    print(i)\nprint('Chúc mừng năm mới!')"
    }
}

# --- HÀM GỌI AI (CHẾ ĐỘ STREAMING) ---
def stream_gemini(code_input, yeu_cau, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Bạn là một trợ lý ảo hỗ trợ học lập trình Python cho học sinh cấp 2.
        Học sinh đang viết đoạn code sau:
        ```python
        {code_input}
        ```
        Yêu cầu: {yeu_cau}
        
        Hãy trả lời ngắn gọn, thân thiện và dễ hiểu.
        Cấu trúc trả lời:
        1. ✅ Nhận xét (Code đúng hay sai)
        2. 📖 Giải thích (Code hoạt động thế nào)
        3. 💡 Gợi ý (Cách viết tốt hơn nếu có)
        """
        
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
                
    except Exception as e:
        yield f"⚠️ Lỗi kết nối: {str(e)}"

# --- SIDEBAR (THANH BÊN) ---
with st.sidebar:
    st.header("⚙️ Cài đặt hệ thống")
    
    # --- PHẦN HƯỚNG DẪN LẤY KEY (MỚI THÊM) ---
    with st.expander("❓ Chưa có Key? Xem hướng dẫn"):
        st.markdown("""
        **Cách lấy API Key miễn phí (Google):**
        1. Truy cập [Google AI Studio](https://aistudio.google.com/).
        2. Đăng nhập bằng Gmail.
        3. Nhấn nút **Get API key** (góc trái).
        4. Nhấn **Create API key**.
        5. Copy đoạn mã (bắt đầu bằng `AIza...`) và dán vào ô bên dưới.
        """)
    
    api_key_input = st.text_input("🔑 Nhập API Key", type="password")
    if api_key_input:
        st.session_state.api_key_configured = True
    
    st.markdown("---")
    st.subheader("🏆 Thống kê")
    st.write(f"💰 Điểm thưởng: **{st.session_state.user_coins}**")
    st.write(f"🔥 Chuỗi hoàn thành: **{st.session_state.streak}**")
    
    st.markdown("---")
    st.subheader("📚 Thư viện Code mẫu")
    bai_chon = st.selectbox("Chọn bài học:", list(BAI_HOC.keys()))
    if st.button("📝 Nạp code mẫu vào khung"):
        st.session_state.code_input = BAI_HOC[bai_chon]["code_mau"]
        st.rerun()

# --- GIAO DIỆN CHÍNH ---
st.header("💻 Trợ lý Lập trình Python (Lớp 9)")
st.caption(f"Chủ đề hiện tại: {BAI_HOC[bai_chon]['mota']}")

col1, col2 = st.columns([1.3, 1])

with col1:
    st.subheader("⌨️ Khung Soạn Thảo Code")
    default_text = st.session_state.get('code_input', "print('Xin chào!')")
    code_input = st.text_area("Nhập code của bạn:", value=default_text, height=350)
    
    c1, c2 = st.columns(2)
    with c1:
        btn_run = st.button("▶️ CHẠY CODE", type="primary", use_container_width=True)
    with c2:
        btn_ai = st.button("🤖 AI PHÂN TÍCH CODE", use_container_width=True)

    # XỬ LÝ CHẠY CODE
    if btn_run:
        st.write("---")
        st.markdown("**🖥️ Kết quả hiển thị (Output):**")
        try:
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            
            # Chạy code
            exec(code_input, {})
            
            sys.stdout = old_stdout
            ket_qua = redirected_output.getvalue()
            
            if ket_qua.strip():
                st.code(ket_qua)
                st.success("Chương trình thực thi thành công!")
                st.session_state.user_coins += 2
            else:
                st.warning("⚠️ Code đã chạy nhưng không có dữ liệu in ra màn hình.")
                st.info("💡 Gợi ý: Hãy sử dụng lệnh `print(...)` để hiển thị kết quả.")
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"❌ Lỗi cú pháp: {e}")

with col2:
    st.subheader("💬 Trợ lý ảo AI")
    
    chat_container = st.container(border=True)
    
    if btn_ai:
        if not st.session_state.api_key_configured:
            st.warning("⚠️ Vui lòng nhập API Key để sử dụng tính năng AI.")
        else:
            with chat_container:
                try:
                    stream_obj = stream_gemini(code_input, "Giải thích code và kiểm tra lỗi", api_key_input)
                    st.write_stream(stream_obj)
                    
                    st.session_state.user_coins += 5
                    st.session_state.streak += 1
                except Exception as e:
                    st.error("Đã xảy ra lỗi khi kết nối với AI.")
    else:
        with chat_container:
            st.write("🤖 *Kết quả phân tích từ AI sẽ hiển thị tại đây...*")

# --- FOOTER ---
st.markdown("---")
st.caption("Ứng dụng hỗ trợ học tập Tin học 9 - Tích hợp Gemini AI.")
