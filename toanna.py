import streamlit as st
import random
from PIL import Image
import google.generativeai as genai

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gia sư Toán AI - Na Ư (Phiên bản Dự thi)",
    page_icon="🎓",
    layout="wide"
)

# --- CẤU HÌNH AI (GOOGLE GEMINI) ---
# Bạn hãy lấy key miễn phí tại: https://aistudio.google.com/app/apikey
# Nếu chưa có key, hệ thống sẽ chạy chế độ cơ bản
GOOGLE_API_KEY = st.sidebar.text_input("🔑 Nhập API Key Google Gemini (để mở khóa tính năng AI cao cấp):", type="password")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash') # Model nhanh và miễn phí

# --- CSS LÀM ĐẸP (GIỮ NGUYÊN VÀ NÂNG CẤP) ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(to bottom right, #f0f2f6, #c2e9fb); }
    .school-header {
        background: linear-gradient(90deg, #0052cc, #003366);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px;
    }
    .success-card { background-color: #d4edda; color: #155724; padding: 15px; border-radius: 10px; border-left: 5px solid #28a745; }
    .ai-response { background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 10px; border-left: 5px solid #ffc107; margin-top: 10px;}
    .stButton>button { border-radius: 25px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# --- HÀM HỖ TRỢ ---

def ask_gemini(prompt, image=None):
    """Hàm gọi AI để giải toán hoặc dịch thuật"""
    if not GOOGLE_API_KEY:
        return "⚠️ Vui lòng nhập API Key để kích hoạt Trí tuệ nhân tạo."
    try:
        if image:
            response = model.generate_content([prompt, image])
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi kết nối AI: {str(e)}"

def sinh_de_co_ban():
    """Sinh đề bằng thuật toán (Chế độ Offline)"""
    a = random.randint(2, 9)
    b = random.randint(1, 20)
    de = f"Tìm x biết: {a}x + {b} = 0"
    dap_an = round(-b/a, 2)
    return de, dap_an

# --- GIAO DIỆN CHÍNH ---

# 1. Header
st.markdown("""
<div class="school-header">
    <h4>SỞ GIÁO DỤC VÀ ĐÀO TẠO TỈNH ĐIỆN BIÊN</h4>
    <h1>🏫 TRƯỜNG PTDTBT THCS NA Ư</h1>
    <h3>🚀 ỨNG DỤNG: TRỢ LÝ HỌC TẬP THÔNG MINH (AI TUTOR)</h3>
    <p><i>Sản phẩm dự thi: "Sáng tạo AI trong giáo dục và đào tạo 2025-2026"</i></p>
</div>
""", unsafe_allow_html=True)

# 2. Sidebar - Bảng điều khiển
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/graduation-cap.png", width=80)
    st.header("🎛️ Trung tâm điều khiển")
    
    mode = st.radio("Chọn chế độ học:", 
        ["🎲 Luyện tập (Sinh đề ngẫu nhiên)", 
         "📷 Mắt thần AI (Giải toán qua ảnh)"])
    
    st.markdown("---")
    st.caption("📊 **Thống kê phiên học:**")
    if 'score' not in st.session_state: st.session_state.score = 0
    st.write(f"Điểm tích lũy: **{st.session_state.score}** ⭐")

# 3. Xử lý theo từng chế độ

# --- CHẾ ĐỘ 1: LUYỆN TẬP (CẢI TIẾN) ---
if mode == "🎲 Luyện tập (Sinh đề ngẫu nhiên)":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Đề bài hôm nay")
        st.info("Chuẩn kiến thức: Đại số lớp 8 - Chương trình GDPT 2018")
        
        if st.button("🔄 Tạo câu hỏi mới"):
            de, da = sinh_de_co_ban()
            st.session_state.current_prob = de
            st.session_state.current_ans = da
            st.session_state.ai_hint = "" # Reset gợi ý
            
        if 'current_prob' in st.session_state:
            st.markdown(f"### {st.session_state.current_prob}")
            
            # Tính năng AI: Gợi ý phương pháp
            if st.button("💡 Xin gợi ý từ AI (Không hiện đáp án)"):
                prompt = f"Hãy đóng vai giáo viên Toán ân cần, gợi ý từng bước cách giải bài toán '{st.session_state.current_prob}' cho học sinh vùng cao dễ hiểu. Tuyệt đối không đưa ra đáp án cuối cùng."
                st.session_state.ai_hint = ask_gemini(prompt)
            
            if 'ai_hint' in st.session_state and st.session_state.ai_hint:
                st.markdown(f"<div class='ai-response'><b>👩‍🏫 Cô giáo AI gợi ý:</b><br>{st.session_state.ai_hint}</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("✍️ Nộp bài")
        user_ans = st.number_input("Nhập kết quả (làm tròn 2 chữ số):", step=0.1)
        
        if st.button("Kiểm tra kết quả"):
            if 'current_ans' in st.session_state:
                if abs(user_ans - st.session_state.current_ans) < 0.1:
                    st.markdown(f"<div class='success-card'>✅ CHÍNH XÁC! Em rất giỏi! (+1 điểm)</div>", unsafe_allow_html=True)
                    st.session_state.score += 1
                    st.balloons()
                else:
                    st.error(f"Tiếc quá! Đáp án đúng là {st.session_state.current_ans}. Hãy thử xem gợi ý nhé!")

# --- CHẾ ĐỘ 2: MẮT THẦN AI (TÍNH NĂNG ĐỘT PHÁ) ---
elif mode == "📷 Mắt thần AI (Giải toán qua ảnh)":
    st.subheader("📸 Chụp ảnh bài toán khó - AI sẽ giúp em!")
    st.caption("Tính năng này sử dụng Thị giác máy tính để đọc đề bài từ sách giáo khoa hoặc vở viết tay.")
    
    # Cho phép nhập bằng Camera hoặc Upload file
    tab1, tab2 = st.tabs(["📸 Chụp trực tiếp", "📂 Tải ảnh lên"])
    
    img_file = None
    
    with tab1:
        cam_img = st.camera_input("Chụp ảnh đề bài tại đây")
        if cam_img: img_file = cam_img
            
    with tab2:
        up_img = st.file_uploader("Hoặc tải ảnh từ máy", type=['png', 'jpg', 'jpeg'])
        if up_img: img_file = up_img

    if img_file:
        st.image(img_file, caption="Ảnh đề bài", width=300)
        
        if st.button("🚀 Gửi cho Gia sư AI phân tích"):
            with st.spinner("Đang đọc đề bài và suy nghĩ..."):
                # Xử lý ảnh
                image = Image.open(img_file)
                
                # Prompt kỹ thuật cho AI
                prompt = """
                1. Hãy đọc đề bài toán trong bức ảnh này.
                2. Giải bài toán này chi tiết, từng bước một.
                3. Giải thích bằng ngôn ngữ đơn giản, thân thiện, phù hợp với học sinh trung học cơ sở.
                4. Cuối cùng, hãy dịch tóm tắt lời giải sang tiếng H'Mông (nếu có thể) hoặc đưa ra lời động viên.
                """
                
                # Gọi Gemini Vision
                loi_giai = ask_gemini(prompt, image)
                
                st.markdown("### 🎓 Lời giải chi tiết:")
                st.write(loi_giai)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    © 2025 Đội thi Chuyển đổi số - Trường PTDTBT THCS Na Ư<br>
    <i>Sản phẩm được hỗ trợ bởi công nghệ Google Gemini AI & Streamlit</i>
</div>
""", unsafe_allow_html=True)
