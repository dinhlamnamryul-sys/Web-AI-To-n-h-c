import streamlit as st
import random
import math
import time
import os
from deep_translator import GoogleTranslator

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
            f.write("5000")
            return 5000
    try:
        with open(count_file, "r") as f:
            content = f.read().strip()
            count = int(content) if content else 5000
    except Exception:
        count = 5000
    count += 1
    try:
        with open(count_file, "w") as f:
            f.write(str(count))
    except Exception:
        pass
    return count

if 'visit_count' not in st.session_state:
    st.session_state.visit_count = update_visit_count()

# --- DỮ LIỆU CHƯƠNG TRÌNH HỌC (CẬP NHẬT CHUẨN SGK KẾT NỐI TRI THỨC) ---
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
        "Chương 1: Đa thức": ["Cộng trừ đa thức", "Nhân đơn thức với đa thức", "Nhân đa thức với đa thức", "Chia đa thức cho đơn thức"],
        "Chương 2: Hằng đẳng thức đáng nhớ": ["Bình phương của một tổng/hiệu", "Hiệu hai bình phương", "Lập phương của một tổng/hiệu"],
        "Chương 3: Phân thức đại số": ["Cộng trừ phân thức", "Nhân chia phân thức"],
        "Chương 4: Hàm số và Đồ thị": ["Hàm số bậc nhất y = ax + b", "Hệ số góc của đường thẳng"]
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

    # ==========================================
    # LỚP 4 (CẬP NHẬT THEO SGK KNTT)
    # ==========================================
    if "Lớp 4" in lop:
        # Chủ đề 1: Ôn tập và bổ sung
        if "ôn tập" in bai_lower:
            a = random.randint(10000, 90000)
            de_latex = f"Số liền sau của số ${a}$ là?"
            dap_an = a + 1
            goi_y_text = "Cộng thêm 1 đơn vị vào hàng đơn vị."
        elif "biểu thức" in bai_lower:
            a = random.randint(5, 20)
            b = random.randint(2, 9)
            de_latex = f"Tính giá trị của biểu thức $a \\times b$ với $a={a}, b={b}$"
            dap_an = a * b
            goi_y_text = "Thay giá trị của chữ vào biểu thức rồi tính."

        # Chủ đề 2: Góc và Đơn vị đo
        elif "góc" in bai_lower:
            question_type = "mcq"
            de_latex = "Góc bẹt bằng bao nhiêu độ?"
            dap_an = "180 độ"
            options = ["90 độ", "180 độ", "60 độ", "360 độ"]
            goi_y_text = "Góc bẹt bằng hai lần góc vuông."
        elif "đơn vị" in bai_lower or "yến" in bai_lower or "tạ" in bai_lower or "giây" in bai_lower:
            if "yến" in bai_lower or "tạ" in bai_lower or "tấn" in bai_lower:
                val = random.randint(2, 10)
                unit_type = random.choice(["yến", "tạ", "tấn"])
                if unit_type == "yến":
                    de_latex = f"Đổi: ${val}$ yến = ... kg"
                    dap_an = val * 10
                    goi_y_text = "1 yến = 10 kg"
                elif unit_type == "tạ":
                    de_latex = f"Đổi: ${val}$ tạ = ... kg"
                    dap_an = val * 100
                    goi_y_text = "1 tạ = 100 kg"
                else:
                    de_latex = f"Đổi: ${val}$ tấn = ... kg"
                    dap_an = val * 1000
                    goi_y_text = "1 tấn = 1000 kg"
            elif "giây" in bai_lower or "thế kỷ" in bai_lower:
                if random.choice([True, False]):
                     m = random.randint(2, 10)
                     de_latex = f"Đổi: ${m}$ phút = ... giây"
                     dap_an = m * 60
                     goi_y_text = "1 phút = 60 giây"
                else:
                     tk = random.randint(1, 10)
                     de_latex = f"Đổi: ${tk}$ thế kỷ = ... năm"
                     dap_an = tk * 100
                     goi_y_text = "1 thế kỷ = 100 năm"

        # Chủ đề 3: Số có nhiều chữ số
        elif "số có nhiều chữ số" in bai_lower or "lớp triệu" in bai_lower:
            a = random.randint(100000, 999999)
            b = random.randint(100000, 999999)
            de_latex = f"So sánh hai số: ${a} \\dots {b}$"
            question_type = "mcq"
            if a > b: ans_correct = ">"; options=[">", "<", "="]
            elif a < b: ans_correct = "<"; options=["<", ">", "="]
            else: ans_correct = "="; options=["=", ">", "<"]
            dap_an = ans_correct
            goi_y_text = "So sánh từng hàng từ trái sang phải."
        elif "làm tròn" in bai_lower:
            base = random.randint(100000, 999999)
            de_latex = f"Làm tròn số ${base}$ đến hàng trăm nghìn."
            dap_an = round(base, -5)
            goi_y_text = "Xét chữ số hàng chục nghìn. Nếu >= 5 thì làm tròn lên."

        # Chủ đề 4: Phép cộng, trừ
        elif "cộng" in bai_lower or "trừ" in bai_lower:
            a = random.randint(10000, 99999)
            b = random.randint(1000, 9999)
            if "cộng" in bai_lower:
                de_latex = f"Đặt tính rồi tính: ${a} + {b}$"
                dap_an = a + b
            else:
                de_latex = f"Đặt tính rồi tính: ${a} - {b}$"
                dap_an = a - b
            goi_y_text = "Tính từ phải sang phải, nhớ (hoặc mượn) nếu cần."
        elif "trung bình cộng" in bai_lower:
            n1 = random.randint(10, 50)
            n2 = random.randint(10, 50)
            n3 = random.randint(10, 50)
            # Điều chỉnh cho chia hết
            total = n1 + n2 + n3
            rem = total % 3
            n3 = n3 - rem
            total = n1 + n2 + n3
            de_latex = f"Tìm trung bình cộng của: ${n1}, {n2}, {n3}$"
            dap_an = total // 3
            goi_y_text = "Cộng tổng các số lại rồi chia cho số các số hạng (3)."

        # Chủ đề 5: Phép nhân, chia
        elif "nhân" in bai_lower:
            a = random.randint(100, 999)
            b = random.randint(10, 99)
            de_latex = f"Tính: ${a} \\times {b}$"
            dap_an = a * b
            goi_y_text = "Nhân lần lượt từng chữ số rồi cộng các tích riêng."
        elif "chia" in bai_lower:
            b = random.randint(10, 50)
            res = random.randint(10, 50)
            a = b * res
            de_latex = f"Tính: ${a} : {b}$"
            dap_an = res
            goi_y_text = "Chia theo thứ tự từ trái sang phải."
            
    # ==========================================
    # LỚP 5 (CẬP NHẬT THEO SGK KNTT)
    # ==========================================
    elif "Lớp 5" in lop:
        # Chủ đề 1: Ôn tập và bổ sung
        if "phân số" in bai_lower or "hỗn số" in bai_lower:
            if "hỗn số" in bai_lower:
                nguyen = random.randint(1, 5)
                tu = random.randint(1, 4)
                mau = random.randint(tu + 1, 9)
                de_latex = f"Chuyển hỗn số ${nguyen}\\frac{{{tu}}}{{{mau}}}$ thành phân số (Nhập tử số, biết mẫu số là {mau})."
                dap_an = nguyen * mau + tu
                goi_y_text = "Tử số mới = Phần nguyên x Mẫu số + Tử số cũ."
            else: # Ôn tập phân số
                tu1 = random.randint(1, 5)
                mau1 = random.randint(2, 6)
                tu2 = random.randint(1, 5)
                mau2 = random.randint(2, 6)
                de_latex = f"Tính: $\\frac{{{tu1}}}{{{mau1}}} + \\frac{{{tu2}}}{{{mau2}}}$ (Viết kết quả dưới dạng số thập phân làm tròn 2 chữ số)"
                val = (tu1/mau1) + (tu2/mau2)
                dap_an = round(val, 2)
                goi_y_text = "Quy đồng mẫu số rồi thực hiện phép tính."
                
        # Chủ đề 2: Số thập phân
        elif "số thập phân" in bai_lower and ("khái niệm" in bai_lower or "so sánh" in bai_lower or "làm tròn" in bai_lower):
            if "so sánh" in bai_lower:
                a = round(random.uniform(1, 100), 2)
                b = round(random.uniform(1, 100), 2)
                de_latex = f"So sánh: ${a} \\dots {b}$"
                question_type = "mcq"
                if a > b: ans_correct = ">"; options=[">", "<", "="]
                elif a < b: ans_correct = "<"; options=["<", ">", "="]
                else: ans_correct = "="; options=["=", ">", "<"]
                dap_an = ans_correct
                goi_y_text = "So sánh phần nguyên trước, sau đó đến phần thập phân."
            elif "làm tròn" in bai_lower:
                val = round(random.uniform(10, 50), 3)
                de_latex = f"Làm tròn số ${val}$ đến hàng phần mười."
                dap_an = round(val, 1)
                goi_y_text = "Xét chữ số hàng phần trăm (sau dấu phẩy thứ 2)."
            else:
                a = random.randint(1, 100)
                de_latex = f"Viết phân số $\\frac{{{a}}}{{100}}$ dưới dạng số thập phân."
                dap_an = a / 100
                question_type = "number"
                goi_y_text = "Dịch dấu phẩy sang trái 2 chữ số."

        # Chủ đề 3: Phép tính với số thập phân (Cộng, Trừ, Nhân, Chia)
        elif "phép tính" in bai_lower or "cộng" in bai_lower or "trừ" in bai_lower or "nhân" in bai_lower or "chia" in bai_lower:
            a = round(random.uniform(1, 50), 1)
            b = round(random.uniform(1, 20), 1)
            if "cộng" in bai_lower:
                de_latex = f"Tính: ${a} + {b} = ?$"
                dap_an = round(a + b, 2)
                goi_y_text = "Đặt dấu phẩy thẳng cột."
            elif "trừ" in bai_lower:
                if a < b: a, b = b, a
                de_latex = f"Tính: ${a} - {b} = ?$"
                dap_an = round(a - b, 2)
                goi_y_text = "Đặt dấu phẩy thẳng cột."
            elif "nhân" in bai_lower:
                a = round(random.uniform(1, 10), 1)
                b = random.randint(2, 9)
                de_latex = f"Tính: ${a} \\times {b} = ?$"
                dap_an = round(a * b, 2)
                goi_y_text = "Nhân như số tự nhiên, đếm số chữ số thập phân để đặt dấu phẩy."
            elif "chia" in bai_lower:
                res = round(random.uniform(1, 10), 1)
                b = random.randint(2, 9)
                a = round(res * b, 1)
                de_latex = f"Tính: ${a} : {b} = ?$"
                dap_an = res
                goi_y_text = "Chia như số tự nhiên. Khi chia hết phần nguyên, đánh dấu phẩy vào thương."
            else: # Fallback for general topic selection
                de_latex = f"Tính: ${a} + {b} = ?$"
                dap_an = round(a + b, 2)
                goi_y_text = "Thực hiện phép tính."

        # Chủ đề 4: Hình học
        elif "hình học" in bai_lower or "tam giác" in bai_lower or "hình thang" in bai_lower or "hình tròn" in bai_lower:
            if "tam giác" in bai_lower:
                a = random.randint(5, 20)
                h = random.randint(5, 20)
                de_latex = f"Tính diện tích hình tam giác có đáy $a={a}cm$ và chiều cao $h={h}cm$."
                dap_an = (a * h) / 2
                goi_y_text = "Diện tích tam giác = (đáy x chiều cao) : 2"
                goi_y_latex = f"S = \\frac{{{a} \\times {h}}}{{2}}"
            elif "hình thang" in bai_lower:
                a = random.randint(5, 15)
                b = random.randint(16, 30)
                h = random.randint(5, 10)
                de_latex = f"Tính diện tích hình thang có đáy bé ${a}cm$, đáy lớn ${b}cm$, chiều cao ${h}cm$."
                dap_an = ((a + b) * h) / 2
                goi_y_text = "Diện tích hình thang = (đáy lớn + đáy bé) x chiều cao : 2"
                goi_y_latex = f"S = \\frac{{({a} + {b}) \\times {h}}}{{2}}"
            elif "hình tròn" in bai_lower:
                r = random.randint(2, 10)
                if random.choice([True, False]):
                    de_latex = f"Tính chu vi hình tròn bán kính $r={r}cm$."
                    dap_an = round(r * 2 * 3.14, 2)
                    goi_y_text = "Chu vi = bán kính x 2 x 3,14"
                else:
                    de_latex = f"Tính diện tích hình tròn bán kính $r={r}cm$."
                    dap_an = round(r * r * 3.14, 2)
                    goi_y_text = "Diện tích = bán kính x bán kính x 3,14"
            else: # Fallback
                de_latex = "Hình hộp chữ nhật có mấy mặt?"
                dap_an = 6
                question_type = "number"
                goi_y_text = "Hình hộp chữ nhật có 6 mặt (2 đáy và 4 mặt bên)."

    # ==========================================
    # LỚP 3 (CẬP NHẬT THEO SGK MỚI - NHƯ YÊU CẦU TRƯỚC)
    # ==========================================
    elif "Lớp 3" in lop:
        # Chủ đề 1: Ôn tập và bổ sung
        if "ôn tập" in bai_lower or "tìm thành phần" in bai_lower:
            if "số đến 1000" in bai_lower:
                a = random.randint(100, 899)
                de_latex = f"Số liền sau của số ${a}$ là số mấy?"
                dap_an = a + 1
                goi_y_text = "Đếm thêm 1 đơn vị."
            else: # Tìm thành phần phép tính
                a = random.randint(10, 100)
                b = random.randint(10, 100)
                tong = a + b
                de_latex = f"Tìm số hạng chưa biết: $? + {a} = {tong}$"
                dap_an = b
                goi_y_text = "Muốn tìm số hạng chưa biết, ta lấy Tổng trừ đi số hạng kia."
                goi_y_latex = f"{tong} - {a} = {b}"

        # Chủ đề 2: Bảng nhân, bảng chia (6, 7, 8, 9)
        elif "bảng nhân" in bai_lower or "bảng chia" in bai_lower:
            base = random.randint(6, 9)
            if "nhân" in bai_lower:
                mult = random.randint(2, 9)
                de_latex = f"Tính nhẩm: ${base} \\times {mult} = ?$"
                dap_an = base * mult
                goi_y_text = f"Dựa vào bảng nhân {base}."
            else:
                quotient = random.randint(2, 9)
                product = base * quotient
                de_latex = f"Tính nhẩm: ${product} : {base} = ?$"
                dap_an = quotient
                goi_y_text = f"Dựa vào bảng chia {base}."
        
        elif "một phần mấy" in bai_lower:
            part = random.randint(2, 9)
            total = part * random.randint(2, 10)
            de_latex = f"Một phần {part} của {total} là bao nhiêu?"
            dap_an = total // part
            goi_y_text = f"Lấy {total} chia cho {part}."
            goi_y_latex = f"{total} : {part} = {dap_an}"

        # Chủ đề 3: Hình phẳng, hình khối
        elif "trung điểm" in bai_lower:
            l = random.randint(4, 20) * 2
            de_latex = f"Đoạn thẳng AB dài ${l}cm$. M là trung điểm của AB. Tính độ dài đoạn AM."
            dap_an = l // 2
            goi_y_text = "Trung điểm chia đoạn thẳng làm 2 phần bằng nhau."
        elif "hình tròn" in bai_lower:
            r = random.randint(2, 9)
            de_latex = f"Hình tròn tâm O có bán kính ${r}cm$. Đường kính của hình tròn dài bao nhiêu?"
            dap_an = r * 2
            goi_y_text = "Đường kính dài gấp 2 lần bán kính."
        elif "góc" in bai_lower:
            question_type = "mcq"
            de_latex = "Góc vuông có đỉnh và cạnh như thế nào?"
            dap_an = "Đỉnh vuông góc, hai cạnh vuông góc"
            options = ["Đỉnh vuông góc, hai cạnh vuông góc", "Đỉnh nhọn", "Đỉnh tù"]
            goi_y_text = "Sử dụng ê-ke để kiểm tra góc vuông."
        elif "hình tam giác" in bai_lower or "tứ giác" in bai_lower:
            de_latex = "Hình tam giác có mấy cạnh?"
            dap_an = 3
            question_type = "number"
            goi_y_text = "Tam giác có 3 cạnh, 3 đỉnh."

        # Chủ đề 4: Phép nhân chia phạm vi 100
        elif "nhân số" in bai_lower and "100" in bai_lower: # Nhân 2 chữ số với 1 chữ số
            a = random.randint(12, 49)
            b = random.randint(2, 5)
            de_latex = f"Đặt tính rồi tính: ${a} \\times {b}$"
            dap_an = a * b
            goi_y_text = "Nhân lần lượt từ hàng đơn vị sang hàng chục."
        elif "chia số" in bai_lower and "100" in bai_lower:
            a = random.randint(20, 99)
            b = random.randint(2, 9)
            de_latex = f"Tính: ${a} : {b}$ (Lấy phần nguyên)"
            dap_an = a // b
            goi_y_text = "Chia từ trái sang phải."
        elif "chia có dư" in bai_lower:
            a = random.randint(10, 50)
            b = random.randint(2, 5)
            rem = a % b
            if rem == 0: a += 1; rem = 1 # Đảm bảo có dư
            de_latex = f"Tìm số dư của phép chia: ${a} : {b}$"
            dap_an = rem
            goi_y_text = "Thực hiện chia, phần còn lại nhỏ hơn số chia là số dư."
        elif "gấp" in bai_lower or "giảm" in bai_lower:
            val = random.randint(4, 20)
            k = random.randint(2, 5)
            if "gấp" in bai_lower:
                de_latex = f"Gấp số ${val}$ lên ${k}$ lần được bao nhiêu?"
                dap_an = val * k
                goi_y_text = "Thực hiện phép nhân."
            else:
                val = val * k # Đảm bảo chia hết
                de_latex = f"Giảm số ${val}$ đi ${k}$ lần được bao nhiêu?"
                dap_an = val // k
                goi_y_text = "Thực hiện phép chia."

        # Chủ đề 5: Đơn vị đo lường
        elif "mi-li-mét" in bai_lower:
            cm = random.randint(1, 10)
            de_latex = f"Đổi: ${cm}cm = ... mm$"
            dap_an = cm * 10
            goi_y_text = "1 cm = 10 mm"
        elif "gam" in bai_lower:
            kg = random.randint(1, 5)
            de_latex = f"Đổi: ${kg}kg = ... g$"
            dap_an = kg * 1000
            goi_y_text = "1 kg = 1000 g"
        elif "nhiệt độ" in bai_lower:
             de_latex = "Nước sôi ở bao nhiêu độ C?"
             dap_an = 100
             question_type = "number"
             goi_y_text = "Nước sôi ở 100 độ C."

        # Chủ đề 6: Phép nhân chia phạm vi 1000
        elif "biểu thức" in bai_lower:
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            c = random.randint(10, 50)
            de_latex = f"Tính giá trị biểu thức: ${c} + {a} \\times {b}$"
            dap_an = c + (a * b)
            goi_y_text = "Nhân chia trước, cộng trừ sau."
            goi_y_latex = f"{c} + {a*b} = {c + a*b}"
        elif "nhân số" in bai_lower and "1000" in bai_lower:
            a = random.randint(101, 200)
            b = random.randint(2, 4)
            de_latex = f"Tính: ${a} \\times {b}$"
            dap_an = a * b
            goi_y_text = "Nhân từ phải sang trái."
        elif "chia số" in bai_lower and "1000" in bai_lower:
            b = random.randint(2, 5)
            a = random.randint(100, 200) * b
            de_latex = f"Tính: ${a} : {b}$"
            dap_an = a // b
            goi_y_text = "Chia từ trái sang phải."


    # ==========================================
    # LỚP 2 (CẬP NHẬT THEO SGK MỚI)
    # ==========================================
    elif "Lớp 2" in lop:
        # --- Chủ đề 1: Ôn tập và bổ sung ---
        if "số hạng" in bai_lower or "tổng" in bai_lower:
            a = random.randint(10, 50)
            b = random.randint(10, 40)
            if random.choice([True, False]):
                de_latex = f"Tính tổng của ${a}$ và ${b}$."
                dap_an = a + b
                goi_y_text = "Thực hiện phép cộng: Số hạng + Số hạng = Tổng."
                goi_y_latex = f"{a} + {b} = {a+b}"
            else:
                tong = a + b
                de_latex = f"Tìm số hạng chưa biết: $? + {b} = {tong}$"
                dap_an = a
                goi_y_text = "Muốn tìm số hạng chưa biết, lấy Tổng trừ đi số hạng kia."
                goi_y_latex = f"{tong} - {b} = {a}"
        elif "số trừ" in bai_lower or "hiệu" in bai_lower or "phép trừ" in bai_lower and "ôn tập" in bai_lower:
            a = random.randint(20, 90) # Số bị trừ
            b = random.randint(10, a)  # Số trừ
            hieu = a - b
            dang_toan = random.choice(["tim_hieu", "tim_sbt", "tim_st"])
            
            if dang_toan == "tim_hieu":
                de_latex = f"Số bị trừ là ${a}$, số trừ là ${b}$. Tìm hiệu."
                dap_an = hieu
                goi_y_text = "Hiệu = Số bị trừ - Số trừ."
                goi_y_latex = f"{a} - {b} = {hieu}"
            elif dang_toan == "tim_sbt":
                de_latex = f"Tìm số bị trừ: $? - {b} = {hieu}$"
                dap_an = a
                goi_y_text = "Muốn tìm Số bị trừ, lấy Hiệu cộng với Số trừ."
                goi_y_latex = f"{hieu} + {b} = {a}"
            else:
                de_latex = f"Tìm số trừ: ${a} - ? = {hieu}$"
                dap_an = b
                goi_y_text = "Muốn tìm Số trừ, lấy Số bị trừ trừ đi Hiệu."
                goi_y_latex = f"{a} - {hieu} = {b}"
        elif "tia số" in bai_lower or "liền trước" in bai_lower:
            val = random.randint(10, 90)
            de_latex = f"Số liền trước và số liền sau của ${val}$ là?"
            question_type = "mcq"
            ans_correct = f"{val-1} và {val+1}"
            dap_an = ans_correct
            options = [f"{val-1} và {val+1}", f"{val-2} và {val+2}", f"{val} và {val+2}"]
            goi_y_text = "Số liền trước bớt 1 đơn vị, số liền sau thêm 1 đơn vị."
        
        # --- Chủ đề 2: Phép cộng trừ qua 10 (phạm vi 20) ---
        elif "qua 10" in bai_lower and "cộng" in bai_lower:
            a = random.randint(2, 9)
            b = random.randint(11-a, 9) 
            de_latex = f"Tính nhẩm: ${a} + {b} = ?$"
            dap_an = a + b
            goi_y_text = f"Gộp cho đủ 10 rồi cộng số còn lại. Ví dụ: {a} + {10-a} + ..."
            goi_y_latex = f"{a} + {b} = {a+b}"
        elif "qua 10" in bai_lower and "trừ" in bai_lower:
            a = random.randint(11, 18)
            b = random.randint(a-9, 9) 
            de_latex = f"Tính nhẩm: ${a} - {b} = ?$"
            dap_an = a - b
            goi_y_text = "Trừ để được 10 rồi trừ tiếp số còn lại."
            goi_y_latex = f"{a} - {b} = {a-b}"
        elif "thêm" in bai_lower or "bớt" in bai_lower or "nhiều hơn" in bai_lower or "ít hơn" in bai_lower:
            val = random.randint(5, 15)
            delta = random.randint(2, 5)
            if "thêm" in bai_lower or "nhiều hơn" in bai_lower:
                de_latex = f"Trên sân có ${val}$ con gà. Có thêm ${delta}$ con chạy tới. Hỏi có tất cả bao nhiêu con?"
                dap_an = val + delta
                goi_y_text = "Thực hiện phép cộng."
                goi_y_latex = f"{val} + {delta} = {val+delta}"
            else:
                de_latex = f"Mẹ có ${val}$ quả cam. Mẹ biếu bà ${delta}$ quả. Hỏi mẹ còn lại bao nhiêu quả?"
                dap_an = val - delta
                goi_y_text = "Thực hiện phép trừ."
                goi_y_latex = f"{val} - {delta} = {val-delta}"

        # --- Chủ đề 3: Khối lượng, dung tích ---
        elif "ki-lô-gam" in bai_lower:
            a = random.randint(5, 40)
            b = random.randint(5, 40)
            op = random.choice(['+', '-'])
            if op == '-':
                lon, be = max(a, b), min(a, b)
                de_latex = f"Tính: ${lon} kg - {be} kg = ?$"
                dap_an = lon - be
            else:
                de_latex = f"Tính: ${a} kg + {b} kg = ?$"
                dap_an = a + b
            goi_y_text = "Cộng/trừ số đo khối lượng như số tự nhiên."
        elif "lít" in bai_lower:
            a = random.randint(2, 30)
            b = random.randint(2, 30)
            de_latex = f"Can xanh đựng ${a}l$, can đỏ đựng ${b}l$. Cả hai can đựng bao nhiêu lít?"
            dap_an = a + b
            goi_y_text = "Cộng dung tích hai can lại."
            goi_y_latex = f"{a} + {b} = {a+b}"

        # --- Chủ đề 4: Phép cộng trừ có nhớ (phạm vi 100) ---
        elif "có nhớ" in bai_lower:
            if "cộng" in bai_lower:
                u1 = random.randint(5, 9)
                u2 = random.randint(10-u1, 9) 
                t1 = random.randint(1, 7)
                t2 = random.randint(1, 8-t1)
                de_latex = f"Đặt tính rồi tính: ${t1*10+u1} + {t2*10+u2}$"
                dap_an = (t1*10+u1) + (t2*10+u2)
                goi_y_text = "Cộng hàng đơn vị trước, nhớ 1 sang hàng chục."
            else: # Trừ có nhớ
                u1 = random.randint(0, 8)
                u2 = random.randint(u1+1, 9)
                t1 = random.randint(3, 9)
                t2 = random.randint(1, t1-1)
                num1 = t1*10 + u1
                num2 = t2*10 + u2
                de_latex = f"Đặt tính rồi tính: ${num1} - {num2}$"
                dap_an = num1 - num2
                goi_y_text = "Hàng đơn vị không trừ được, mượn 1 ở hàng chục."

        # --- Chủ đề 5: Hình phẳng ---
        elif "đoạn thẳng" in bai_lower or "đường gấp khúc" in bai_lower or "điểm" in bai_lower:
            if "gấp khúc" in bai_lower:
                a = random.randint(2, 6)
                b = random.randint(2, 6)
                c = random.randint(2, 6)
                de_latex = f"Đường gấp khúc ABC có đoạn AB dài ${a}cm$, đoạn BC dài ${b}cm$, đoạn CD dài ${c}cm$. Tính độ dài đường gấp khúc."
                dap_an = a + b + c
                goi_y_text = "Cộng độ dài tất cả các đoạn thẳng thành phần."
            elif "thẳng hàng" in bai_lower:
                de_latex = "Ba điểm thẳng hàng là ba điểm như thế nào?"
                question_type = "mcq"
                dap_an = "Cùng nằm trên một đường thẳng"
                options = ["Cùng nằm trên một đường thẳng", "Tạo thành hình tam giác", "Cách đều nhau"]
                goi_y_text = "Ba điểm cùng nằm trên một đường thẳng gọi là 3 điểm thẳng hàng."
            else:
                de_latex = f"Đoạn thẳng AB dài 10cm. Điểm I nằm giữa A và B sao cho AI = 4cm. Tính IB."
                dap_an = 6
                goi_y_text = "IB = AB - AI."

        elif "tứ giác" in bai_lower:
            de_latex = "Hình tứ giác có mấy cạnh và mấy đỉnh?"
            question_type = "mcq"
            dap_an = "4 cạnh, 4 đỉnh"
            options = ["3 cạnh, 3 đỉnh", "4 cạnh, 4 đỉnh", "5 cạnh, 5 đỉnh"]
            goi_y_text = "Tứ giác là hình có 4 cạnh."

        # --- Chủ đề 6: Ngày giờ ---
        elif "ngày" in bai_lower or "giờ" in bai_lower or "lịch" in bai_lower:
            if "lịch" in bai_lower or "tháng" in bai_lower:
                de_latex = "Tháng 12 có bao nhiêu ngày?"
                dap_an = 31
                question_type = "number"
                goi_y_text = "Ghi nhớ số ngày trong các tháng (Dùng quy tắc nắm tay)."
            else:
                h = random.randint(1, 11)
                de_latex = f"Đồng hồ chỉ ${h}$ giờ. 30 phút sau là mấy giờ?"
                question_type = "mcq"
                dap_an = f"{h} giờ 30 phút"
                options = [f"{h} giờ 30 phút", f"{h+1} giờ", f"{h} giờ 15 phút"]
                goi_y_text = "Kim phút chỉ số 6 là 30 phút."

    # ==========================================
    # LỚP 1 (GIỮ NGUYÊN)
    # ==========================================
    elif "Lớp 1" in lop:
        if "các số" in bai_lower:
            a = random.randint(0, 9)
            de_latex = f"Số liền sau của số ${a}$ là số mấy?"
            dap_an = a + 1
            goi_y_text = "Đếm thêm 1 đơn vị."
            goi_y_latex = f"{a} + 1 = {a+1}"
        elif "so sánh" in bai_lower:
            a, b = random.randint(0, 10), random.randint(0, 10)
            while a == b:
                b = random.randint(0, 10)
            de_latex = f"Điền dấu thích hợp: ${a} \\dots {b}$"
            question_type = "mcq"
            if a > b: 
                ans_correct = "$>$"
                options = [">", "<", "="]
            elif a < b: 
                ans_correct = "$<$"
                options = ["<", ">", "="]
            else: 
                ans_correct = "$=$"
                options = ["=", ">", "<"]
            dap_an = ans_correct
            goi_y_text = "So sánh số lượng xem bên nào nhiều hơn."
        elif "mấy và mấy" in bai_lower:
            tong = random.randint(3, 9)
            a = random.randint(1, tong - 1)
            b = tong - a
            de_latex = f"Số ${tong}$ gồm ${a}$ và mấy?"
            dap_an = b
            goi_y_text = "Dùng phép trừ để tìm số còn thiếu."
            goi_y_latex = f"{tong} - {a} = {b}"
        elif "hình" in bai_lower and "phẳng" in bai_lower:
            shapes = [("Hình tam giác", 3), ("Hình vuông", 4)]
            shape_name, sides = random.choice(shapes)
            de_latex = f"{shape_name} có bao nhiêu cạnh?"
            dap_an = sides
            goi_y_text = "Đếm số đường thẳng tạo nên hình đó."
        elif "phép cộng" in bai_lower:
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            de_latex = f"Tính: ${a} + {b} = ?$"
            dap_an = a + b
            goi_y_text = "Gộp hai nhóm lại với nhau."
            goi_y_latex = f"{a} + {b} = {a+b}"
        elif "phép trừ" in bai_lower:
            a = random.randint(2, 10)
            b = random.randint(1, a)
            de_latex = f"Tính: ${a} - {b} = ?$"
            dap_an = a - b
            goi_y_text = "Bớt đi số lượng tương ứng."
            goi_y_latex = f"{a} - {b} = {a-b}"
        elif "khối" in bai_lower:
            question_type = "mcq"
            de_latex = "Viên xúc xắc có dạng khối gì?"
            dap_an = "Khối lập phương"
            options = ["Khối lập phương", "Khối hộp chữ nhật", "Khối cầu"]
            goi_y_text = "Các mặt của xúc xắc đều là hình vuông."

    # ==========================================
    # CẤP 2: LỚP 8 (GIỮ NGUYÊN)
    # ==========================================
    elif "Lớp 8" in lop:
        question_type = "mcq"
        if "đa thức" in bai_lower:
            if "cộng trừ" in bai_lower:
                a1, b1 = random.randint(2, 5), random.randint(1, 9)
                a2, b2 = random.randint(2, 5), random.randint(1, 9)
                op = random.choice(['+', '-'])
                if op == '+':
                    de_latex = f"Rút gọn: $({a1}x^2 + {b1}xy) + ({a2}x^2 + {b2}xy)$"
                    res_a, res_b = a1 + a2, b1 + b2
                else:
                    de_latex = f"Rút gọn: $({a1}x^2 + {b1}xy) - ({a2}x^2 + {b2}xy)$"
                    res_a, res_b = a1 - a2, b1 - b2
                ans_correct = f"${res_a}x^2 {res_b:+d}xy$"
                dap_an = ans_correct
                options = [ans_correct, f"${res_a}x^2 {-res_b:+d}xy$", f"${a1+a2}x^2 {b1+b2:+d}xy$", f"${res_a}x^2 + {res_b*2}xy$"]
                goi_y_text = "Cộng/trừ các hạng tử đồng dạng."
                goi_y_latex = f"({a1}x^2 + {a2}x^2) {op} ({b1}xy {op} {b2}xy)"
            elif "nhân đơn thức" in bai_lower:
                k = random.randint(2, 5) * random.choice([1, -1])
                a, b = random.randint(1, 5), random.randint(1, 5)
                de_latex = f"Thực hiện phép tính: ${k}x(x^2 - {a}x + {b})$"
                c1, c2, c3 = k, -k*a, k*b
                ans_correct = f"${c1}x^3 {c2:+d}x^2 {c3:+d}x$"
                dap_an = ans_correct
                options = [ans_correct, f"${c1}x^3 {c2:+d}x {c3:+d}$", f"${c1}x^3 {-c2:+d}x^2 {c3:+d}x$", f"${k}x^3 - {a}x + {b}$"]
                goi_y_text = "Nhân phân phối: $A(B+C) = AB + AC$."
            elif "nhân đa thức" in bai_lower:
                a, b = random.randint(1, 5), random.randint(1, 5)
                de_latex = f"Khai triển: $(x + {a})(x - {b})$"
                mid = a - b
                end = -a * b
                ans_correct = f"$x^2 {mid:+d}x {end:+d}$"
                dap_an = ans_correct
                options = [ans_correct, f"$x^2 {mid:+d}x {abs(end):+d}$", f"$x^2 {a+b:+d}x {end:+d}$", f"$x^2 {-mid:+d}x {end:+d}$"]
                goi_y_text = "Nhân đa thức với đa thức."
            elif "chia" in bai_lower:
                k = random.randint(2, 4)
                exp = random.randint(2, 4)
                de_latex = f"Chia: $({k*3}x^{exp+1} - {k*2}x^{exp}) : {k}x^{exp-1}$"
                ans_correct = f"$3x^2 - 2x$"
                dap_an = ans_correct
                options = [ans_correct, "$3x^2 + 2x$", "$3x - 2$", "$3x^2 - 2$"]
                goi_y_text = "Chia từng hạng tử cho đơn thức."
        elif "hằng đẳng thức" in bai_lower or "bình phương" in bai_lower or "lập phương" in bai_lower or "hiệu hai" in bai_lower:
            if "bình phương" in bai_lower and "tổng" in bai_lower:
                a = random.randint(2, 6)
                de_latex = f"Khai triển: $(x + {a})^2$"
                ans_correct = f"$x^2 + {2*a}x + {a**2}$"
                dap_an = ans_correct
                options = [ans_correct, f"$x^2 + {a**2}$", f"$x^2 - {2*a}x + {a**2}$", f"$2x + {a**2}$"]
                goi_y_text = "$(A+B)^2 = A^2 + 2AB + B^2$"
            elif "hiệu" in bai_lower and "bình phương" in bai_lower:
                a = random.randint(2, 9)
                de_latex = f"Viết thành tích: $x^2 - {a**2}$"
                ans_correct = f"$(x - {a})(x + {a})$"
                dap_an = ans_correct
                options = [ans_correct, f"$(x - {a})^2$", f"$(x + {a})^2$", f"$(x - {a})(x - {a})$"]
                goi_y_text = "$A^2 - B^2 = (A-B)(A+B)$"
            elif "lập phương" in bai_lower:
                de_latex = f"Khai triển: $(x - 2)^3$"
                ans_correct = f"$x^3 - 6x^2 + 12x - 8$"
                dap_an = ans_correct
                options = [ans_correct, "$x^3 - 8$", "$x^3 + 6x^2 + 12x + 8$", "$x^3 - 6x^2 - 12x - 8$"]
                goi_y_text = "$(A-B)^3 = A^3 - 3A^2B + 3AB^2 - B^3$"
            else:
                a = random.randint(2, 5)
                de_latex = f"Tính $(x-{a})^2$"
                ans_correct = f"$x^2 - {2*a}x + {a**2}$"
                dap_an = ans_correct
                options = [ans_correct, f"$x^2+{a**2}$", f"$x^2- {a**2}$", f"$x^2 + {2*a}x + {a**2}$"]
        elif "phân thức" in bai_lower:
            question_type = "mcq"
            if "cộng" in bai_lower or "trừ" in bai_lower:
                tu1 = random.randint(1, 5)
                tu2 = random.randint(1, 5)
                de_latex = f"Cộng hai phân thức: $\\frac{{x+{tu1}}}{{x-1}} + \\frac{{2x+{tu2}}}{{x-1}}$"
                res_num = tu1 + tu2
                ans_correct = f"$\\frac{{3x+{res_num}}}{{x-1}}$"
                dap_an = ans_correct
                options = [ans_correct, f"$\\frac{{3x+{res_num}}}{{2x-2}}$", f"$\\frac{{3x}}{{{x-1}}}$", f"$\\frac{{3x+{abs(tu1-tu2)}}}{{x-1}}$"]
                goi_y_text = "Cộng tử thức với tử thức, giữ nguyên mẫu thức chung."
                goi_y_latex = f"\\frac{{A}}{{M}} + \\frac{{B}}{{M}} = \\frac{{A+B}}{{M}}"
            else: 
                a = random.randint(2, 6)
                de_latex = f"Rút gọn biểu thức: $\\frac{{x^2 - {a**2}}}{{x}} \\cdot \\frac{{x}}{{x+{a}}}$"
                ans_correct = f"$x - {a}$"
                dap_an = ans_correct
                options = [ans_correct, f"$x + {a}$", f"$\\frac{{1}}{{x+{a}}}$", f"$x^2 - {a**2}$"]
                goi_y_text = "Phân tích tử thức thành nhân tử rồi rút gọn."
                goi_y_latex = f"\\frac{{(x-{a})(x+{a})}}{{x}} \\cdot \\frac{{x}}{{x+{a}}} = x - {a}"
        elif "hàm số" in bai_lower or "hệ số góc" in bai_lower:
            if "hệ số góc" in bai_lower:
                a = random.randint(-5, 5)
                b = random.randint(1, 10)
                if a == 0: a = 2
                de_latex = f"Hệ số góc của đường thẳng $y = {a}x + {b}$ là?"
                question_type = "number"
                dap_an = a
                goi_y_text = "Hệ số góc là hệ số a đi liền với x."
            else:
                a = random.randint(2, 5)
                b = random.randint(1, 5)
                x0 = random.randint(1, 3)
                de_latex = f"Cho $y = {a}x - {b}$. Tính $y$ khi $x = {x0}$."
                question_type = "number"
                dap_an = a * x0 - b
                goi_y_text = "Thay giá trị của x vào công thức."
        if not de_latex: 
            a = random.randint(2,5)
            de_latex = f"Phân tích đa thức thành nhân tử: $x^2 - {a}x$"
            ans_correct = f"$x(x-{a})$"
            dap_an = ans_correct
            options = [ans_correct, f"$x(x+{a})$", f"$x^2(1-{a})$", f"$(x-{a})^2$"]
            goi_y_text = "Đặt nhân tử chung là x."
        random.shuffle(options)

    # ==========================================
    # CÁC LỚP CÒN LẠI (GIỮ NGUYÊN)
    # ==========================================
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
                goi_y_latex = f"\\left(\\frac{{a}}{{b}}\\right)^n = \\frac{{a^n}}{{b^n}}"
            else:
                a, b = round(random.uniform(-10, 10), 1), round(random.uniform(-10, 10), 1)
                de_latex = f"Tính: ${a} + ({b}) = ?$"
                dap_an = round(a + b, 1)
                goi_y_text = "Cộng hai số hữu tỉ."
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
            goi_y_latex = f"\\hat{{C}} = 180^\\circ - ({g1}^\\circ + {g2}^\\circ)"

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
                # Chỉ dịch phần text, không dịch phần công thức LaTeX (phần trong dấu $)
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
                else:
                    st.error(f"Chưa đúng rồi! (Tsis yog lawm)")
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
                
            # Dịch phần gợi ý sang tiếng Mông
            translation = dich_sang_mong(st.session_state.goi_y_text)
            st.markdown('<div class="hmong-hint">', unsafe_allow_html=True)
            st.markdown(f"**🗣️ H'Mông:** {translation}")
            # Hiển thị công thức toán riêng để không bị lỗi dịch
            if st.session_state.goi_y_latex:
                st.latex(st.session_state.goi_y_latex)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("👈 Chọn bài học và nhấn nút 'Tạo câu hỏi mới'.")

# Footer
st.markdown("---")
st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư - Bản Mường.")
