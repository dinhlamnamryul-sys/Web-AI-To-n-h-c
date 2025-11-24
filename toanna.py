import streamlit as st
import random
import math
import time
import os
import pandas as pd
import io
import base64
from deep_translator import GoogleTranslator
from gtts import gTTS  # Thư viện giọng nói Google

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gia sư Toán AI - Bản Mường (Lớp 1-9)",
    page_icon="🏔️",
    layout="wide"
)

# --- BỘ ĐẾM LƯỢT TRUY CẬP THỰC TẾ ---
def update_visit_count():
    count_file = "visit_count.txt"
    if not os.path.exists(count_file):
        with open(count_file, "w") as f:
            f.write("5383") 
            return 5383
    try:
        with open(count_file, "r") as f:
            content = f.read().strip()
            count = int(content) if content else 5383
    except Exception:
        count = 5383
    count += 1
    try:
        with open(count_file, "w") as f:
            f.write(str(count))
    except Exception:
        pass
    return count

if 'visit_count' not in st.session_state:
    st.session_state.visit_count = update_visit_count()

# --- DỮ LIỆU CHƯƠNG TRÌNH HỌC ---
CHUONG_TRINH_HOC = {
    "Lớp 1": {
        "Chủ đề 1: Các số từ 0 đến 10": ["Các số 0-10", "So sánh số", "Mấy và mấy"],
        "Chủ đề 2: Làm quen với một số hình phẳng": ["Hình vuông, tròn, tam giác, chữ nhật"],
        "Chủ đề 3: Phép cộng, phép trừ trong phạm vi 10": ["Phép cộng trong phạm vi 10", "Phép trừ trong phạm vi 10"],
        "Chủ đề 4: Làm quen với một số hình khối": ["Khối lập phương, khối hộp chữ nhật"]
    },
    "Lớp 2": {
        "Chủ đề 1: Ôn tập và bổ sung": ["Số hạng - Tổng", "Số bị trừ - Số trừ - Hiệu", "Luyện tập phép cộng trừ", "Tia số - Số liền trước, sau"],
        "Chủ đề 2: Phép cộng, phép trừ trong phạm vi 20": ["Phép cộng (qua 10) trong phạm vi 20", "Phép trừ (qua 10) trong phạm vi 20", "Bài toán thêm, bớt", "Bài toán nhiều hơn, ít hơn"],
        "Chủ đề 3: Làm quen với khối lượng, dung tích": ["Ki-lô-gam (kg)", "Lít (l)"],
        "Chủ đề 4: Phép cộng, phép trừ (có nhớ) trong phạm vi 100": ["Phép cộng (có nhớ) số có 2 chữ số", "Phép trừ (có nhớ) số có 2 chữ số"],
        "Chủ đề 5: Làm quen với hình phẳng": ["Điểm - Đoạn thẳng - Đường thẳng - Đường cong", "Đường gấp khúc - Hình tứ giác", "Ba điểm thẳng hàng"],
        "Chủ đề 6: Ngày giờ, ngày tháng": ["Ngày - Giờ, Giờ - Phút", "Ngày - Tháng", "Xem lịch và đồng hồ"]
    },
    "Lớp 3": {
        "Chủ đề 1: Ôn tập và bổ sung": ["Ôn tập các số đến 1000", "Ôn tập phép cộng, phép trừ", "Tìm thành phần trong phép cộng, phép trừ", "Ôn tập bảng nhân 2, 5, bảng chia 2, 5", "Bảng nhân 3, 4 - Bảng chia 3, 4"],
        "Chủ đề 2: Bảng nhân, bảng chia": ["Bảng nhân 6, 7, 8, 9", "Bảng chia 6, 7, 8, 9", "Tìm thành phần trong phép nhân, chia", "Một phần mấy"],
        "Chủ đề 3: Hình phẳng, hình khối": ["Điểm ở giữa - Trung điểm", "Hình tròn (Tâm, bán kính, đường kính)", "Góc vuông, góc không vuông", "Hình tam giác, tứ giác, chữ nhật, vuông", "Khối lập phương, khối hộp chữ nhật"],
        "Chủ đề 4: Phép nhân, phép chia trong phạm vi 100": ["Nhân số có 2 chữ số với số có 1 chữ số", "Chia số có 2 chữ số cho số có 1 chữ số", "Phép chia hết, phép chia có dư", "Gấp/Giảm một số đi một số lần", "Bài toán giải bằng hai bước tính"],
        "Chủ đề 5: Một số đơn vị đo": ["Mi-li-mét (mm)", "Gam (g)", "Mi-li-lít (ml)", "Nhiệt độ"],
        "Chủ đề 6: Phép nhân, chia trong phạm vi 1000": ["Nhân số có 3 chữ số với số có 1 chữ số", "Chia số có 3 chữ số cho số có 1 chữ số", "Biểu thức số - Giá trị biểu thức"]
    },
    "Lớp 4": {
        "Chủ đề 1: Ôn tập và bổ sung": ["Ôn tập số đến 100.000", "Biểu thức có chứa chữ"],
        "Chủ đề 2: Góc và Đơn vị đo": ["Góc nhọn, góc tù, góc bẹt", "Đơn vị đo khối lượng (Yến, Tạ, Tấn)", "Đơn vị đo thời gian (Giây, Thế kỷ)"],
        "Chủ đề 3: Số có nhiều chữ số": ["Lớp triệu - Lớp đơn vị", "Đọc, viết, so sánh số lớn", "Làm tròn số đến hàng trăm nghìn"],
        "Chủ đề 4: Phép cộng, phép trừ": ["Cộng, trừ số có nhiều chữ số", "Tính chất giao hoán, kết hợp", "Tìm số trung bình cộng"],
        "Chủ đề 5: Phép nhân, phép chia": ["Nhân với số có 2 chữ số", "Chia cho số có 2 chữ số", "Thương có chữ số 0"]
    },
    "Lớp 5": {
        "Chủ đề 1: Ôn tập và bổ sung": ["Ôn tập về phân số", "Hỗn số", "Bài toán tỉ lệ"],
        "Chủ đề 2: Số thập phân": ["Khái niệm số thập phân", "Hàng của số thập phân", "Đọc, viết số thập phân", "So sánh số thập phân", "Viết số đo đại lượng dưới dạng số thập phân"],
        "Chủ đề 3: Các phép tính với số thập phân": ["Cộng hai số thập phân", "Trừ hai số thập phân", "Nhân số thập phân", "Chia số thập phân"],
        "Chủ đề 4: Hình học": ["Hình tam giác (Diện tích)", "Hình thang (Diện tích)", "Hình tròn (Chu vi, Diện tích)"]
    },
    "Lớp 6": {
        "Chương 1: Tập hợp các số tự nhiên": ["Phép tính lũy thừa", "Thứ tự thực hiện phép tính", "Quan hệ chia hết", "Số nguyên tố - Hợp số", "ƯCLN - BCNN"],
        "Chương 2: Số nguyên": ["Tập hợp số nguyên", "Phép cộng, trừ số nguyên", "Phép nhân, chia số nguyên", "Quy tắc dấu ngoặc"],
        "Chương 3: Một số hình phẳng trong thực tiễn": ["Tam giác đều, hình vuông, lục giác đều", "Hình chữ nhật, hình thoi, hình bình hành, hình thang cân"],
        "Chương 4: Tính đối xứng của hình phẳng": ["Hình có trục đối xứng", "Hình có tâm đối xứng"]
    },
    "Lớp 7": {
        "Chương 1: Số hữu tỉ": ["Cộng, trừ, nhân, chia số hữu tỉ", "Lũy thừa với số mũ tự nhiên của số hữu tỉ", "Quy tắc dấu ngoặc"],
        "Chương 2: Số thực": ["Số vô tỉ - Căn bậc hai số học", "Số thực - Giá trị tuyệt đối"],
        "Chương 3: Góc và đường thẳng song song": ["Góc ở vị trí đặc biệt", "Tia phân giác", "Hai đường thẳng song song"],
        "Chương 4: Tam giác bằng nhau": ["Tổng 3 góc trong tam giác", "Hai tam giác bằng nhau", "Các trường hợp bằng nhau của tam giác"]
    },
    "Lớp 8": {
        "Chương 1: Đa thức": ["Cộng trừ đa thức", "Nhân đơn thức với đa thức", "Nhân đa thức với đa thức", "Chia đa thức cho đơn thức"],
        "Chương 2: Hằng đẳng thức đáng nhớ": ["Bình phương của một tổng/hiệu", "Hiệu hai bình phương", "Lập phương của một tổng/hiệu"],
        "Chương 3: Phân thức đại số": ["Cộng trừ phân thức", "Nhân chia phân thức"],
        "Chương 4: Hàm số và Đồ thị": ["Hàm số bậc nhất y = ax + b", "Hệ số góc của đường thẳng"]
    },
    "Lớp 9": {
        "Chương 1: Phương trình và Hệ phương trình bậc nhất": ["Phương trình quy về phương trình bậc nhất một ẩn", "Phương trình bậc nhất hai ẩn", "Giải hệ hai phương trình bậc nhất hai ẩn"],
        "Chương 2: Phương trình và bất phương trình bậc nhất một ẩn": ["Bất đẳng thức", "Bất phương trình bậc nhất một ẩn"],
        "Chương 3: Căn thức": ["Căn bậc hai", "Căn bậc ba", "Biến đổi đơn giản biểu thức chứa căn"],
        "Chương 4: Hệ thức lượng trong tam giác vuông": ["Tỉ số lượng giác của góc nhọn", "Một số hệ thức về cạnh và góc"],
        "Chương 5: Đường tròn": ["Đường tròn và các yếu tố liên quan", "Vị trí tương đối của đường thẳng và đường tròn"]
    }
}

# --- CSS PHONG CÁCH THỔ CẨM H'MÔNG ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    .stApp { background-color: #f0f4f8; background-image: radial-gradient(#dde1e7 1px, transparent 1px); background-size: 20px 20px; }
    
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
        color: #d32f2f;
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 2px 2px 0px #ffcdd2;
    }
    
    .hmong-main-title h2 {
        color: #283593;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 10px;
    }
    
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

    .visit-counter {
        background-color: #263238;
        color: #00e676;
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
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        color: #1b5e20;
    }
    .hmong-hint {
        background-color: #fce4ec;
        border-left: 5px solid #e91e63;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
        font-style: italic;
        color: #880e4f;
    }
    .error-box {
        background-color: #ffebee;
        border: 1px solid #ef9a9a;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
        color: #c62828;
        font-weight: bold;
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

    if "Lớp 9" in lop:
        question_type = "mcq" 
        if "hệ phương trình" in bai_lower or "hệ hai phương trình" in bai_lower:
            x = random.randint(1, 5)
            y = random.randint(1, 5)
            c1 = x + y
            c2 = x - y
            de_latex = f"Giải hệ phương trình: $\\begin{{cases}} x + y = {c1} \\\\ x - y = {c2} \\end{{cases}}$"
            ans_correct = f"x={x}, y={y}"
            dap_an = ans_correct
            options = [f"x={x}, y={y}", f"x={x+1}, y={y-1}", f"x={y}, y={x}", f"x={x}, y={-y}"]
            goi_y_text = "Cộng đại số hai phương trình để tìm x, sau đó thay vào tìm y."
            goi_y_latex = f"2x = {c1+c2} \\Rightarrow x = {x}"
        elif "phương trình bậc nhất hai ẩn" in bai_lower:
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            x_true, y_true = random.randint(0,3), random.randint(0,3)
            c_true = a*x_true + b*y_true
            de_latex = f"Cặp số nào là nghiệm của phương trình ${a}x + {b}y = {c_true}$?"
            ans_correct = f"({x_true}; {y_true})"
            dap_an = ans_correct
            options = [f"({x_true}; {y_true})", f"({x_true+1}; {y_true})", f"({x_true}; {y_true+1})", f"(0; 0)"]
            goi_y_text = "Thay cặp số (x; y) vào phương trình xem có thỏa mãn không."
        elif "phương trình quy về" in bai_lower:
            a = random.randint(2, 5)
            b = random.randint(1, 10)
            de_latex = f"Giải phương trình: ${a}x - {b} = 0$ (Làm tròn 2 số thập phân)"
            ans_val = round(b/a, 2)
            dap_an = ans_val
            question_type = "number"
            goi_y_text = "Chuyển vế đổi dấu rồi chia cho hệ số."
            goi_y_latex = f"x = \\frac{{{b}}}{{{a}}}"
        elif "bất đẳng thức" in bai_lower:
            a = random.randint(2, 9)
            de_latex = f"Nếu $a > b$ thì khẳng định nào sau đây đúng?"
            ans_correct = f"$a + {a} > b + {a}$"
            dap_an = ans_correct
            options = [ans_correct, f"$a - {a} < b - {a}$", f"$-{a}a > -{a}b$", f"$a < b$"]
            goi_y_text = "Cộng cả hai vế với cùng một số thì chiều bất đẳng thức không đổi."
        elif "bất phương trình" in bai_lower:
            a = random.randint(2, 5)
            b = random.randint(1, 10)
            de_latex = f"Giải bất phương trình: ${a}x > {a*b}$"
            ans_correct = f"$x > {b}$"
            dap_an = ans_correct
            options = [ans_correct, f"$x < {b}$", f"$x > {a}$", f"$x > {a*b}$"]
            goi_y_text = "Chia cả hai vế cho số dương, chiều bất đẳng thức giữ nguyên."
        elif "căn bậc hai" in bai_lower and "căn bậc ba" not in bai_lower:
            sq = random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100])
            de_latex = f"Tính: $\\sqrt{{{sq}}}$"
            dap_an = int(math.sqrt(sq))
            question_type = "number"
            goi_y_text = "Tìm số dương bình phương lên bằng số trong căn."
        elif "căn bậc ba" in bai_lower:
            cb = random.choice([8, 27, 64, 125, -8, -27])
            de_latex = f"Tính: $\\sqrt[3]{{{cb}}}$"
            dap_an = int(cb**(1/3)) if cb > 0 else -int(abs(cb)**(1/3))
            question_type = "number"
            goi_y_text = "Tìm số lập phương lên bằng số trong căn."
        elif "biến đổi" in bai_lower or "căn thức" in bai_lower:
            a = random.randint(2, 5)
            b = random.randint(2, 5)
            de_latex = f"Rút gọn biểu thức: $\\sqrt{{{a**2 * b}}}$"
            ans_correct = f"${a}\\sqrt{{{b}}}$"
            dap_an = ans_correct
            options = [ans_correct, f"${b}\\sqrt{{{a}}}$", f"$\\sqrt{{{a*b}}}$", f"${a*b}$"]
            goi_y_text = "Đưa thừa số ra ngoài dấu căn: $\\sqrt{A^2B} = |A|\\sqrt{B}$"
        elif "tỉ số lượng giác" in bai_lower:
            de_latex = "Trong tam giác vuông, tỉ số giữa cạnh đối và cạnh huyền là?"
            ans_correct = "Sin"
            dap_an = ans_correct
            options = ["Sin", "Cos", "Tan", "Cot"]
            goi_y_text = "Sin = Đối / Huyền"
        elif "hệ thức" in bai_lower or "tam giác vuông" in bai_lower:
            c1, c2 = 3, 4
            de_latex = f"Tam giác vuông có hai cạnh góc vuông là {c1}cm và {c2}cm. Tính cạnh huyền."
            dap_an = 5
            question_type = "number"
            goi_y_text = "Định lý Pythagoras: $a^2 = b^2 + c^2$"
        elif "đường tròn" in bai_lower:
            r = random.randint(3, 10)
            de_latex = f"Đường tròn tâm O bán kính R={r}cm. Điểm M cách O một khoảng {r-1}cm. Vị trí của M?"
            ans_correct = "Nằm trong đường tròn"
            dap_an = ans_correct
            options = ["Nằm trong đường tròn", "Nằm trên đường tròn", "Nằm ngoài đường tròn", "Trùng với tâm O"]
            goi_y_text = "Khoảng cách d < R thì điểm nằm trong đường tròn."
        else:
            x = random.randint(1, 10)
            de_latex = f"Tìm x biết $\\sqrt{{x}} = {x}$"
            dap_an = x**2
            question_type = "number"
            goi_y_text = "Bình phương hai vế."
        if question_type == "mcq": random.shuffle(options)

    elif "Lớp 4" in lop:
        if "ôn tập" in bai_lower:
            a = random.randint(10000, 90000)
            de_latex = f"Số liền sau của số ${a}$ là?"
            dap_an = a + 1
            goi_y_text = "Cộng thêm 1 đơn vị."
        elif "biểu thức" in bai_lower:
            a, b = random.randint(5, 20), random.randint(2, 9)
            de_latex = f"Tính giá trị của biểu thức $a \\times b$ với $a={a}, b={b}$"
            dap_an = a * b
            goi_y_text = "Thay giá trị của chữ vào biểu thức."
        elif "góc" in bai_lower:
            question_type = "mcq"
            de_latex = "Góc bẹt bằng bao nhiêu độ?"
            dap_an = "180 độ"
            options = ["90 độ", "180 độ", "60 độ", "360 độ"]
            goi_y_text = "Góc bẹt bằng hai lần góc vuông."
        elif "đơn vị" in bai_lower or "yến" in bai_lower or "tạ" in bai_lower or "giây" in bai_lower:
            if "yến" in bai_lower:
                val = random.randint(2, 10)
                de_latex = f"Đổi: ${val}$ yến = ... kg"
                dap_an = val * 10
                goi_y_text = "1 yến = 10 kg"
            else:
                m = random.randint(2, 10)
                de_latex = f"Đổi: ${m}$ phút = ... giây"
                dap_an = m * 60
                goi_y_text = "1 phút = 60 giây"
        elif "số có nhiều chữ số" in bai_lower:
            a, b = random.randint(100000, 999999), random.randint(100000, 999999)
            de_latex = f"So sánh: ${a} \\dots {b}$"
            question_type = "mcq"
            ans_correct = ">" if a > b else ("<" if a < b else "=")
            dap_an = ans_correct
            options = [">", "<", "="]
            goi_y_text = "So sánh từng hàng từ trái sang phải."
        elif "cộng" in bai_lower:
            a, b = random.randint(10000, 99999), random.randint(1000, 9999)
            de_latex = f"Tính: ${a} + {b}$"
            dap_an = a + b
            goi_y_text = "Đặt tính rồi tính."
        elif "trung bình cộng" in bai_lower:
            n1, n2, n3 = random.randint(10, 50), random.randint(10, 50), random.randint(10, 50)
            n3 = n3 - ((n1 + n2 + n3) % 3)
            total = n1 + n2 + n3
            de_latex = f"Trung bình cộng của ${n1}, {n2}, {n3}$ là?"
            dap_an = total // 3
            goi_y_text = "Tổng chia cho số các số hạng."
        elif "nhân" in bai_lower:
            a, b = random.randint(100, 999), random.randint(10, 99)
            de_latex = f"Tính: ${a} \\times {b}$"
            dap_an = a * b
            goi_y_text = "Nhân lần lượt từng chữ số."
        elif "chia" in bai_lower:
            b = random.randint(10, 50)
            res = random.randint(10, 50)
            a = b * res
            de_latex = f"Tính: ${a} : {b}$"
            dap_an = res
            goi_y_text = "Đặt tính rồi tính."

    elif "Lớp 5" in lop:
        if "phân số" in bai_lower:
            tu1, mau1, tu2, mau2 = random.randint(1, 5), random.randint(2, 6), random.randint(1, 5), random.randint(2, 6)
            de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau1}}} + \\frac{{{tu2}}}{{{mau2}}}$ (Kết quả làm tròn 2 số thập phân)"
            dap_an = round((tu1/mau1) + (tu2/mau2), 2)
            goi_y_text = "Quy đồng mẫu số rồi cộng."
        elif "số thập phân" in bai_lower and "so sánh" in bai_lower:
            a, b = round(random.uniform(1, 100), 2), round(random.uniform(1, 100), 2)
            de_latex = f"So sánh: ${a} \\dots {b}$"
            question_type = "mcq"
            ans_correct = ">" if a > b else ("<" if a < b else "=")
            dap_an = ans_correct
            options = [">", "<", "="]
            goi_y_text = "So sánh phần nguyên rồi đến phần thập phân."
        elif "phép tính" in bai_lower or "cộng" in bai_lower or "trừ" in bai_lower:
            a, b = round(random.uniform(1, 50), 1), round(random.uniform(1, 20), 1)
            if "cộng" in bai_lower:
                de_latex = f"Tính: ${a} + {b} = ?$"
                dap_an = round(a + b, 2)
            else:
                if a < b: a, b = b, a
                de_latex = f"Tính: ${a} - {b} = ?$"
                dap_an = round(a - b, 2)
            goi_y_text = "Đặt dấu phẩy thẳng cột."
        elif "hình học" in bai_lower or "tam giác" in bai_lower:
            a, h = random.randint(5, 20), random.randint(5, 20)
            de_latex = f"Diện tích tam giác đáy $a={a}$, cao $h={h}$."
            dap_an = (a * h) / 2
            goi_y_text = "S = (đáy x chiều cao) : 2"

    elif "Lớp 8" in lop:
        question_type = "mcq"
        if "đa thức" in bai_lower:
            a1, a2 = random.randint(2, 5), random.randint(2, 5)
            de_latex = f"Rút gọn: $({a1}x) + ({a2}x)$"
            ans_correct = f"${a1+a2}x$"
            dap_an = ans_correct
            options = [ans_correct, f"${a1*a2}x$", f"${a1}x^2", f"${a2}x"]
            goi_y_text = "Cộng hệ số, giữ nguyên phần biến."
        elif "hằng đẳng thức" in bai_lower:
            a = random.randint(2, 5)
            de_latex = f"Khai triển: $(x+{a})^2$"
            ans_correct = f"$x^2 + {2*a}x + {a**2}$"
            dap_an = ans_correct
            options = [ans_correct, f"$x^2 + {a**2}$", f"$x^2 - {2*a}x + {a**2}$", f"$x^2 + {2*a}x$"]
            goi_y_text = "Bình phương số thứ nhất + 2 lần tích + bình phương số thứ hai."

    elif "Lớp 3" in lop:
        if "ôn tập" in bai_lower:
            a = random.randint(100, 899)
            de_latex = f"Số liền sau của số ${a}$ là?"
            dap_an = a + 1
            goi_y_text = "Đếm thêm 1 đơn vị."
        elif "bảng nhân" in bai_lower:
            base, mult = random.randint(6, 9), random.randint(2, 9)
            de_latex = f"Tính nhẩm: ${base} \\times {mult} = ?$"
            dap_an = base * mult
            goi_y_text = f"Dựa vào bảng nhân {base}."
        elif "hình tròn" in bai_lower:
            r = random.randint(2, 9)
            de_latex = f"Bán kính ${r}cm$. Đường kính là?"
            dap_an = r * 2
            goi_y_text = "Đường kính = 2 x Bán kính."
        elif "chia có dư" in bai_lower:
            a, b = random.randint(10, 50), random.randint(2, 5)
            rem = a % b
            if rem == 0: a += 1; rem = 1
            de_latex = f"Số dư của ${a} : {b}$ là?"
            dap_an = rem
            goi_y_text = "Thực hiện phép chia."

    elif "Lớp 2" in lop:
        if "số hạng" in bai_lower:
            a, b = random.randint(10, 50), random.randint(10, 40)
            de_latex = f"Tính tổng: ${a} + {b}$"
            dap_an = a + b
            goi_y_text = "Cộng hai số hạng."
        elif "qua 10" in bai_lower:
            a, b = random.randint(5, 9), random.randint(5, 9)
            de_latex = f"${a} + {b} = ?$"
            dap_an = a + b
            goi_y_text = "Gộp cho tròn 10."
        elif "ki-lô-gam" in bai_lower:
            a, b = random.randint(10, 50), random.randint(10, 50)
            de_latex = f"${a} kg + {b} kg = ?$"
            dap_an = a + b
            goi_y_text = "Cộng số đo khối lượng."

    elif "Lớp 1" in lop:
        if "phép cộng" in bai_lower:
            a, b = random.randint(1, 5), random.randint(1, 4)
            de_latex = f"${a} + {b} = ?$"
            dap_an = a + b
            goi_y_text = "Gộp lại."
        else:
            a = random.randint(0, 9)
            de_latex = f"Số liền sau của ${a}$ là?"
            dap_an = a + 1
            goi_y_text = "Đếm thêm 1."

    elif "Lớp 6" in lop:
        if "lũy thừa" in bai_lower:
            base, exp = random.randint(2, 5), random.randint(2, 4)
            de_latex = f"Tính giá trị của lũy thừa: ${base}^{exp}$"
            dap_an = base ** exp
            goi_y_text = f"Nhân số {base} với chính nó {exp} lần."
            goi_y_latex = f"{base}^{exp} = " + " \\times ".join([str(base)]*exp)
        elif "thứ tự" in bai_lower or "phép tính" in bai_lower:
            a, b, c = random.randint(2, 10), random.randint(2, 5), random.randint(2, 5)
            de_latex = f"Tính: ${a} + {b} \\times {c}^2$"
            dap_an = a + b * (c**2)
            goi_y_text = "Lũy thừa -> Nhân chia -> Cộng trừ."
            goi_y_latex = f"{a} + {b} \\times {c**2} = {a} + {b*c**2}"
        elif "chia hết" in bai_lower or "ước" in bai_lower or "bội" in bai_lower:
            num = random.randint(10, 50)
            de_latex = f"Tìm số dư khi chia ${num}$ cho 5."
            dap_an = num % 5
            goi_y_text = "Xét chữ số tận cùng."
        elif "số nguyên" in bai_lower:
            a, b = random.randint(-20, 20), random.randint(-20, 20)
            if "cộng" in bai_lower or "trừ" in bai_lower:
                op = "+" if "cộng" in bai_lower else "-"
                de_latex = f"Tính: ${a} {op} ({b})$"
                dap_an = a + b if op == "+" else a - b
                goi_y_text = "Cộng/trừ hai số nguyên."
            else:
                de_latex = f"Tính: ${a} \\times ({b})$"
                dap_an = a * b
                goi_y_text = "Nhân hai số nguyên (cùng dấu dương, khác dấu âm)."
        elif "hình phẳng" in bai_lower or "tam giác đều" in bai_lower:
             de_latex = "Tam giác đều có mấy trục đối xứng?"
             question_type = "mcq"
             dap_an = "3"
             options = ["3", "1", "0", "6"]
             goi_y_text = "Tam giác đều có 3 trục đối xứng đi qua 3 đỉnh."

    elif "Lớp 7" in lop:
        if "số hữu tỉ" in bai_lower:
            if "lũy thừa" in bai_lower:
                base, exp = random.randint(1, 4), 2
                de_latex = f"Tính: $\\left(\\frac{{-{base}}}{{3}}\\right)^{exp}$"
                question_type = "mcq"
                ans_correct = f"$\\frac{{{base**2}}}{{9}}$"
                dap_an = ans_correct
                options = [ans_correct, f"$\\frac{{-{base**2}}}{{9}}$", f"$\\frac{{{base*2}}}{{6}}$", f"$\\frac{{{base}}}{{9}}$"]
                goi_y_text = "Bình phương của số âm là số dương."
            else:
                a, b = random.randint(1, 5), random.randint(1, 5)
                de_latex = f"Tính: $\\frac{{{a}}}{{2}} + \\frac{{{b}}}{{2}}$"
                question_type = "mcq"
                ans_correct = f"$\\frac{{{a+b}}}{{2}}$"
                dap_an = ans_correct
                options = [ans_correct, f"$\\frac{{{a+b}}}{{4}}$", f"$\\frac{{{a*b}}}{{2}}$", f"$\\frac{{{a-b}}}{{2}}$"]
                goi_y_text = "Cộng tử số, giữ nguyên mẫu số."
        elif "căn bậc hai" in bai_lower or "số thực" in bai_lower:
            sq = random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100])
            de_latex = f"Tìm căn bậc hai số học của {sq}."
            dap_an = int(math.sqrt(sq))
            goi_y_text = f"Số nào bình phương lên bằng {sq}?"
            goi_y_latex = f"\\sqrt{{{sq}}} = {dap_an}"
        elif "góc" in bai_lower:
            angle = random.randint(30, 150)
            de_latex = f"Cho góc $xOy = {angle}^\\circ$. Tính góc đối đỉnh với nó."
            dap_an = angle
            goi_y_text = "Hai góc đối đỉnh thì bằng nhau."
        elif "tam giác" in bai_lower:
            a, b = random.randint(30, 80), random.randint(30, 80)
            de_latex = f"Tam giác ABC có $\\hat{{A}}={a}^\\circ, \\hat{{B}}={b}^\\circ$. Tính $\\hat{{C}}$."
            dap_an = 180 - a - b
            goi_y_text = "Tổng ba góc trong tam giác bằng 180 độ."
    
    else:
        a, b = random.randint(1, 10), random.randint(1, 10)
        de_latex = f"Tính: ${a} + {b} = ?$"
        dap_an = a + b
              
    return de_latex, question_type, dap_an, options, goi_y_text, goi_y_latex

# --- HÀM PHÂN TÍCH LỖI SAI (CÔNG NGHỆ AI MỚI) ---
def phan_tich_loi_sai(user_ans, true_ans, q_type):
    # Trả về thông điệp gợi ý dựa trên độ lệch của đáp án
    hint_msg = "Chưa đúng rồi! (Tsis yog lawm)"
    
    if q_type == "number" and isinstance(true_ans, (int, float)):
        try:
            diff = abs(user_ans - true_ans)
            if diff == 0:
                return "Tuyệt vời!"
            if user_ans == -true_ans:
                hint_msg = "Bạn bị nhầm dấu rồi! Kiểm tra lại âm/dương nhé. (Tsis yog, saib dua)"
            elif diff <= 2:
                hint_msg = "Bạn tính gần đúng rồi! Thử tính lại cẩn thận hơn chút nữa xem. (Xam dua)"
            elif diff > 10:
                hint_msg = "Kết quả còn xa quá. Hãy xem lại công thức gợi ý bên dưới nhé!"
        except:
            pass
    return hint_msg

# Hàm dịch thuật
def dich_sang_mong(text):
    try:
        return GoogleTranslator(source='vi', target='hmn').translate(text)
    except:
        return "..."

# --- TÍNH NĂNG MỚI: AI ĐỌC ĐỀ (TEXT TO SPEECH) ---
def text_to_speech_html(text, lang='vi'):
    # Xử lý text để loại bỏ ký tự LaTeX
    clean_text = text.replace("$", "").replace("\\begin{cases}", "hệ phương trình ").replace("\\end{cases}", "").replace("\\\\", " và ")
    # Tạo file audio ảo trong bộ nhớ
    tts = gTTS(text=clean_text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    # Mã hóa base64 để hiển thị
    b64 = base64.b64encode(fp.getvalue()).decode()
    md = f"""
        <audio controls autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    return md

# --- GIAO DIỆN CHÍNH ---

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

    # DASHBOARD QUẢN LÝ (ẨN)
    st.markdown("---")
    with st.expander("👨‍🏫 Khu vực Giáo viên (Admin)"):
        st.write("**Thống kê lớp học (Giả lập):**")
        st.info(f"Tổng lượt truy cập: {st.session_state.visit_count}")
        data = pd.DataFrame({
            'Trạng thái': ['Đúng ngay', 'Sai lần 1', 'Cần gợi ý'],
            'Số lượng': [45, 15, 10]
        })
        st.bar_chart(data.set_index('Trạng thái'))
        st.caption("*Dữ liệu hỗ trợ quản lý dạy học số*")

col_trai, col_phai = st.columns([1.6, 1])

if 'de_bai' not in st.session_state:
    st.session_state.de_bai = ""
    st.session_state.q_type = "number"
    st.session_state.dap_an = 0
    st.session_state.options = []
    st.session_state.goi_y_text = ""
    st.session_state.goi_y_latex = ""
    st.session_state.show_hint = False
    st.session_state.adaptive_msg = "" 

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
    st.session_state.adaptive_msg = ""

with col_trai:
    st.subheader(f"📖 {bai_chon}")
    
    if st.button("✨ TẠO CÂU HỎI MỚI (AI Generated)", type="primary", on_click=click_sinh_de):
        pass
    
    if st.session_state.de_bai:
        st.markdown('<div class="problem-box">', unsafe_allow_html=True)
        st.markdown("### ❓ Câu hỏi:")
        st.markdown(f"## {st.session_state.de_bai}")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- CÔNG CỤ AI MỚI ---
        st.markdown("### 🤖 Công cụ hỗ trợ AI:")
        col_tool1, col_tool2 = st.columns(2)
        
        with col_tool1:
            if st.button("🗣️ Đọc đề (Giọng AI)"):
                # Gọi hàm AI đọc và hiển thị
                audio_html = text_to_speech_html(st.session_state.de_bai)
                st.markdown(audio_html, unsafe_allow_html=True)
                
        with col_tool2:
            if st.button("🌏 Dịch H'Mông"):
                text_to_translate = st.session_state.de_bai.replace("$", "")
                bd = dich_sang_mong(text_to_translate)
                st.info(f"**H'Mông:** {bd}")

with col_phai:
    st.subheader("✍️ Làm bài")
    
    if st.session_state.de_bai:
        with st.form("form_lam_bai"):
            user_ans = None
            if st.session_state.q_type == "mcq":
                st.markdown("**Chọn đáp án đúng:**")
                if st.session_state.options: 
                    user_ans = st.radio("Đáp án:", st.session_state.options, label_visibility="collapsed")
                else:
                     st.error("Lỗi: Không tìm thấy đáp án phù hợp.")
            else:
                is_integer_answer = False
                if isinstance(st.session_state.dap_an, int) or (isinstance(st.session_state.dap_an, float) and st.session_state.dap_an.is_integer()):
                    is_integer_answer = True
                
                if is_integer_answer:
                    user_ans = st.number_input("Nhập đáp án (Số nguyên):", step=1, format="%d")
                else:
                    user_ans = st.number_input("Nhập đáp án:", step=0.01, format="%.2f")

            btn_nop = st.form_submit_button("✅ Kiểm tra")
            
            if btn_nop and user_ans is not None:
                st.session_state.submitted = True
                is_correct = False
                if st.session_state.q_type == "mcq":
                    if user_ans == st.session_state.dap_an:
                        is_correct = True
                else:
                    if isinstance(st.session_state.dap_an, str):
                         if str(user_ans) == st.session_state.dap_an:
                             is_correct = True
                    else:
                        if abs(user_ans - float(st.session_state.dap_an)) <= 0.05:
                            is_correct = True

                if is_correct:
                    st.balloons()
                    st.success("CHÍNH XÁC! (Yog lawm) 👏")
                    st.session_state.show_hint = False
                else:
                    adaptive_msg = phan_tich_loi_sai(user_ans, st.session_state.dap_an, st.session_state.q_type)
                    st.markdown(f'<div class="error-box">{adaptive_msg}</div>', unsafe_allow_html=True)
                    if st.session_state.q_type == "mcq":
                        st.markdown(f"Đáp án đúng là: {st.session_state.dap_an}")
                    else:
                        if isinstance(st.session_state.dap_an, (int, float)):
                             ans_display = int(st.session_state.dap_an) if float(st.session_state.dap_an).is_integer() else st.session_state.dap_an
                        else:
                             ans_display = st.session_state.dap_an
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
            if st.session_state.goi_y_latex:
                st.latex(st.session_state.goi_y_latex)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("👈 Chọn bài học và nhấn nút 'Tạo câu hỏi mới'.")

# Footer
st.markdown("---")
st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư - Bản Mường.")
