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
    
    /* Style cho phần gợi ý */
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

# --- LOGIC SINH ĐỀ ---

def tao_de_toan(lop, bai_hoc):
    de_latex = ""
    question_type = "number" 
    dap_an = 0
    options = []
    goi_y_text = ""
    goi_y_latex = ""
    
    bai_lower = bai_hoc.lower()

    # === LỚP 3: CẬP NHẬT CÔNG THỨC & LOGIC ===
    if "Lớp 3" in lop:
        if "nhân" in bai_lower:
            # Nhân số có 2 chữ số với số có 1 chữ số
            a = random.randint(10, 50)
            b = random.randint(2, 9)
            de_latex = f"Tính: ${a} \\times {b} = ?$"
            dap_an = a * b
            goi_y_text = "Đặt tính rồi tính: Nhân lần lượt từ hàng đơn vị đến hàng chục."
            goi_y_latex = f"{a} \\times {b} = {a*b}"
        elif "chia" in bai_lower:
            # Chia hết: b * kq = a
            b = random.randint(2, 9)
            kq = random.randint(10, 50)
            a = b * kq
            de_latex = f"Tính: ${a} : {b} = ?$"
            dap_an = kq
            goi_y_text = "Đặt tính rồi tính: Chia lần lượt từ hàng chục đến hàng đơn vị."
            goi_y_latex = f"{a} : {b} = {kq}"
        elif "diện tích" in bai_lower:
            if "vuông" in bai_lower:
                a = random.randint(3, 9)
                de_latex = f"Tính diện tích hình vuông có cạnh ${a}cm$."
                dap_an = a * a
                goi_y_text = "Diện tích hình vuông bằng cạnh nhân cạnh."
                goi_y_latex = f"S = {a} \\times {a} = {a*a} (cm^2)"
            else: # Chữ nhật
                a = random.randint(5, 10)
                b = random.randint(2, a-1)
                de_latex = f"Tính diện tích hình chữ nhật có chiều dài ${a}cm$, chiều rộng ${b}cm$."
                dap_an = a * b
                goi_y_text = "Diện tích hình chữ nhật bằng chiều dài nhân chiều rộng."
                goi_y_latex = f"S = {a} \\times {b} = {a*b} (cm^2)"

    # === LỚP 4: CẬP NHẬT CÔNG THỨC & LOGIC ===
    elif "Lớp 4" in lop:
        if "làm tròn" in bai_lower:
            # Làm tròn đến hàng nghìn, chục nghìn
            base = random.randint(10000, 99999)
            de_latex = f"Làm tròn số ${base}$ đến hàng nghìn."
            dap_an = round(base, -3)
            goi_y_text = "Quan sát chữ số hàng trăm. Nếu >= 5 thì cộng 1 vào hàng nghìn, ngược lại giữ nguyên."
        elif "phân số" in bai_lower:
            # Dùng MCQ cho phân số đẹp như Lớp 6
            question_type = "mcq"
            mau = random.randint(3, 9)
            tu1 = random.randint(1, mau-1)
            tu2 = random.randint(1, mau-1)
            
            if "cộng" in bai_lower:
                de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau}}} + \\frac{{{tu2}}}{{{mau}}} = ?$"
                correct_tu = tu1 + tu2
                ans_correct = f"$\\frac{{{correct_tu}}}{{{mau}}}$"
                dap_an = ans_correct
                options = [
                    ans_correct,
                    f"$\\frac{{{abs(tu1-tu2)}}}{{{mau}}}$",
                    f"$\\frac{{{correct_tu}}}{{{mau+mau}}}$", # Sai lầm cộng mẫu
                    f"$\\frac{{{tu1*tu2}}}{{{mau}}}$"
                ]
                goi_y_text = "Cộng tử số, giữ nguyên mẫu số."
                goi_y_latex = f"\\frac{{{tu1}}}{{{mau}}} + \\frac{{{tu2}}}{{{mau}}} = \\frac{{{tu1}+{tu2}}}{{{mau}}}"
            elif "trừ" in bai_lower:
                if tu1 < tu2: tu1, tu2 = tu2, tu1 # Đảm bảo dương
                de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau}}} - \\frac{{{tu2}}}{{{mau}}} = ?$"
                correct_tu = tu1 - tu2
                ans_correct = f"$\\frac{{{correct_tu}}}{{{mau}}}$"
                dap_an = ans_correct
                options = [
                    ans_correct,
                    f"$\\frac{{{tu1+tu2}}}{{{mau}}}$",
                    f"$\\frac{{{correct_tu}}}{{{mau-mau}}}$", 
                    f"$\\frac{{{tu1}}}{{{mau}}}$"
                ]
                goi_y_text = "Trừ tử số, giữ nguyên mẫu số."
                goi_y_latex = f"\\frac{{{tu1}}}{{{mau}}} - \\frac{{{tu2}}}{{{mau}}} = \\frac{{{tu1}-{tu2}}}{{{mau}}}"
            elif "nhân" in bai_lower:
                mau2 = random.randint(2, 9)
                de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau}}} \\times \\frac{{{tu2}}}{{{mau2}}} = ?$"
                ans_correct = f"$\\frac{{{tu1*tu2}}}{{{mau*mau2}}}$"
                dap_an = ans_correct
                options = [
                    ans_correct,
                    f"$\\frac{{{tu1+tu2}}}{{{mau+mau2}}}$",
                    f"$\\frac{{{tu1*mau2}}}{{{mau*tu2}}}$",
                    f"$\\frac{{{tu1}}}{{{mau}}}$"
                ]
                goi_y_text = "Lấy tử nhân tử, mẫu nhân mẫu."
                goi_y_latex = f"\\frac{{{tu1}}}{{{mau}}} \\times \\frac{{{tu2}}}{{{mau2}}} = \\frac{{{tu1} \\times {tu2}}}{{{mau} \\times {mau2}}}"
            
            random.shuffle(options)

    # === LỚP 5: CẬP NHẬT CÔNG THỨC & LOGIC ===
    elif "Lớp 5" in lop:
        if "số thập phân" in bai_lower:
            a = round(random.uniform(1, 20), 1)
            b = round(random.uniform(1, 20), 1)
            if "cộng" in bai_lower:
                de_latex = f"Tính: ${a} + {b} = ?$"
                dap_an = round(a + b, 1)
                goi_y_text = "Đặt tính thẳng hàng dấu phẩy rồi cộng như số tự nhiên."
            elif "trừ" in bai_lower:
                lon, be = max(a, b), min(a, b)
                de_latex = f"Tính: ${lon} - {be} = ?$"
                dap_an = round(lon - be, 1)
                goi_y_text = "Đặt tính thẳng hàng dấu phẩy rồi trừ như số tự nhiên."
            elif "nhân" in bai_lower:
                # Nhân số thập phân đơn giản (1 chữ số thập phân)
                a = round(random.uniform(1, 10), 1)
                b = random.randint(2, 9) # Nhân với số tự nhiên cho dễ hoặc số thập phân nhỏ
                de_latex = f"Tính: ${a} \\times {b} = ?$"
                dap_an = round(a * b, 1)
                goi_y_text = "Nhân như số tự nhiên, sau đó đếm phần thập phân để đặt dấu phẩy."

    # === LỚP 8: SỬ DỤNG LATEX CHO ĐÁP ÁN TRẮC NGHIỆM ===
    elif "Lớp 8" in lop:
        question_type = "mcq"
        if "Nhân đơn thức" in bai_hoc:
            a = random.choice([-3, -2, 2, 3, 4])
            b = random.choice([-3, -2, 2, 3, 4])
            c = random.choice([-5, -4, -3, 2, 3, 4, 5])
            de_latex = f"Thực hiện phép tính: ${a}x( {b}x {c:+d} )$"
            res_a, res_b = a * b, a * c
            ans_correct = f"${res_a}x^2 {res_b:+d}x$"
            options = [
                ans_correct, 
                f"${res_a}x^2 {-res_b:+d}x$", 
                f"${res_a}x {res_b:+d}$", 
                f"${res_a+2}x^2 {res_b:+d}x$"
            ]
            dap_an = ans_correct
            goi_y_text = "Nhân phân phối đơn thức vào đa thức: $A(B+C) = AB + AC$"
            goi_y_latex = f"{a}x \\cdot ({b}x {c:+d}) = {a}x \\cdot {b}x + {a}x \\cdot {c}"
            
        elif "Nhân đa thức" in bai_hoc:
            a, b = random.randint(1,5)*random.choice([-1,1]), random.randint(1,5)*random.choice([-1,1])
            de_latex = f"Thực hiện phép tính: $(x {a:+d})(x {b:+d})$"
            term_x = a + b
            term_free = a * b
            ans_correct = f"$x^2 {term_x:+d}x {term_free:+d}$"
            options = [
                ans_correct, 
                f"$x^2 {term_x:+d}x {-term_free:+d}$", 
                f"$x^2 {-term_x:+d}x {term_free:+d}$", 
                f"$x^2 {term_free:+d}x {term_x:+d}$"
            ]
            dap_an = ans_correct
            goi_y_text = "Nhân từng hạng tử của đa thức này với đa thức kia."
            
        elif "Hằng đẳng thức" in bai_hoc:
            a = random.randint(2, 5)
            de_latex = f"Khai triển: $(x - {a})^2$"
            ans_correct = f"$x^2 - {2*a}x + {a**2}$"
            options = [
                ans_correct, 
                f"$x^2 + {2*a}x + {a**2}$", 
                f"$x^2 - {a**2}$", 
                f"$x^2 - {2*a}x - {a**2}$"
            ]
            dap_an = ans_correct
            goi_y_text = "Sử dụng hằng đẳng thức $(A-B)^2 = A^2 - 2AB + B^2$"
        
        random.shuffle(options)

    # === LỚP 6: CẬP NHẬT CÔNG THỨC TOÁN CHO TRẮC NGHIỆM ===
    elif "Lớp 6" in lop:
        if "thứ tự" in bai_lower or "phép tính" in bai_lower:
            a, b, c = random.randint(2, 10), random.randint(2, 10), random.randint(2, 10)
            op1, op2 = random.choice(['+', '-']), '\\times'
            de_latex = f"Tính giá trị biểu thức: ${a} {op1} {b} {op2} {c} = ?$"
            if op1 == '+': dap_an = a + b * c
            else: dap_an = a - b * c
            goi_y_text = "Thực hiện phép nhân chia trước, cộng trừ sau."
            goi_y_latex = f"{a} {op1} ({b} \\times {c}) = {a} {op1} {b*c}"

        elif "lũy thừa" in bai_lower:
            base = random.randint(2, 5)
            exp = random.randint(2, 4)
            de_latex = f"Tính giá trị: ${base}^{exp} = ?$"
            dap_an = base ** exp
            goi_y_text = f"Nhân {base} với chính nó {exp} lần: $a^n = a \\times a \\dots$"
            goi_y_latex = f"{base}^{exp} = " + "\\times".join([str(base)]*exp)
            
        elif "số nguyên" in bai_lower:
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
                
        elif "phân số" in bai_lower:
            tu1, mau = random.randint(1, 5), random.randint(2, 6)
            tu2 = random.randint(1, 5)
            if "cộng" in bai_lower:
                de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau}}} + \\frac{{{tu2}}}{{{mau}}} = ?$"
                question_type = "mcq"
                correct_tu = tu1 + tu2
                # CẬP NHẬT: Dùng \frac cho đáp án
                ans_correct = f"$\\frac{{{correct_tu}}}{{{mau}}}$"
                dap_an = ans_correct
                options = [
                    ans_correct, 
                    f"$\\frac{{{abs(tu1-tu2)}}}{{{mau}}}$", 
                    f"$\\frac{{{correct_tu}}}{{{mau*2}}}$", 
                    f"$\\frac{{{tu1*tu2}}}{{{mau}}}$"
                ]
                random.shuffle(options)
                goi_y_text = "Cộng tử số và giữ nguyên mẫu số: $\\frac{a}{m} + \\frac{b}{m} = \\frac{a+b}{m}$"
            elif "nhân" in bai_lower:
                mau2 = random.randint(2, 6)
                de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau}}} \\cdot \\frac{{{tu2}}}{{{mau2}}} = ?$"
                question_type = "mcq"
                ans_correct = f"$\\frac{{{tu1*tu2}}}{{{mau*mau2}}}$"
                dap_an = ans_correct
                options = [
                    ans_correct, 
                    f"$\\frac{{{tu1+tu2}}}{{{mau+mau2}}}$", 
                    f"$\\frac{{{tu1*mau2}}}{{{mau*tu2}}}$", 
                    f"$\\frac{{{tu1*tu2}}}{{{mau+mau2}}}$"
                ]
                random.shuffle(options)
                goi_y_text = "Tử nhân tử, mẫu nhân mẫu: $\\frac{a}{b} \\cdot \\frac{c}{d} = \\frac{a \\cdot c}{b \\cdot d}$"

    # === LỚP 7: CẬP NHẬT CÔNG THỨC TOÁN CHO TRẮC NGHIỆM ===
    elif "Lớp 7" in lop:
        if "làm tròn" in bai_lower:
            val = random.uniform(10, 100)
            precision = random.choice([1, 2])
            de_latex = f"Làm tròn số ${val:.4f}$ đến chữ số thập phân thứ {precision}."
            dap_an = round(val, precision)
            goi_y_text = f"Nếu chữ số thứ {precision+1} sau dấu phẩy >= 5 thì cộng 1 vào chữ số trước nó."
            
        elif "số hữu tỉ" in bai_lower:
            if "lũy thừa" in bai_lower:
                base = random.randint(1, 3)
                exp = 2
                # CẬP NHẬT: Dùng \left( \right) và \frac cho đề bài
                de_latex = f"Tính: $\\left(\\frac{{{base}}}{{2}}\\right)^{{{exp}}} = ?$"
                question_type = "mcq"
                numerator = base**2
                denominator = 4
                # CẬP NHẬT: Dùng \frac cho đáp án
                ans_correct = f"$\\frac{{{numerator}}}{{{denominator}}}$"
                dap_an = ans_correct
                options = [
                    ans_correct, 
                    f"$\\frac{{{base*2}}}{{{denominator}}}$", 
                    f"$\\frac{{{base}}}{{{denominator}}}$", 
                    f"$\\frac{{{numerator}}}{{2}}$"
                ]
                random.shuffle(options)
                goi_y_text = "Lũy thừa của một thương bằng thương các lũy thừa: $(\\frac{x}{y})^n = \\frac{x^n}{y^n}$"
            else:
                a = round(random.uniform(-10, 10), 1)
                b = round(random.uniform(-10, 10), 1)
                de_latex = f"Tính: ${a} + ({b}) = ?$"
                dap_an = round(a + b, 1)
                goi_y_text = "Cộng trừ số thập phân hữu tỉ."
                
        elif "căn" in bai_lower:
            res = random.randint(2, 15)
            n = res**2
            de_latex = f"Tính căn bậc hai số học: $\\sqrt{{{n}}} = ?$"
            dap_an = res
            goi_y_text = f"Số dương nào bình phương lên bằng {n}?"
            
        elif "tam giác" in bai_lower:
            g1 = random.randint(30, 80)
            g2 = random.randint(30, 80)
            de_latex = f"Cho $\\Delta ABC$ có $\\hat{{A}}={g1}^\\circ, \\hat{{B}}={g2}^\\circ$. Tính $\\hat{{C}}$?"
            dap_an = 180 - g1 - g2
            goi_y_text = "Tổng ba góc trong một tam giác bằng $180^\\circ$."

    # === LỚP 9 (ĐÃ CẬP NHẬT ĐA DẠNG DẠNG CÂU HỎI) ===
    elif "Lớp 9" in lop:
        if "hệ phương trình" in bai_lower:
            x = random.randint(1, 5)
            y = random.randint(1, 5)
            a = x + y
            b = x - y
            de_latex = f"Cho hệ phương trình: $\\begin{{cases}} x + y = {a} \\\\ x - y = {b} \\end{{cases}}$. Tìm giá trị của $x$?"
            dap_an = x
            goi_y_text = "Cộng đại số hai phương trình để triệt tiêu y."
            goi_y_latex = f"(x+y) + (x-y) = {a} + {b} \\Rightarrow 2x = {a+b}"
        
        elif "phương trình bậc hai" in bai_lower or "vi-ét" in bai_lower:
            x1 = random.randint(1, 5)
            x2 = random.randint(1, 5)
            S = x1 + x2
            P = x1 * x2
            de_latex = f"Tìm nghiệm lớn nhất của phương trình: $x^2 - {S}x + {P} = 0$"
            dap_an = max(x1, x2)
            goi_y_text = "Sử dụng công thức nghiệm hoặc nhẩm nghiệm theo Vi-ét."
            
        elif "căn" in bai_lower:
            dang_bai = random.randint(1, 4)
            if dang_bai == 1:
                a = random.randint(2, 5)
                de_latex = f"Rút gọn biểu thức: $\\sqrt{{{a}^2 \\cdot 3}}$ (Nhập hệ số đứng trước căn 3)"
                dap_an = a
                goi_y_text = "Đưa thừa số ra ngoài dấu căn: $\\sqrt{A^2B} = |A|\\sqrt{B}$"
            elif dang_bai == 2:
                res = random.randint(4, 15)
                de_latex = f"Tính: $\\sqrt{{{res**2}}} = ?$"
                dap_an = res
                goi_y_text = "Tìm số dương mà bình phương lên bằng số trong căn."
            elif dang_bai == 3:
                sq1, sq2 = random.choice([4, 9, 16, 25]), random.choice([4, 9, 16, 25])
                de_latex = f"Tính: $\\sqrt{{{sq1}}} + \\sqrt{{{sq2}}} = ?$"
                dap_an = math.sqrt(sq1) + math.sqrt(sq2)
                goi_y_text = "Khai phương từng số hạng rồi cộng lại."
            elif dang_bai == 4:
                res = random.randint(2, 10)
                de_latex = f"Tìm $x$ biết $\\sqrt{{x}} = {res}$"
                dap_an = res**2
                goi_y_text = "Bình phương hai vế lên: $x = a^2$"

        elif "phương trình" in bai_lower:
            a = random.randint(2, 5)
            b = random.randint(1, 10)
            de_latex = f"Giải phương trình: ${a}x - {b} = 0$. (Kết quả làm tròn 2 chữ số thập phân)"
            dap_an = round(b/a, 2)
            goi_y_text = "Chuyển vế đổi dấu rồi chia cho hệ số."
            goi_y_latex = f"{a}x = {b} \\Rightarrow x = \\frac{{{b}}}{{{a}}}"

    # === CẤP 1 (LỚP 1, 2, CÁC TRƯỜNG HỢP MẶC ĐỊNH) ===
    else: 
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        
        if "Lớp 1" in lop: a, b = random.randint(1, 5), random.randint(0, 5)
        elif "Lớp 2" in lop: a, b = random.randint(10, 50), random.randint(1, 9)

        if "cộng" in bai_lower:
            de_latex = f"Tính: ${a} + {b} = ?$"
            dap_an = a + b
        elif "trừ" in bai_lower:
            lon, be = max(a, b), min(a, b)
            de_latex = f"Tính: ${lon} - {be} = ?$"
            dap_an = lon - be
        elif "nhân" in bai_lower:
             a, b = random.randint(2, 9), random.randint(2, 9)
             de_latex = f"Tính: ${a} \\times {b} = ?$"
             dap_an = a * b
        elif "chia" in bai_lower:
             b = random.randint(2, 9)
             ans = random.randint(2, 9)
             a = b * ans
             de_latex = f"Tính: ${a} : {b} = ?$"
             dap_an = ans
        else:
             de_latex = f"Tính: ${a} + {b} = ?$"
             dap_an = a + b
             
    return de_latex, question_type, dap_an, options, goi_y_text, goi_y_latex

# Hàm dịch thuật (ĐÃ SỬA ĐỂ GIỮ LẠI CÔNG THỨC TOÁN)
def dich_sang_mong(text):
    try:
        # Không xóa các ký tự đặc biệt của LaTeX ($, \, {, }) để Google Translate giữ nguyên hoặc xử lý tốt hơn
        return GoogleTranslator(source='vi', target='hmn').translate(text)
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
            
            # --- XỬ LÝ GIAO DIỆN NHẬP LIỆU ---
            if st.session_state.q_type == "mcq":
                st.markdown("**Chọn đáp án đúng:**")
                # Đáp án trắc nghiệm bây giờ đã là công thức LaTeX ($...$) nên sẽ hiển thị đẹp
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
                        # Hiển thị đáp án đúng dạng LaTeX
                        st.markdown(f"Đáp án đúng là: {st.session_state.dap_an}")
                    else:
                        ans_display = int(st.session_state.dap_an) if float(st.session_state.dap_an).is_integer() else st.session_state.dap_an
                        st.markdown(f"Đáp án đúng là: **{ans_display}**")
                    st.session_state.show_hint = True
        
        # --- HIỂN THỊ GỢI Ý VÀ DỊCH H'MÔNG ---
        if st.session_state.show_hint:
            st.markdown("---")
            st.markdown('<div class="hint-container">', unsafe_allow_html=True)
            st.markdown(f"**💡 Gợi ý:** {st.session_state.goi_y_text}")
            
            if st.session_state.goi_y_latex:
                st.latex(st.session_state.goi_y_latex)
            st.markdown('</div>', unsafe_allow_html=True)
                
            # THÊM PHẦN DỊCH GỢI Ý TIẾNG MÔNG
            translation = dich_sang_mong(st.session_state.goi_y_text)
            st.markdown('<div class="hmong-hint">', unsafe_allow_html=True)
            st.markdown(f"**🗣️ H'Mông:** {translation}")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("👈 Chọn bài học và nhấn nút 'Tạo câu hỏi mới'.")

# Footer
st.markdown("---")
st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư - Bản Mường.")
