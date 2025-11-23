import streamlit as st
import random
import math
import time
from deep_translator import GoogleTranslator

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gia sư Toán AI - Bản Mường (Lớp 1-9)",
    page_icon="🏔️",
    layout="wide"
)

# --- GIẢ LẬP BỘ ĐẾM LƯỢT TRUY CẬP ---
if 'visit_count' not in st.session_state:
    # Khởi tạo một con số ngẫu nhiên để trông giống thật (ví dụ từ 5000 đến 8000)
    st.session_state.visit_count = random.randint(5000, 8000)

# --- DỮ LIỆU CHƯƠNG TRÌNH HỌC (CHUẨN KẾT NỐI TRI THỨC) ---
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
        "Chương 1: Đa thức": ["Nhân đơn thức với đa thức", "Nhân đa thức với đa thức", "Hằng đẳng thức (Bình phương)", "Hằng đẳng thức (Hiệu hai bình phương)"],
    },
    "Lớp 9": {
        "Chương 1: Phương trình và Hệ phương trình": ["Phương trình quy về bậc nhất", "Giải hệ phương trình bậc nhất hai ẩn"],
        "Chương 2: Phương trình bậc hai": ["Giải phương trình bậc hai (Công thức nghiệm)", "Hệ thức Vi-ét"],
        "Chương 3: Căn thức": ["Căn bậc hai", "Biến đổi đơn giản biểu thức chứa căn"]
    }
}

# --- CSS PHONG CÁCH THỔ CẨM H'MÔNG & HEADER ĐẸP ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    .stApp { background-color: #f0f4f8; background-image: radial-gradient(#dde1e7 1px, transparent 1px); background-size: 20px 20px; }
    
    /* HEADER ĐƯỢC THIẾT KẾ LẠI */
    .hmong-header-container {
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        overflow: hidden;
        margin-bottom: 30px;
        border: 2px solid #e0e0e0;
    }
    
    .hmong-top-bar {
        background: linear-gradient(90deg, #1a237e, #3949ab);
        color: white;
        padding: 10px 20px;
        text-align: center;
        font-size: 0.9rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .hmong-main-title {
        padding: 30px 20px;
        text-align: center;
        background: white;
    }
    
    .hmong-main-title h1 {
        color: #d32f2f; /* Màu đỏ đậm */
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 2px 2px 0px #ffcdd2;
    }
    
    .hmong-main-title h2 {
        color: #283593; /* Màu xanh chàm */
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 10px;
    }
    
    /* HỌA TIẾT THỔ CẨM */
    .hmong-pattern {
        height: 12px;
        background: repeating-linear-gradient(
            45deg,
            #d32f2f,
            #d32f2f 15px,
            #ffeb3b 15px,
            #ffeb3b 30px,
            #388e3c 30px,
            #388e3c 45px,
            #1976d2 45px,
            #1976d2 60px
        );
        width: 100%;
    }

    /* COUNTER BADGE */
    .visit-counter {
        background-color: #263238;
        color: #00e676; /* Màu xanh neon */
        padding: 5px 15px;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 0.9rem;
        display: inline-block;
        margin-top: 10px;
        border: 1px solid #00e676;
        box-shadow: 0 0 10px rgba(0, 230, 118, 0.3);
    }

    .problem-box {
        background-color: white; padding: 30px; border-radius: 20px;
        border: 2px solid #e0e0e0; border-top: 8px solid #1a237e;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(to right, #d32f2f, #b71c1c); 
        color: white;
        border: none; border-radius: 30px; font-weight: bold; font-size: 16px;
        padding: 0.6rem 2rem; transition: transform 0.2s; width: 100%;
        box-shadow: 0 4px 6px rgba(211, 47, 47, 0.3);
    }
    .stButton>button:hover { transform: scale(1.05); color: white; }
    .stRadio > div { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #eeeeee; }
    
    .hint-container {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 15px;
        border-radius: 5px;
        margin-top: 20px;
    }
    .hmong-hint {
        background-color: #fce4ec;
        border-left: 5px solid #e91e63;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC SINH ĐỀ (GIỮ NGUYÊN NHƯ BẠN YÊU CẦU) ---

def tao_de_toan(lop, bai_hoc):
    de_latex = ""
    question_type = "number" 
    dap_an = 0
    options = []
    goi_y_text = ""
    goi_y_latex = ""
    
    bai_lower = bai_hoc.lower()

    # === LỚP 8 ===
    if "Lớp 8" in lop:
        question_type = "mcq"
        if "Nhân đơn thức" in bai_hoc:
            a = random.choice([-3, -2, 2, 3, 4])
            b = random.choice([-3, -2, 2, 3, 4])
            c = random.choice([-5, -4, -3, 2, 3, 4, 5])
            de_latex = f"Thực hiện phép tính: ${a}x( {b}x {c:+d} )$"
            res_a, res_b = a * b, a * c
            ans_correct = f"${res_a}x^2 {res_b:+d}x$"
            options = [ans_correct, f"${res_a}x^2 {-res_b:+d}x$", f"${res_a}x {res_b:+d}$", f"${res_a+2}x^2 {res_b:+d}x$"]
            dap_an = ans_correct
            goi_y_text = "Nhân phân phối đơn thức vào đa thức: $A(B+C) = AB + AC$"
            goi_y_latex = f"{a}x \\cdot ({b}x {c:+d}) = {a}x \\cdot {b}x + {a}x \\cdot {c}"
        elif "Nhân đa thức" in bai_hoc:
            a, b = random.randint(1,5)*random.choice([-1,1]), random.randint(1,5)*random.choice([-1,1])
            de_latex = f"Thực hiện phép tính: $(x {a:+d})(x {b:+d})$"
            ans_correct = f"$x^2 {a+b:+d}x {a*b:+d}$"
            options = [ans_correct, f"$x^2 {a+b:+d}x {-a*b:+d}$", f"$x^2 {-a-b:+d}x {a*b:+d}$", f"$x^2 {a*b:+d}x {a+b:+d}$"]
            dap_an = ans_correct
            goi_y_text = "Nhân từng hạng tử của đa thức này với đa thức kia."
        elif "Hằng đẳng thức" in bai_hoc:
            a = random.randint(2, 5)
            de_latex = f"Khai triển: $(x - {a})^2$"
            ans_correct = f"$x^2 - {2*a}x + {a**2}$"
            options = [ans_correct, f"$x^2 + {2*a}x + {a**2}$", f"$x^2 - {a**2}$", f"$x^2 - {2*a}x - {a**2}$"]
            dap_an = ans_correct
            goi_y_text = "Sử dụng hằng đẳng thức $(A-B)^2 = A^2 - 2AB + B^2$"
        random.shuffle(options)

    # === LỚP 9 ===
    elif "Lớp 9" in lop:
        if "hệ phương trình" in bai_lower:
            x, y = random.randint(1, 5), random.randint(1, 5)
            a, b = x + y, x - y
            de_latex = f"Cho hệ: $\\begin{{cases}} x + y = {a} \\\\ x - y = {b} \\end{{cases}}$. Tìm $x$?"
            dap_an = x
            goi_y_text = "Cộng đại số hai phương trình để triệt tiêu y."
            goi_y_latex = f"(x+y) + (x-y) = {a} + {b} \\Rightarrow 2x = {a+b}"
        elif "phương trình bậc hai" in bai_lower or "vi-ét" in bai_lower:
            x1, x2 = random.randint(1, 5), random.randint(1, 5)
            de_latex = f"Tìm nghiệm lớn nhất của phương trình: $x^2 - {x1+x2}x + {x1*x2} = 0$"
            dap_an = max(x1, x2)
            goi_y_text = "Sử dụng công thức nghiệm hoặc nhẩm nghiệm Vi-ét."
        elif "căn" in bai_lower:
            dang_bai = random.randint(1, 4)
            if dang_bai == 1:
                a = random.randint(2, 5)
                de_latex = f"Rút gọn: $\\sqrt{{{a}^2 \\cdot 3}}$ (Nhập hệ số ngoài căn)"
                dap_an = a
                goi_y_text = "Đưa thừa số ra ngoài dấu căn: $\\sqrt{A^2B} = |A|\\sqrt{B}$"
            elif dang_bai == 2:
                res = random.randint(4, 15)
                de_latex = f"Tính: $\\sqrt{{{res**2}}} = ?$"
                dap_an = res
                goi_y_text = "Tìm số dương bình phương lên bằng số trong căn."
            elif dang_bai == 3:
                sq1, sq2 = random.choice([4, 9, 16]), random.choice([4, 9, 16])
                de_latex = f"Tính: $\\sqrt{{{sq1}}} + \\sqrt{{{sq2}}} = ?$"
                dap_an = math.sqrt(sq1) + math.sqrt(sq2)
            elif dang_bai == 4:
                res = random.randint(2, 10)
                de_latex = f"Tìm $x$ biết $\\sqrt{{x}} = {res}$"
                dap_an = res**2
                goi_y_text = "Bình phương hai vế: $x = a^2$"
        elif "phương trình" in bai_lower:
            a, b = random.randint(2, 5), random.randint(1, 10)
            de_latex = f"Giải phương trình: ${a}x - {b} = 0$ (Làm tròn 2 số thập phân)"
            dap_an = round(b/a, 2)
            goi_y_text = "Chuyển vế đổi dấu rồi chia cho hệ số."
            goi_y_latex = f"{a}x = {b} \\Rightarrow x = \\frac{{{b}}}{{{a}}}"

    # === LỚP 6 ===
    elif "Lớp 6" in lop:
        if "thứ tự" in bai_lower or "phép tính" in bai_lower:
            a, b, c = random.randint(2, 10), random.randint(2, 10), random.randint(2, 10)
            op1, op2 = random.choice(['+', '-']), '\\times'
            de_latex = f"Tính giá trị: ${a} {op1} {b} {op2} {c} = ?$"
            dap_an = a + b*c if op1 == '+' else a - b*c
            goi_y_text = "Nhân chia trước, cộng trừ sau."
            goi_y_latex = f"{a} {op1} ({b} \\times {c}) = {a} {op1} {b*c}"
        elif "lũy thừa" in bai_lower:
            base, exp = random.randint(2, 5), random.randint(2, 4)
            de_latex = f"Tính: ${base}^{exp} = ?$"
            dap_an = base ** exp
            goi_y_text = f"Nhân {base} với chính nó {exp} lần."
            goi_y_latex = f"{base}^{exp} = " + "\\times".join([str(base)]*exp)
        elif "số nguyên" in bai_lower:
            a, b = random.randint(-20, 20), random.randint(-20, 20)
            if "cộng" in bai_lower:
                de_latex = f"Tính: ${a} + ({b}) = ?$"
                dap_an = a + b
            elif "trừ" in bai_lower:
                de_latex = f"Tính: ${a} - ({b}) = ?$"
                dap_an = a - b
            elif "nhân" in bai_lower:
                de_latex = f"Tính: ${a} \\cdot ({b}) = ?$"
                dap_an = a * b
        elif "phân số" in bai_lower:
            tu1, mau, tu2 = random.randint(1, 5), random.randint(2, 6), random.randint(1, 5)
            if "cộng" in bai_lower:
                de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau}}} + \\frac{{{tu2}}}{{{mau}}} = ?$"
                question_type = "mcq"
                ans_correct = f"$\\frac{{{tu1+tu2}}}{{{mau}}}$"
                dap_an = ans_correct
                options = [ans_correct, f"$\\frac{{{abs(tu1-tu2)}}}{{{mau}}}$", f"$\\frac{{{tu1+tu2}}}{{{mau*2}}}$", f"$\\frac{{{tu1*tu2}}}{{{mau}}}$"]
                random.shuffle(options)
                goi_y_text = "Cộng tử, giữ nguyên mẫu."
            elif "nhân" in bai_lower:
                mau2 = random.randint(2, 6)
                de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau}}} \\cdot \\frac{{{tu2}}}{{{mau2}}} = ?$"
                question_type = "mcq"
                ans_correct = f"$\\frac{{{tu1*tu2}}}{{{mau*mau2}}}$"
                dap_an = ans_correct
                options = [ans_correct, f"$\\frac{{{tu1+tu2}}}{{{mau+mau2}}}$", f"$\\frac{{{tu1*mau2}}}{{{mau*tu2}}}$", f"$\\frac{{{tu1*tu2}}}{{{mau+mau2}}}$"]
                random.shuffle(options)
                goi_y_text = "Tử nhân tử, mẫu nhân mẫu."

    # === LỚP 7 ===
    elif "Lớp 7" in lop:
        if "làm tròn" in bai_lower:
            val, prec = random.uniform(10, 100), random.choice([1, 2])
            de_latex = f"Làm tròn số ${val:.4f}$ đến chữ số thập phân thứ {prec}."
            dap_an = round(val, prec)
            goi_y_text = f"Xét chữ số thứ {prec+1} sau dấu phẩy."
        elif "số hữu tỉ" in bai_lower:
            if "lũy thừa" in bai_lower:
                base, exp = random.randint(1, 3), 2
                de_latex = f"Tính: $\\left(\\frac{{{base}}}{{2}}\\right)^{{{exp}}} = ?$"
                question_type = "mcq"
                ans_correct = f"$\\frac{{{base**2}}}{{4}}$"
                dap_an = ans_correct
                options = [ans_correct, f"$\\frac{{{base*2}}}{{4}}$", f"$\\frac{{{base}}}{{4}}$", f"$\\frac{{{base**2}}}{{2}}$"]
                random.shuffle(options)
                goi_y_text = "Lũy thừa của tử và mẫu."
            else:
                a, b = round(random.uniform(-10, 10), 1), round(random.uniform(-10, 10), 1)
                de_latex = f"Tính: ${a} + ({b}) = ?$"
                dap_an = round(a + b, 1)
        elif "căn" in bai_lower:
            res = random.randint(2, 15)
            de_latex = f"Tính: $\\sqrt{{{res**2}}} = ?$"
            dap_an = res
            goi_y_text = "Tìm số dương bình phương lên bằng số trong căn."
        elif "tam giác" in bai_lower:
            g1, g2 = random.randint(30, 80), random.randint(30, 80)
            de_latex = f"$\\Delta ABC$ có $\\hat{{A}}={g1}^\\circ, \\hat{{B}}={g2}^\\circ$. Tính $\\hat{{C}}$?"
            dap_an = 180 - g1 - g2
            goi_y_text = "Tổng ba góc trong tam giác bằng $180^\\circ$."

    # === CẤP 1: LỚP 5 ===
    elif "Lớp 5" in lop:
        if "số thập phân" in bai_lower:
            a = round(random.uniform(1, 20), 1)
            b = round(random.uniform(1, 20), 1)
            if "cộng" in bai_lower:
                de_latex = f"Tính: ${a} + {b} = ?$"
                dap_an = round(a + b, 1)
                goi_y_text = "Cộng phần thập phân và phần nguyên tương ứng."
            elif "trừ" in bai_lower:
                lon, be = max(a, b), min(a, b)
                de_latex = f"Tính: ${lon} - {be} = ?$"
                dap_an = round(lon - be, 1)
                goi_y_text = "Trừ thẳng hàng dấu phẩy."
            elif "nhân" in bai_lower:
                a = round(random.uniform(1, 10), 1)
                b = random.randint(2, 9)
                de_latex = f"Tính: ${a} \\times {b} = ?$"
                dap_an = round(a * b, 1)
                goi_y_text = "Nhân như số tự nhiên, sau đó đặt dấu phẩy."

    # === CẤP 1: LỚP 4 ===
    elif "Lớp 4" in lop:
        if "làm tròn" in bai_lower:
            base = random.randint(10000, 99999)
            de_latex = f"Làm tròn số ${base}$ đến hàng nghìn."
            dap_an = round(base, -3)
            goi_y_text = "Xét chữ số hàng trăm. Nếu $\\ge 5$ thì cộng 1 vào hàng nghìn."
        elif "nhiều chữ số" in bai_lower or "số tự nhiên" in bai_lower: 
            a, b = random.randint(10000, 99999), random.randint(10000, 99999)
            op = random.choice(['+', '-'])
            if op == '-': a, b = max(a, b), min(a, b)
            de_latex = f"Tính: ${a} {op} {b} = ?$"
            dap_an = a + b if op == '+' else a - b
            goi_y_text = "Đặt tính rồi tính từ phải sang trái."
            goi_y_latex = f"\\begin{{array}}{{c}} \\phantom{{+}}{a} \\\\ \\underline{{ {op} {b} }} \\\\ \\dots \\end{{array}}"
        elif "phân số" in bai_lower:
            question_type = "mcq"
            mau = random.randint(3, 9)
            tu1, tu2 = random.randint(1, mau-1), random.randint(1, mau-1)
            if "cộng" in bai_lower:
                de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau}}} + \\frac{{{tu2}}}{{{mau}}} = ?$"
                ans_correct = f"$\\frac{{{tu1+tu2}}}{{{mau}}}$"
                dap_an = ans_correct
                options = [ans_correct, f"$\\frac{{{abs(tu1-tu2)}}}{{{mau}}}$", f"$\\frac{{{tu1+tu2}}}{{{mau+mau}}}$", f"$\\frac{{{tu1*tu2}}}{{{mau}}}$"]
                goi_y_text = "Cộng tử số, giữ nguyên mẫu số."
                goi_y_latex = f"\\frac{{{tu1}}}{{{mau}}} + \\frac{{{tu2}}}{{{mau}}} = \\frac{{{tu1}+{tu2}}}{{{mau}}}"
            elif "trừ" in bai_lower:
                if tu1 < tu2: tu1, tu2 = tu2, tu1
                de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau}}} - \\frac{{{tu2}}}{{{mau}}} = ?$"
                ans_correct = f"$\\frac{{{tu1-tu2}}}{{{mau}}}$"
                dap_an = ans_correct
                options = [ans_correct, f"$\\frac{{{tu1+tu2}}}{{{mau}}}$", f"$\\frac{{{tu1-tu2}}}{{{mau-mau}}}$", f"$\\frac{{{tu1}}}{{{mau}}}$"]
                goi_y_text = "Trừ tử số, giữ nguyên mẫu số."
            elif "nhân" in bai_lower:
                mau2 = random.randint(2, 9)
                de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau}}} \\times \\frac{{{tu2}}}{{{mau2}}} = ?$"
                ans_correct = f"$\\frac{{{tu1*tu2}}}{{{mau*mau2}}}$"
                dap_an = ans_correct
                options = [ans_correct, f"$\\frac{{{tu1+tu2}}}{{{mau+mau2}}}$", f"$\\frac{{{tu1*mau2}}}{{{mau*tu2}}}$", f"$\\frac{{{tu1}}}{{{mau}}}$"]
                goi_y_text = "Tử nhân tử, mẫu nhân mẫu."
                goi_y_latex = f"\\frac{{{tu1}}}{{{mau}}} \\times \\frac{{{tu2}}}{{{mau2}}} = \\frac{{{tu1} \\times {tu2}}}{{{mau} \\times {mau2}}}"
            random.shuffle(options)

    # === CẤP 1: LỚP 3 ===
    elif "Lớp 3" in lop:
        if "nhân" in bai_lower:
            a, b = random.randint(10, 50), random.randint(2, 9)
            de_latex = f"Tính: ${a} \\times {b} = ?$"
            dap_an = a * b
            goi_y_text = "Nhân lần lượt từ hàng đơn vị sang hàng chục."
            goi_y_latex = f"{a} \\times {b} = {a*b}"
        elif "chia" in bai_lower:
            b, kq = random.randint(2, 9), random.randint(10, 50)
            a = b * kq
            de_latex = f"Tính: ${a} : {b} = ?$"
            dap_an = kq
            goi_y_text = "Chia lần lượt từ hàng chục sang hàng đơn vị."
        elif "diện tích" in bai_lower:
            if "vuông" in bai_lower:
                a = random.randint(3, 9)
                de_latex = f"Tính diện tích hình vuông cạnh ${a}cm$."
                dap_an = a * a
                goi_y_text = "Diện tích hình vuông bằng cạnh nhân cạnh."
                goi_y_latex = f"S = a \\times a = {a} \\times {a}"
            else:
                a = random.randint(5, 10)
                b = random.randint(2, a-1)
                de_latex = f"Tính diện tích HCN dài ${a}cm$, rộng ${b}cm$."
                dap_an = a * b
                goi_y_text = "Diện tích hình chữ nhật bằng dài nhân rộng."
                goi_y_latex = f"S = a \\times b = {a} \\times {b}"

    # === CẤP 1: LỚP 1, 2 ===
    elif "Lớp 1" in lop or "Lớp 2" in lop:
        a, b = random.randint(1, 10), random.randint(1, 10)
        if "Lớp 1" in lop: a, b = random.randint(1, 5), random.randint(0, 5)
        elif "Lớp 2" in lop: a, b = random.randint(10, 50), random.randint(2, 9)

        if "cộng" in bai_lower:
            de_latex = f"Tính: ${a} + {b} = ?$"
            dap_an = a + b
            goi_y_text = "Thực hiện phép cộng."
            goi_y_latex = f"{a} + {b} = {a+b}"
        elif "trừ" in bai_lower:
            lon, be = max(a, b), min(a, b)
            de_latex = f"Tính: ${lon} - {be} = ?$"
            dap_an = lon - be
            goi_y_text = "Thực hiện phép trừ."
            goi_y_latex = f"{lon} - {be} = {lon-be}"
        elif "nhân" in bai_lower:
            a, b = random.randint(2, 5), random.randint(1, 10)
            de_latex = f"Tính: ${a} \\times {b} = ?$"
            dap_an = a * b
            goi_y_text = "Sử dụng bảng cửu chương."
        elif "chia" in bai_lower:
            b = random.choice([2, 5])
            ans = random.randint(1, 10)
            a = b * ans
            de_latex = f"Tính: ${a} : {b} = ?$"
            dap_an = ans
            goi_y_text = "Sử dụng bảng chia."
        elif "so sánh" in bai_lower:
            question_type = "mcq"
            de_latex = f"So sánh: ${a} \\dots {b}$"
            if a > b: ans_correct = "$>$"
            elif a < b: ans_correct = "$<$"
            else: ans_correct = "$=$"
            dap_an = ans_correct
            options = ["$>$", "$<$", "$=$"]
            goi_y_text = "So sánh giá trị hai số."
        elif "số" in bai_lower: 
             de_latex = f"Số liền sau của ${a}$ là?"
             dap_an = a + 1
             goi_y_text = "Đếm thêm 1 đơn vị."

    else:
        # Fallback
        a, b = random.randint(1, 10), random.randint(1, 10)
        de_latex = f"Tính: ${a} + {b} = ?$"
        dap_an = a + b
             
    return de_latex, question_type, dap_an, options, goi_y_text, goi_y_latex

# Hàm dịch thuật
def dich_sang_mong(text):
    try:
        return GoogleTranslator(source='vi', target='hmn').translate(text)
    except:
        return "..."

# --- GIAO DIỆN CHÍNH ---

# Header mới với bộ đếm
st.markdown(f"""
<div class="hmong-header-container">
    <div class="hmong-top-bar">SỞ GIÁO DỤC VÀ ĐÀO TẠO TỈNH ĐIỆN BIÊN</div>
    <div class="hmong-main-title">
        <h1>🏫 TRƯỜNG PTDTBT TH&THCS NA Ư</h1>
        <h2>🚀 GIA SƯ TOÁN AI - BẢN MƯỜNG</h2>
        <div class="visit-counter">Lượt truy cập: {st.session_state.visit_count}</div>
    </div>
    <div class="hmong-pattern"></div>
</div>
""", unsafe_allow_html=True)

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
            
            if st.session_state.q_type == "mcq":
                st.markdown("**Chọn đáp án đúng:**")
                user_ans = st.radio("Đáp án:", st.session_state.options, label_visibility="collapsed")
            else:
                is_integer_answer = False
                if isinstance(st.session_state.dap_an, int) or (isinstance(st.session_state.dap_an, float) and st.session_state.dap_an.is_integer()):
                    is_integer_answer = True
                
                if is_integer_answer:
                    user_ans = st.number_input("Nhập đáp án (Số nguyên):", step=1, format="%d")
                else:
                    user_ans = st.number_input("Nhập đáp án:", step=0.01, format="%.2f")

            btn_nop = st.form_submit_button("✅ Kiểm tra")
            
            if btn_nop:
                st.session_state.submitted = True
                is_correct = False
                
                if st.session_state.q_type == "mcq":
                    if user_ans == st.session_state.dap_an:
                        is_correct = True
                else:
                    if abs(user_ans - float(st.session_state.dap_an)) <= 0.05:
                        is_correct = True

                if is_correct:
                    st.balloons()
                    st.success("CHÍNH XÁC! (Yog lawm) 👏")
                else:
                    st.error(f"Chưa đúng rồi! (Tsis yog lawm)")
                    if st.session_state.q_type == "mcq":
                        st.markdown(f"Đáp án đúng là: {st.session_state.dap_an}")
                    else:
                        ans_display = int(st.session_state.dap_an) if float(st.session_state.dap_an).is_integer() else st.session_state.dap_an
                        st.markdown(f"Đáp án đúng là: **{ans_display}**")
                    st.session_state.show_hint = True
        
        if st.session_state.show_hint:
            st.markdown("---")
            st.markdown('<div class="hint-container">', unsafe_allow_html=True)
            st.markdown(f"**💡 Gợi ý:** {st.session_state.goi_y_text}")
            
            if st.session_state.goi_y_latex:
                st.latex(st.session_state.goi_y_latex)
            st.markdown('</div>', unsafe_allow_html=True)
                
            translation = dich_sang_mong(st.session_state.goi_y_text)
            st.markdown('<div class="hmong-hint">', unsafe_allow_html=True)
            st.markdown(f"**🗣️ H'Mông:** {translation}")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("👈 Chọn bài học và nhấn nút 'Tạo câu hỏi mới'.")

# Footer
st.markdown("---")
st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư - Bản Mường.")
