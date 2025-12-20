import streamlit as st
import google.generativeai as genai
import sys
import io

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Trợ lý Tin học 9 - Python AI",
    page_icon="🐍",
    layout="wide"
)

# --- KHỞI TẠO BIẾN (Lưu điểm số & trạng thái) ---
if 'user_coins' not in st.session_state:
    st.session_state.user_coins = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

# --- DỮ LIỆU BÀI HỌC CƠ BẢN ---
BAI_HOC = {
    "Bài 1: Hello World": {
        "mota": "Lệnh in ra màn hình đầu tiên",
        "code_mau": "print('Xin chào thế giới!')\nprint('Em yêu Tin học 9')"
    },
    "Bài 2: Biến số & Phép tính": {
        "mota": "Lưu trữ số và tính toán đơn giản",
        "code_mau": "a = 15\nb = 5\ntong = a + b\nhieu = a - b\nprint('Tổng là:', tong)\nprint('Hiệu là:', hieu)"
    },
    "Bài 3: Câu lệnh điều kiện (If-Else)": {
        "mota": "Kiểm tra điều kiện đúng hay sai",
        "code_mau": "diem_so = 8\n\nif diem_so >= 5:\n    print('Chúc mừng! Bạn đã đậu.')\nelse:\n    print('Rất tiếc, bạn cần cố gắng hơn.')"
    },
    "Bài 4: Vòng lặp For": {
        "mota": "Lặp lại một hành động nhiều lần",
        "code_mau": "print('Bảng cửu chương 2:')\nfor i in range(1, 11):\n    ket_qua = 2 * i\n    print('2 x', i, '=', ket_qua)"
    }
}

# --- HÀM GỌI AI GEMINI ---
def goi_gemini(code_input, yeu_cau, api_key):
    try:
        genai.configure(api_key=api_key)
        # Sử dụng model Flash mới nhất cho nhanh và miễn phí
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Bạn là một giáo viên dạy lập trình Python lớp 9 thân thiện, dễ hiểu.
        Học sinh đang viết đoạn code sau:
        ```python
        {code_input}
        ```
        Yêu cầu của học sinh: {yeu_cau}
        
        Hãy trả lời ngắn gọn theo cấu trúc:
        1. ✅ **Nhận xét:** Code đúng hay sai? (Nếu sai chỉ rõ dòng nào).
        2. 📖 **Giải thích:** Giải thích code chạy như thế nào bằng tiếng Việt đơn giản.
        3. 💡 **Gợi ý:** Nếu code đúng, hãy gợi ý một cách viết khác hay hơn hoặc bài tập nâng cao nhỏ.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Lỗi kết nối AI: {str(e)}. (Vui lòng kiểm tra lại API Key)"

# --- GIAO DIỆN THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.title("⚙️ Cài đặt")
    
    # Ô nhập API Key
    api_key_input = st.text_input("🔑 Nhập Gemini API Key", type="password")
    if api_key_input:
        st.session_state.api_key_configured = True
        st.success("Đã nhận Key!")
    
    st.divider()
    
    # Bảng thành tích
    st.subheader("🏆 Thành tích của em")
    st.write(f"💰 Điểm tích lũy: **{st.session_state.user_coins}**")
    st.write(f"🔥 Chuỗi thắng: **{st.session_state.streak}**")
    
    st.divider()
    
    # Menu chọn bài
    st.subheader("📚 Chọn bài mẫu")
    bai_chon = st.selectbox("Danh sách bài học:", list(BAI_HOC.keys()))
    if st.button("Dán code mẫu này vào khung"):
        st.session_state.code_input = BAI_HOC[bai_chon]["code_mau"]
        st.rerun()

# --- GIAO DIỆN CHÍNH ---
st.header("🐍 Trợ lý Lập trình Python Lớp 9")
st.info(f"Đang học: **{bai_chon}** - {BAI_HOC[bai_chon]['mota']}")

# Chia màn hình làm 2 cột
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("⌨️ Khung Soạn Thảo (Code Editor)")
    
    # Lấy code từ session hoặc dùng mặc định
    default_text = st.session_state.get('code_input', "print('Xin chào!')")
    code_input = st.text_area("Viết code Python của em vào đây:", value=default_text, height=350)
    
    # Hàng nút bấm
    c1, c2 = st.columns(2)
    with c1:
        btn_run = st.button("▶️ CHẠY THỬ CODE", type="primary", use_container_width=True)
    with c2:
        btn_ai = st.button("🤖 AI GIẢI THÍCH & SỬA LỖI", use_container_width=True)

    # --- XỬ LÝ CHẠY CODE ---
    if btn_run:
        st.write("---")
        st.markdown("### 🖥️ Kết quả chạy trên màn hình:")
        
        try:
            # 1. Chuẩn bị hứng kết quả in ra (Capture stdout)
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()
            
            # 2. Chạy code
            exec(code_input, {})
            
            # 3. Lấy kết quả
            sys.stdout = old_stdout # Trả lại trạng thái bình thường
            ket_qua = redirected_output.getvalue()
            
            # 4. Kiểm tra xem có kết quả không
            if ket_qua.strip():
                st.code(ket_qua)
                st.success("Chương trình chạy thành công! 🎉")
                st.session_state.user_coins += 2
            else:
                st.warning("⚠️ Code đã chạy xong nhưng không in gì ra cả!")
                st.markdown("""
                **Gợi ý:** Máy tính đã tính xong nhưng em chưa bảo nó in ra.
                👉 Em hãy dùng lệnh `print(...)` để xem kết quả nhé.
                """)
                
        except Exception as e:
            sys.stdout = old_stdout # Trả lại stdout nếu lỗi
            st.error(f"❌ Lỗi cú pháp: {e}")

with col2:
    st.subheader("💬 Phản hồi từ Giáo viên AI")
    
    if btn_ai:
        if not st.session_state.api_key_configured:
            st.warning("⚠️ Em chưa nhập API Key ở thanh bên trái kìa!")
        else:
            with st.spinner("Thầy giáo đang đọc bài của em..."):
                phan_hoi = goi_gemini(code_input, "Kiểm tra code và giải thích", api_key_input)
                
                # Hiển thị kết quả trong khung đẹp
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 1px solid #ddd; color: #333;">
                    {phan_hoi}
                </div>
                """, unsafe_allow_html=True)
                
                # Cộng điểm khuyến khích
                st.session_state.user_coins += 5
                st.toast("Đã cộng +5 điểm chuyên cần! 🎓")

# --- FOOTER ---
st.markdown("---")
st.caption("Ứng dụng được xây dựng với Streamlit & Google Gemini AI.")

