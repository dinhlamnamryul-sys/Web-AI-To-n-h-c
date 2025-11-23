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

# --- DỮ LIỆU CHƯƠNG TRÌNH HỌC (CHUẨN KẾT NỐI TRI THỨC) ---
# Đã cập nhật lại nội dung Lớp 6, 7, 9 theo mục lục SGK mới
CHUONG_TRINH_HOC = {
    "Lớp 1": {
        "Chương 1: Các số từ 0 đến 10": ["Các số 0-10", "Tách - Gộp số", "So sánh số"],
        "Chương 2: Phép cộng, trừ trong phạm vi 10": ["Phép cộng trong phạm vi 10", "Phép trừ trong phạm vi 10"]
    },
    "Lớp 2": {
        "Chương 1: Phép cộng, trừ (có nhớ)": ["Phép cộng qua 10", "Phép trừ qua 10"],
        "Chương 2: Phép nhân, Phép chia": ["Bảng nhân 2, 5", "Bảng chia 2, 5"]
    },
    "Lớp 3": {
        "Chương 1: Phép nhân, chia phạm vi 1000": ["Nhân số có 2 chữ số với số có 1 chữ số", "Chia số có 2 chữ số cho số có 1 chữ số"],
        "Chương 2: Diện tích": ["Diện tích hình chữ nhật", "Diện tích hình vuông"]
    },
    "Lớp 4": {
        "Chương 1: Số tự nhiên": ["Các số có nhiều chữ số", "Làm tròn số"],
        "Chương 2: Phân số": ["Cộng phân số (cùng mẫu)", "Trừ phân số (cùng mẫu)", "Nhân phân số"]
    },
    "Lớp 5": {
        "Chương 1: Số thập phân": ["Cộng số thập phân", "Trừ số thập phân", "Nhân số thập phân"]
    },
    "Lớp 6": {
        "Chương 1: Tập hợp các số tự nhiên": ["Thứ tự thực hiện phép tính", "Lũy thừa với số mũ tự nhiên"],
        "Chương 2: Số nguyên": ["Phép cộng số nguyên", "Phép trừ số nguyên", "Phép nhân số nguyên"],
        "Chương 3: Phân số": ["Phép cộng phân số", "Phép nhân phân số"]
    },
    "Lớp 7": {
        "Chương 1: Số hữu tỉ": ["Cộng, trừ, nhân, chia số hữu tỉ", "Lũy thừa của số hữu tỉ"],
        "Chương 2: Số thực": ["Căn bậc hai số học", "Làm tròn số"],
        "Chương 3: Góc và đường thẳng song song": ["Tổng ba góc trong một tam giác"]
    },
    "Lớp 8": {
        # Giữ nguyên logic lớp 8 như bạn yêu cầu
        "Chương 1: Đa thức": ["Nhân đơn thức với đa thức", "Nhân đa thức với đa thức", "Hằng đẳng thức (Bình phương)", "Hằng đẳng thức (Hiệu hai bình phương)"],
    },
    "Lớp 9": {
        "Chương 1: Phương trình và Hệ phương trình": ["Phương trình quy về bậc nhất", "Giải hệ phương trình bậc nhất hai ẩn"],
        "Chương 2: Phương trình bậc hai": ["Giải phương trình bậc hai (Công thức nghiệm)", "Hệ thức Vi-ét"],
        "Chương 3: Căn thức": ["Căn bậc hai", "Biến đổi đơn giản biểu thức chứa căn"]
    }
}

# --- CSS PHONG CÁCH THỔ CẨM H'MÔNG ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    .stApp { background-color: #f3f6fb; background-image: radial-gradient(#dbeafe 1px, transparent 1px); background-size: 20px 20px; }
    
    .hmong-header {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        color: white; padding: 25px; border-radius: 15px; text-align: center;
        border-bottom: 5px solid #d32f2f; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    .hmong-pattern {
        height: 10px;
        background: repeating-linear-gradient(45deg, #d32f2f, #d32f2f 10px, #ffeb3b 10px, #ffeb3b 20px, #388e3c 20px, #388e3c 30px);
        margin-top: 10px; border-radius: 5px;
    }
    .problem-box {
        background-color: white; padding: 30px; border-radius: 20px;
        border: 2px solid #e0e0e0; border-top: 8px solid #1a237e;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(to right, #d32f2f, #c62828); color: white;
        border: none; border-radius: 30px; font-weight: bold; font-size: 16px;
        padding: 0.6rem 2rem; transition: transform 0.2s; width: 100%;
    }
    .stButton>button:hover { transform: scale(1.05); color: white; }
    .stRadio > div { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #eeeeee; }
</style>
""", unsafe_allow_html=True)

# --- LOGIC SINH ĐỀ (CẬP NHẬT MỚI) ---

def tao_de_toan(lop, bai_hoc):
    de_latex = ""
    question_type = "number" 
    dap_an = 0
    options = []
    goi_y_text = ""
    goi_y_latex = ""
    
    bai_lower = bai_hoc.lower()

    # === LỚP 8 (GIỮ NGUYÊN CODE CŨ) ===
    if "Lớp 8" in lop:
        question_type = "mcq"
        if "Nhân đơn thức" in bai_hoc:
            a = random.choice([-3, -2, 2, 3, 4])
            b = random.choice([-3, -2, 2, 3, 4])
            c = random.choice([-5, -4, -3, 2, 3, 4, 5])
            de_latex = f"Thực hiện phép tính: ${a}x( {b}x {c:+d} )$"
            res_a, res_b = a * b, a * c
            ans_correct = f"{res_a}x^2 {res_b:+d}x"
            options = [ans_correct, f"{res_a}x^2 {-res_b:+d}x", f"{res_a}x {res_b:+d}", f"{res_a+2}x^2 {res_b:+d}x"]
            dap_an = ans_correct
            goi_y_text = "Nhân phân phối đơn thức vào đa thức."
            goi_y_latex = f"{a}x \\cdot ({b}x {c:+d}) = {a}x \\cdot {b}x + {a}x \\cdot {c}"
        elif "Nhân đa thức" in bai_hoc:
            a, b = random.randint(1,5)*random.choice([-1,1]), random.randint(1,5)*random.choice([-1,1])
            de_latex = f"Thực hiện phép tính: $(x {a:+d})(x {b:+d})$"
            ans_correct = f"x^2 {a+b:+d}x {a*b:+d}"
            options = [ans_correct, f"x^2 {a+b:+d}x {-a*b:+d}", f"x^2 {-(a+b):+d}x {a*b:+d}", f"x^2 {a*b:+d}x {a+b:+d}"]
            dap_an = ans_correct
            goi_y_text = "Nhân từng hạng tử của đa thức này với đa thức kia."
        elif "Hằng đẳng thức" in bai_hoc:
            a = random.randint(2, 5)
            de_latex = f"Khai triển: $(x - {a})^2$"
            ans_correct = f"x^2 - {2*a}x + {a**2}"
            options = [ans_correct, f"x^2 + {2*a}x + {a**2}", f"x^2 - {a**2}", f"x^2 - {2*a}x - {a**2}"]
            dap_an = ans_correct
            goi_y_text = "Sử dụng hằng đẳng thức $(A-B)^2 = A^2 - 2AB + B^2$"
        
        random.shuffle(options)
        return de_latex, question_type, dap_an, options, goi_y_text, goi_y_latex

    # === LỚP 6 (CẬP NHẬT) ===
    elif "Lớp 6" in lop:
        if "Lũy thừa" in bai_hoc:
            base = random.randint(2, 5)
            exp = random.randint(2, 4)
            de_latex = f"Tính giá trị: ${base}^{exp} = ?$"
            dap_an = base ** exp
            goi_y_text = f"Nhân {base} với chính nó {exp} lần."
            goi_y_latex = f"{base}^{exp} = " + "\\times".join([str(base)]*exp)
        elif "Số nguyên" in bai_hoc:
            a = random.randint(-20, 20)
            b = random.randint(-20, 20)
            if "cộng" in bai_lower:
                de_latex = f"Tính: ${a} + ({b}) = ?$"
                dap_an = a + b
                goi_y_text = "Cộng hai số nguyên."
            elif "trừ" in bai_lower:
                de_latex = f"Tính: ${a} - ({b}) = ?$"
                dap_an = a - b
                goi_y_text = "Muốn trừ số nguyên a cho b, ta cộng a với số đối của b."
            elif "nhân" in bai_lower:
                de_latex = f"Tính: ${a} \\cdot ({b}) = ?$"
                dap_an = a * b
                goi_y_text = "Nhân hai số nguyên: cùng dấu là dương, trái dấu là âm."
        elif "Phân số" in bai_hoc:
            tu1, mau = random.randint(1, 5), random.randint(2, 6)
            tu2 = random.randint(1, 5)
            if "cộng" in bai_lower:
                de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau}}} + \\frac{{{tu2}}}{{{mau}}} = ?$"
                # Để đơn giản cho nhập liệu, ta yêu cầu nhập kết quả dạng thập phân hoặc chọn bài trắc nghiệm
                # Ở đây ta đổi sang trắc nghiệm cho phân số lớp 6 để dễ kiểm tra
                question_type = "mcq"
                correct_tu = tu1 + tu2
                ans_correct = f"{correct_tu}/{mau}"
                dap_an = ans_correct
                options = [ans_correct, f"{abs(tu1-tu2)}/{mau}", f"{correct_tu}/{mau*2}", f"{tu1*tu2}/{mau}"]
                random.shuffle(options)
                goi_y_text = "Cộng tử giữ nguyên mẫu."

    # === LỚP 7 (CẬP NHẬT) ===
    elif "Lớp 7" in lop:
        if "Số hữu tỉ" in bai_lower:
            # Cộng trừ số hữu tỉ đơn giản (dạng thập phân)
            a = round(random.uniform(-10, 10), 1)
            b = round(random.uniform(-10, 10), 1)
            de_latex = f"Tính: ${a} + ({b}) = ?$"
            dap_an = round(a + b, 1)
            goi_y_text = "Cộng trừ số thập phân hữu tỉ."
        elif "Căn bậc hai" in bai_hoc:
            res = random.randint(2, 15)
            n = res**2
            de_latex = f"Tính căn bậc hai số học: $\\sqrt{{{n}}} = ?$"
            dap_an = res
            goi_y_text = f"Số dương nào bình phương lên bằng {n}?"
        elif "Tam giác" in bai_hoc:
            g1 = random.randint(30, 80)
            g2 = random.randint(30, 80)
            de_latex = f"Cho $\\Delta ABC$ có $\\hat{{A}}={g1}^\\circ, \\hat{{B}}={g2}^\\circ$. Tính $\\hat{{C}}$?"
            dap_an = 180 - g1 - g2
            goi_y_text = "Tổng ba góc trong một tam giác bằng $180^\\circ$."

    # === LỚP 9 (CẬP NHẬT) ===
    elif "Lớp 9" in lop:
        if "Hệ phương trình" in bai_hoc:
            # Giải hệ cơ bản tìm x
            x = random.randint(1, 5)
            y = random.randint(1, 5)
            # x + y = a, x - y = b
            a = x + y
            b = x - y
            de_latex = f"Cho hệ phương trình: $\\begin{{cases}} x + y = {a} \\\\ x - y = {b} \\end{{cases}}$. Tìm giá trị của $x$?"
            dap_an = x
            goi_y_text = "Cộng đại số hai phương trình để triệt tiêu y."
            goi_y_latex = f"(x+y) + (x-y) = {a} + {b} \\Rightarrow 2x = {a+b}"
        elif "Phương trình bậc hai" in bai_hoc:
            # Tìm nghiệm dương của x^2 - Sx + P = 0
            x1 = random.randint(1, 5)
            x2 = random.randint(1, 5)
            S = x1 + x2
            P = x1 * x2
            de_latex = f"Tìm nghiệm lớn nhất của phương trình: $x^2 - {S}x + {P} = 0$"
            dap_an = max(x1, x2)
            goi_y_text = "Sử dụng công thức nghiệm hoặc nhẩm nghiệm theo Vi-ét."
        elif "Căn thức" in bai_hoc:
            # Tính sqrt(a^2 * b)
            a = random.randint(2, 5)
            de_latex = f"Rút gọn biểu thức: $\\sqrt{{{a}^2 \\cdot 3}}$ (Nhập hệ số đứng trước căn 3)"
            dap_an = a
            goi_y_text = "Đưa thừa số ra ngoài dấu căn: $\\sqrt{A^2B} = |A|\\sqrt{B}$"

    # === CẤP 1 (LỚP 1-5): ƯU TIÊN SỐ NGUYÊN ===
    else: 
        # Logic mặc định cho Cấp 1
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        
        # Điều chỉnh độ khó theo lớp
        if "Lớp 1" in lop:
            a, b = random.randint(1, 5), random.randint(0, 5)
        elif "Lớp 2" in lop or "Lớp 3" in lop:
            a, b = random.randint(10, 50), random.randint(1, 9)
        elif "Lớp 4" in lop or "Lớp 5" in lop:
            a, b = random.randint(100, 900), random.randint(10, 99)

        if "cộng" in bai_lower:
            de_latex = f"Tính: ${a} + {b} = ?$"
            dap_an = a + b
        elif "trừ" in bai_lower:
            # Đảm bảo trừ ra số dương cho cấp 1
            lon, be = max(a, b), min(a, b)
            de_latex = f"Tính: ${lon} - {be} = ?$"
            dap_an = lon - be
        elif "nhân" in bai_lower:
             # Lớp 2, 3 bảng cửu chương
             a, b = random.randint(2, 9), random.randint(2, 9)
             de_latex = f"Tính: ${a} \\times {b} = ?$"
             dap_an = a * b
        elif "chia" in bai_lower:
             b = random.randint(2, 9)
             ans = random.randint(2, 9)
             a = b * ans
             de_latex = f"Tính: ${a} : {b} = ?$"
             dap_an = ans
        else: # Fallback cộng
             de_latex = f"Tính: ${a} + {b} = ?$"
             dap_an = a + b
             
    return de_latex, question_type, dap_an, options, goi_y_text, goi_y_latex

# Hàm dịch thuật
def dich_sang_mong(text):
    try:
        clean_text = text.replace("$", "").replace("\\", "").replace("{", "").replace("}", "")
        return GoogleTranslator(source='vi', target='hmn').translate(clean_text)
    except:
        return "..."

# --- GIAO DIỆN CHÍNH ---

st.markdown('<div class="hmong-header">', unsafe_allow_html=True)
st.markdown('<h3>SỞ GIÁO DỤC VÀ ĐÀO TẠO TỈNH ĐIỆN BIÊN</h3>', unsafe_allow_html=True)
st.markdown('<h1>🏫 TRƯỜNG PTDTBT TH&THCS NA Ư</h1>', unsafe_allow_html=True)
st.markdown('<h2>🚀 GIA SƯ TOÁN AI - BẢN MƯỜNG</h2>', unsafe_allow_html=True)
st.markdown('<div class="hmong-pattern"></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
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

col_trai, col_phai = st.columns([1.6, 1])

if 'de_bai' not in st.session_state:
    st.session_state.de_bai = ""
    st.session_state.q_type = "number"
    st.session_state.dap_an = 0
    st.session_state.options = []
    st.session_state.goi_y_text = ""
    st.session_state.goi_y_latex = ""
    st.session_state.show_hint = False

def click_sinh_de():
    db, qt, da, ops, gyt, gyl = tao_de_toan(lop_chon, bai_chon)
    st.session_state.de_bai = db
    st.session_state.q_type = qt
    st.session_state.dap_an = da
    st.session_state.options = ops
    st.session_state.goi_y_text = gyt
    st.session_state.goi_y_latex = gyl
    st.session_state.show_hint = False
    st.session_state.submitted = False

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
            user_ans = None
            
            # --- XỬ LÝ GIAO DIỆN NHẬP LIỆU THÔNG MINH ---
            if st.session_state.q_type == "mcq":
                st.markdown("**Chọn đáp án đúng:**")
                user_ans = st.radio("Đáp án:", st.session_state.options, label_visibility="collapsed")
            else:
                # KIỂM TRA: Nếu đáp án là số nguyên -> Hiển thị input số nguyên (không có .00)
                # Đây là phần sửa lỗi "7.00" cho Cấp 1
                is_integer_answer = False
                if isinstance(st.session_state.dap_an, int) or (isinstance(st.session_state.dap_an, float) and st.session_state.dap_an.is_integer()):
                    is_integer_answer = True
                
                if is_integer_answer:
                    # step=1 và format="%d" để chỉ hiện số nguyên
                    user_ans = st.number_input("Nhập đáp án (Số nguyên):", step=1, format="%d")
                else:
                    # Nếu là số thập phân thì giữ nguyên như cũ
                    user_ans = st.number_input("Nhập đáp án:", step=0.01, format="%.2f")

            btn_nop = st.form_submit_button("✅ Kiểm tra")
            
            if btn_nop:
                st.session_state.submitted = True
                is_correct = False
                
                if st.session_state.q_type == "mcq":
                    if user_ans == st.session_state.dap_an:
                        is_correct = True
                else:
                    # So sánh số học
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
                        # Hiển thị đáp án đúng cũng theo định dạng số nguyên nếu cần
                        ans_display = int(st.session_state.dap_an) if float(st.session_state.dap_an).is_integer() else st.session_state.dap_an
                        st.markdown(f"Đáp án đúng là: **{ans_display}**")
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

