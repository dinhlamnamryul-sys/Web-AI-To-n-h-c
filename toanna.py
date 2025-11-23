import streamlit as st
import random
import math
from deep_translator import GoogleTranslator

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gia sư Toán AI - Bản Mường (Lớp 1-9)",
    page_icon="🏔️",
    layout="wide"
)

# --- DỮ LIỆU CHƯƠNG TRÌNH HỌC ---
CHUONG_TRINH_HOC = {
    "Lớp 1": {
        "Chương 1: Các số từ 0 đến 10": ["Các số 0-10", "So sánh số"],
        "Chương 3: Phép cộng, trừ phạm vi 10": ["Cộng trong phạm vi 10", "Trừ trong phạm vi 10"]
    },
    "Lớp 2": {
        "Chương 4: Phép nhân, Phép chia": ["Bảng nhân 2, 5", "Bảng chia 2, 5"]
    },
    "Lớp 3": {
        "Chương 4: Diện tích": ["Diện tích hình chữ nhật", "Diện tích hình vuông"]
    },
    "Lớp 4": {
        "Chương 4: Phân số": ["Cộng phân số", "Nhân phân số"]
    },
    "Lớp 5": {
        "Chương 2: Số thập phân": ["Cộng số thập phân", "Nhân số thập phân"]
    },
    "Lớp 6": {
        "Chương 1: Số tự nhiên": ["Lũy thừa", "Thứ tự thực hiện phép tính"]
    },
    "Lớp 7": {
        "Chương 1: Số hữu tỉ": ["Cộng trừ số hữu tỉ", "Lũy thừa số hữu tỉ"],
        "Chương 2: Số thực": ["Căn bậc hai số học", "Làm tròn số"]
    },
    "Lớp 8": {
        "Chương 1: Đa thức": ["Nhân đơn thức với đa thức", "Nhân đa thức với đa thức", "Hằng đẳng thức (Bình phương tổng/hiệu)", "Hằng đẳng thức (Hiệu hai bình phương)"],
    },
    "Lớp 9": {
        "Chương 1: Hệ phương trình": ["Giải hệ phương trình"],
        "Chương 3: Căn thức": ["Căn bậc hai", "Trục căn thức"]
    }
}

# --- CSS PHONG CÁCH THỔ CẨM H'MÔNG ---
st.markdown("""
<style>
    /* Font chữ thân thiện */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    /* Nền chính màu chàm nhạt */
    .stApp {
        background-color: #f3f6fb;
        background-image: radial-gradient(#dbeafe 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* Header phong cách Thổ cẩm */
    .hmong-header {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%); /* Màu chàm */
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border-bottom: 5px solid #d32f2f; /* Viền đỏ thổ cẩm */
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        position: relative;
    }
    
    /* Họa tiết giả lập CSS */
    .hmong-pattern {
        height: 10px;
        background: repeating-linear-gradient(
            45deg,
            #d32f2f,
            #d32f2f 10px,
            #ffeb3b 10px,
            #ffeb3b 20px,
            #388e3c 20px,
            #388e3c 30px
        );
        margin-top: 10px;
        border-radius: 5px;
    }

    /* Khung câu hỏi */
    .problem-box {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #e0e0e0;
        border-top: 8px solid #1a237e; /* Màu chàm */
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }

    /* Nút bấm đẹp */
    .stButton>button {
        background: linear-gradient(to right, #d32f2f, #c62828); /* Màu đỏ Hmong */
        color: white;
        border: none;
        border-radius: 30px;
        font-weight: bold;
        font-size: 16px;
        padding: 0.6rem 2rem;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        color: white;
    }

    /* Đáp án trắc nghiệm */
    .stRadio > div {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #eeeeee;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC SINH ĐỀ (CORE) ---

def format_poly(a, x_pow):
    """Helper format đa thức: 1x -> x, -1x -> -x, 0x -> ''"""
    if a == 0: return ""
    sign = "+ " if a > 0 else "- "
    abs_a = abs(a)
    coeff = "" if abs_a == 1 and x_pow > 0 else str(abs_a)
    var = f"x^{x_pow}" if x_pow > 1 else ("x" if x_pow == 1 else "")
    return f"{sign}{coeff}{var} "

def tao_de_toan(lop, bai_hoc):
    """
    Trả về: 
    - de_latex: Chuỗi hiển thị câu hỏi
    - type: 'number' (nhập số) hoặc 'mcq' (trắc nghiệm)
    - dap_an: Đáp án đúng (số hoặc string)
    - options: Danh sách đáp án trắc nghiệm (nếu type='mcq')
    - goi_y_latex: Gợi ý
    """
    de_latex = ""
    question_type = "number" # Mặc định là nhập số
    dap_an = 0
    options = []
    goi_y_text = ""
    goi_y_latex = ""

    # === XỬ LÝ RIÊNG CHO LỚP 8 (ĐẠI SỐ) ===
    if "Lớp 8" in lop:
        question_type = "mcq" # Chuyển sang trắc nghiệm cho Lớp 8
        
        if "Nhân đơn thức" in bai_hoc:
            # a*x * (bx + c)
            a = random.choice([-3, -2, 2, 3, 4])
            b = random.choice([-3, -2, 2, 3, 4])
            c = random.choice([-5, -4, -3, 2, 3, 4, 5])
            
            de_latex = f"Thực hiện phép tính: ${a}x( {b}x {c:+d} )$"
            
            # Đáp án đúng: ab x^2 + ac x
            res_a = a * b
            res_b = a * c
            ans_correct = f"{res_a}x^2 {res_b:+d}x"
            dap_an = ans_correct
            
            # Tạo đáp án nhiễu
            options = [
                ans_correct,
                f"{res_a}x^2 {-res_b:+d}x", # Sai dấu
                f"{res_a}x {res_b:+d}",      # Sai bậc
                f"{res_a + 2}x^2 {res_b:+d}x" # Sai hệ số
            ]
            goi_y_text = "Nhân đơn thức vào từng hạng tử của đa thức:"
            goi_y_latex = f"{a}x \\cdot {b}x + {a}x \\cdot ({c}) = {res_a}x^2 {res_b:+d}x"

        elif "Nhân đa thức" in bai_hoc:
            # (x + a)(x + b) = x^2 + (a+b)x + ab
            a = random.randint(1, 5) * random.choice([-1, 1])
            b = random.randint(1, 5) * random.choice([-1, 1])
            
            de_latex = f"Thực hiện phép tính: $(x {a:+d})(x {b:+d})$"
            
            term_x = a + b
            term_free = a * b
            ans_correct = f"x^2 {term_x:+d}x {term_free:+d}"
            dap_an = ans_correct
            
            options = [
                ans_correct,
                f"x^2 {term_x:+d}x {-term_free:+d}", # Sai dấu số hạng tự do
                f"x^2 {-term_x:+d}x {term_free:+d}", # Sai dấu hệ số x
                f"x^2 {term_free:+d}x {term_x:+d}"   # Nhầm lẫn a+b và ab
            ]
            goi_y_text = "Nhân từng hạng tử của đa thức này với đa thức kia:"
            goi_y_latex = f"x \\cdot x + x \\cdot {b} + {a} \\cdot x + {a} \\cdot {b}"

        elif "Hằng đẳng thức (Bình phương" in bai_hoc:
            # (ax + b)^2
            a = random.choice([1, 2]) # Giữ đơn giản
            b = random.randint(1, 5)
            sign = random.choice(["+", "-"])
            
            if sign == "+":
                de_latex = f"Khai triển: $({a if a>1 else ''}x + {b})^2$"
                res_a = a**2
                res_b = 2*a*b
                res_c = b**2
                ans_correct = f"{res_a if res_a>1 else ''}x^2 + {res_b}x + {res_c}"
                options = [
                    ans_correct,
                    f"{res_a if res_a>1 else ''}x^2 + {res_c}", # Thiếu 2ab
                    f"{res_a if res_a>1 else ''}x^2 - {res_b}x + {res_c}", # Sai dấu
                    f"{a if a>1 else ''}x^2 + {res_b}x + {res_c}" # Quên bình phương a
                ]
                goi_y_text = "Dùng hằng đẳng thức $(A+B)^2 = A^2 + 2AB + B^2$"
            else:
                de_latex = f"Khai triển: $({a if a>1 else ''}x - {b})^2$"
                res_a = a**2
                res_b = 2*a*b
                res_c = b**2
                ans_correct = f"{res_a if res_a>1 else ''}x^2 - {res_b}x + {res_c}"
                options = [
                    ans_correct,
                    f"{res_a if res_a>1 else ''}x^2 - {res_c}", # Thiếu 2ab
                    f"{res_a if res_a>1 else ''}x^2 + {res_b}x + {res_c}", # Sai dấu
                    f"{res_a if res_a>1 else ''}x^2 - {b}x + {res_c}" # Sai hệ số giữa
                ]
                goi_y_text = "Dùng hằng đẳng thức $(A-B)^2 = A^2 - 2AB + B^2$"
            
            dap_an = ans_correct
            goi_y_latex = ""

        else: # Hiệu hai bình phương
            # (x-a)(x+a)
            a = random.randint(2, 6)
            de_latex = f"Khai triển: $(x - {a})(x + {a})$"
            ans_correct = f"x^2 - {a**2}"
            dap_an = ans_correct
            options = [
                ans_correct,
                f"x^2 + {a**2}",
                f"x^2 - {a*2}",
                f"(x-{a})^2"
            ]
            goi_y_text = "Dùng hằng đẳng thức $(A-B)(A+B) = A^2 - B^2$"
            
        # Trộn đáp án trắc nghiệm
        random.shuffle(options)
        return de_latex, question_type, dap_an, options, goi_y_text, goi_y_latex

    # === CÁC LỚP KHÁC (GIỮ NGUYÊN LOGIC SỐ HỌC CƠ BẢN) ===
    # (Code rút gọn cho các phần đã ổn định để tập trung vào Lớp 8)
    a, b = random.randint(1, 10), random.randint(1, 10) # Default fallback
    if "Lớp 1" in lop:
        a, b = random.randint(1, 5), random.randint(1, 5)
        de_latex = f"Tính: ${a} + {b} = ?$"
        dap_an = a + b
    elif "Lớp 7" in lop and "Căn" in bai_hoc:
        kq = random.randint(2, 12)
        de_latex = f"Tính: $\\sqrt{{{kq**2}}} = ?$"
        dap_an = kq
    elif "Lớp 6" in lop and "Lũy thừa" in bai_hoc:
        base, exp = random.randint(2, 5), 2
        de_latex = f"Tính: ${base}^{exp} = ?$"
        dap_an = base**exp
    else: # Fallback chung
        de_latex = f"Tính: ${a} + {b} = ?$"
        dap_an = a+b
        
    return de_latex, "number", dap_an, [], "Tính toán cơ bản", ""

# Hàm dịch thuật
def dich_sang_mong(text):
    try:
        clean_text = text.replace("$", "").replace("\\", "")
        return GoogleTranslator(source='vi', target='hmn').translate(clean_text)
    except:
        return "..."

# --- GIAO DIỆN CHÍNH ---

# 1. Header
st.markdown('<div class="hmong-header">', unsafe_allow_html=True)
st.markdown('<h3>SỞ GIÁO DỤC VÀ ĐÀO TẠO TỈNH ĐIỆN BIÊN</h3>', unsafe_allow_html=True)
st.markdown('<h1>🏫 TRƯỜNG PTDTBT TH&THCS NA Ư</h1>', unsafe_allow_html=True)
st.markdown('<h2>🚀 GIA SƯ TOÁN AI - BẢN MƯỜNG</h2>', unsafe_allow_html=True)
st.markdown('<div class="hmong-pattern"></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 2. Sidebar
with st.sidebar:
    # Logo hoặc icon
    st.markdown("<div style='text-align: center; font-size: 80px;'>🏔️</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("📚 CHỌN BÀI HỌC")
    
    ds_lop = list(CHUONG_TRINH_HOC.keys())
    lop_chon = st.selectbox("Lớp:", ds_lop)
    
    du_lieu_lop = CHUONG_TRINH_HOC[lop_chon]
    ds_chuong = list(du_lieu_lop.keys())
    chuong_chon = st.selectbox("Chương:", ds_chuong)
    
    ds_bai = du_lieu_lop[chuong_chon]
    bai_chon = st.selectbox("Bài học:", ds_bai)
    
    if st.button("🔄 Đặt lại"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# 3. Khu vực chính
col_trai, col_phai = st.columns([1.6, 1])

# Init Session
if 'de_bai' not in st.session_state:
    st.session_state.de_bai = ""
    st.session_state.q_type = "number"
    st.session_state.dap_an = 0
    st.session_state.options = []
    st.session_state.goi_y_text = ""
    st.session_state.goi_y_latex = ""
    st.session_state.show_hint = False

def click_sinh_de():
    # Sinh đề mới
    db, qt, da, ops, gyt, gyl = tao_de_toan(lop_chon, bai_chon)
    st.session_state.de_bai = db
    st.session_state.q_type = qt
    st.session_state.dap_an = da
    st.session_state.options = ops
    st.session_state.goi_y_text = gyt
    st.session_state.goi_y_latex = gyl
    st.session_state.show_hint = False
    st.session_state.submitted = False # Reset trạng thái nộp

with col_trai:
    st.subheader(f"📖 {bai_chon}")
    
    if st.button("✨ TẠO CÂU HỎI MỚI", type="primary", on_click=click_sinh_de):
        pass
    
    if st.session_state.de_bai:
        st.markdown('<div class="problem-box">', unsafe_allow_html=True)
        st.markdown("### ❓ Câu hỏi:")
        st.markdown(f"## {st.session_state.de_bai}")
        st.markdown('</div>', unsafe_allow_html=True)

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if st.button("🗣️ Dịch H'Mông"):
                bd = dich_sang_mong(st.session_state.de_bai)
                st.info(f"**H'Mông:** {bd}")

with col_phai:
    st.subheader("✍️ Làm bài")
    
    if st.session_state.de_bai:
        with st.form("form_lam_bai"):
            
            # Hiển thị input dựa trên loại câu hỏi (Trắc nghiệm vs Tự luận)
            user_ans = None
            if st.session_state.q_type == "mcq":
                st.markdown("**Chọn đáp án đúng:**")
                user_ans = st.radio("Đáp án:", st.session_state.options, label_visibility="collapsed")
            else:
                user_ans = st.number_input("Nhập đáp án số:", step=0.01, format="%.2f")

            btn_nop = st.form_submit_button("✅ Kiểm tra")
            
            if btn_nop:
                st.session_state.submitted = True
                is_correct = False
                
                # Kiểm tra đáp án
                if st.session_state.q_type == "mcq":
                    if user_ans == st.session_state.dap_an:
                        is_correct = True
                else:
                    # Số học
                    if abs(user_ans - float(st.session_state.dap_an)) <= 0.05:
                        is_correct = True

                if is_correct:
                    st.balloons()
                    st.success("CHÍNH XÁC! (Yog lawm) 👏")
                else:
                    st.error(f"Chưa đúng rồi! (Tsis yog lawm)")
                    if st.session_state.q_type == "mcq":
                        st.markdown(f"Đáp án đúng là: **${st.session_state.dap_an}$**")
                    else:
                        st.markdown(f"Đáp án đúng là: **{st.session_state.dap_an}**")
                    st.session_state.show_hint = True
        
        if st.session_state.show_hint:
            st.markdown("---")
            st.info(f"💡 **Gợi ý:** {st.session_state.goi_y_text}")
            if st.session_state.goi_y_latex:
                st.latex(st.session_state.goi_y_latex)

    else:
        st.info("👈 Chọn bài học và nhấn nút 'Tạo câu hỏi mới'.")

# Footer
st.markdown("---")
st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư - Bản Mường.")
