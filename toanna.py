import streamlit as st
import random
import math
import time
import os
import pandas as pd
import io
import base64
import re
from deep_translator import GoogleTranslator
from gtts import gTTS
from PIL import Image # Thư viện xử lý ảnh cho phần Chấm bài

# --- CẤU HÌNH TRANG WEB (CHẠY 1 LẦN DUY NHẤT) ---
st.set_page_config(
    page_title="Cổng Giáo Dục Số - Trường Na Ư",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- KHỞI TẠO SESSION STATE ---
if 'corn_count' not in st.session_state:
    st.session_state.corn_count = 0
if 'user_rank' not in st.session_state:
    st.session_state.user_rank = "Em bé ngoan"
if 'visit_count' not in st.session_state:
    st.session_state.visit_count = 5383

# --- DỮ LIỆU CHƯƠNG TRÌNH HỌC CHI TIẾT (TỪ FILE CỦA BẠN) ---
CHUONG_TRINH_HOC = {
    "Lớp 1": {
        "Chủ đề 1: Các số từ 0 đến 10": ["Đếm số lượng", "So sánh số", "Tách gộp số (Mấy và mấy)"],
        "Chủ đề 2: Phép cộng, trừ phạm vi 10": ["Phép cộng trong phạm vi 10", "Phép trừ trong phạm vi 10"],
        "Chủ đề 3: Hình học đơn giản": ["Nhận biết hình vuông, tròn, tam giác"]
    },
    "Lớp 2": {
        "Chủ đề 1: Phép cộng, trừ (có nhớ)": ["Phép cộng qua 10", "Phép trừ qua 10", "Bài toán nhiều hơn/ít hơn"],
        "Chủ đề 2: Đơn vị đo lường": ["Ki-lô-gam (kg)", "Lít (l)", "Xem ngày giờ"],
        "Chủ đề 3: Hình học": ["Đường thẳng, đoạn thẳng", "Hình tứ giác"]
    },
    "Lớp 3": {
        "Chủ đề 1: Phép nhân và chia": ["Bảng nhân 6, 7, 8, 9", "Bảng chia 6, 7, 8, 9", "Phép chia có dư"],
        "Chủ đề 2: Các số đến 1000": ["Cộng trừ số có 3 chữ số", "Tìm x (Tìm thành phần chưa biết)"],
        "Chủ đề 3: Hình học & Đơn vị": ["Diện tích hình chữ nhật, hình vuông", "Đơn vị đo độ dài (mm, cm, m, km)"]
    },
    "Lớp 4": {
        "Chủ đề 1: Số tự nhiên lớp triệu": ["Đọc viết số lớn", "Làm tròn số"],
        "Chủ đề 2: Bốn phép tính": ["Phép nhân số có 2 chữ số", "Phép chia cho số có 2 chữ số", "Trung bình cộng"],
        "Chủ đề 3: Phân số": ["Rút gọn phân số", "Quy đồng mẫu số", "Cộng trừ phân số"]
    },
    "Lớp 5": {
        "Chủ đề 1: Số thập phân": ["Đọc, viết, so sánh số thập phân", "Chuyển phân số thành số thập phân"],
        "Chủ đề 2: Các phép tính số thập phân": ["Cộng trừ số thập phân", "Nhân chia số thập phân"],
        "Chủ đề 3: Hình học": ["Diện tích hình tam giác", "Chu vi, diện tích hình tròn"]
    },
    "Lớp 6": {
        "Chương 1: Số tự nhiên": ["Lũy thừa", "Thứ tự thực hiện phép tính", "Dấu hiệu chia hết", "Số nguyên tố, Hợp số"],
        "Chương 2: Số nguyên": ["Cộng trừ số nguyên", "Nhân chia số nguyên", "Quy tắc dấu ngoặc"],
        "Chương 3: Hình học trực quan": ["Hình có trục đối xứng", "Hình có tâm đối xứng"]
    },
    "Lớp 7": {
        "Chương 1: Số hữu tỉ": ["Cộng trừ nhân chia số hữu tỉ", "Lũy thừa số hữu tỉ"],
        "Chương 2: Số thực": ["Căn bậc hai số học", "Giá trị tuyệt đối"],
        "Chương 3: Hình học": ["Góc đối đỉnh", "Tổng ba góc trong tam giác", "Các trường hợp bằng nhau của tam giác"]
    },
    "Lớp 8": {
        "Chương 1: Đa thức": ["Cộng trừ đa thức", "Nhân đa thức", "Chia đa thức cho đơn thức"],
        "Chương 2: Hằng đẳng thức": ["Bình phương của tổng/hiệu", "Hiệu hai bình phương"],
        "Chương 3: Phân thức đại số": ["Rút gọn phân thức", "Cộng trừ phân thức"],
        "Chương 4: Hàm số bậc nhất": ["Tính giá trị hàm số", "Hệ số góc"]
    },
    "Lớp 9": {
        "Chương 1: Căn thức": ["Điều kiện xác định của căn", "Rút gọn biểu thức chứa căn"],
        "Chương 2: Hàm số bậc nhất": ["Đồ thị hàm số y=ax+b", "Đường thẳng song song, cắt nhau"],
        "Chương 3: Hệ phương trình": ["Giải hệ phương trình bậc nhất 2 ẩn"],
        "Chương 4: Phương trình bậc hai": ["Công thức nghiệm (Delta)", "Định lý Vi-ét"],
        "Chương 5: Hình học (Đường tròn & Lượng giác)": ["Tỉ số lượng giác", "Góc nội tiếp"]
    }
}

# --- CÁC HÀM XỬ LÝ LOGIC (TỪ CODE CỦA BẠN) ---

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

def update_rank():
    corns = st.session_state.corn_count
    if corns < 5: st.session_state.user_rank = "Em bé ngoan"
    elif corns < 15: st.session_state.user_rank = "Học trò chăm chỉ"
    elif corns < 30: st.session_state.user_rank = "Thợ săn giỏi"
    else: st.session_state.user_rank = "Già làng thông thái"

def tao_de_toan(lop, bai_hoc):
    de_latex = ""
    question_type = "number" 
    dap_an = 0
    options = []
    goi_y_text = ""
    goi_y_latex = ""
    loai_toan = ""
    
    bai_lower = bai_hoc.lower()

    # --- LOGIC SINH ĐỀ CHI TIẾT (GIỮ NGUYÊN TỪ FILE BẠN GỬI) ---
    if "Lớp 1" in lop:
        if "hình" in bai_lower or "nhận biết" in bai_lower:
            question_type = "mcq"
            de_latex = "Hình nào dưới đây có 3 cạnh?"
            dap_an = "Hình tam giác"
            options = ["Hình tam giác", "Hình vuông", "Hình tròn", "Hình chữ nhật"]
            goi_y_text = "Đếm số cạnh của hình. Hình tam giác có 3 cạnh."
            loai_toan = "hinh_hoc_1"
        elif "so sánh" in bai_lower:
            a, b = random.randint(0, 10), random.randint(0, 10)
            while a == b: b = random.randint(0, 10)
            de_latex = f"Điền dấu thích hợp: ${a} \\dots {b}$"
            question_type = "mcq"
            if a > b: dap_an = "Dấu lớn ( > )"
            else: dap_an = "Dấu bé ( < )"
            options = ["Dấu lớn ( > )", "Dấu bé ( < )", "Dấu bằng ( = )"]
            goi_y_text = "Số nào đứng sau trong dãy số thì lớn hơn."
            loai_toan = "so_sanh"
        elif "đếm" in bai_lower or "số lượng" in bai_lower:
            n = random.randint(3, 9)
            items = ["bông hoa", "con gà", "viên bi", "cái kẹo"]
            item = random.choice(items)
            de_latex = f"An có ${n}$ {item}. Hỏi An có mấy {item}?"
            dap_an = n
            goi_y_text = "Đếm số lượng đồ vật."
            loai_toan = "dem_so"
        elif "tách gộp" in bai_lower:
            total = random.randint(4, 10)
            part1 = random.randint(1, total - 1)
            de_latex = f"Gộp ${part1}$ và mấy thì được ${total}$?"
            dap_an = total - part1
            goi_y_text = f"Thực hiện phép trừ: ${total} - {part1}$"
            loai_toan = "tach_gop"
        else:
            a, b = random.randint(1, 5), random.randint(0, 4)
            de_latex = f"Tính: ${a} + {b} = ?$"
            dap_an = a + b
            goi_y_text = "Gộp hai nhóm lại với nhau."
            loai_toan = "cong_don_gian"

    elif "Lớp 2" in lop:
        if "hình" in bai_lower:
            question_type = "mcq"
            de_latex = "Hình tứ giác có bao nhiêu cạnh?"
            dap_an = "4 cạnh"
            options = ["3 cạnh", "4 cạnh", "5 cạnh", "2 cạnh"]
            goi_y_text = "Tứ giác là hình có 4 cạnh."
            loai_toan = "hinh_hoc"
        elif "cộng" in bai_lower:
            a = random.randint(6, 9)
            b = random.randint(5, 9)
            de_latex = f"Tính nhẩm: ${a} + {b} = ?$"
            dap_an = a + b
            goi_y_text = "Gộp cho tròn 10."
            loai_toan = "cong_qua_10"
        else:
            h = random.randint(1, 11)
            de_latex = f"Bây giờ là ${h}$ giờ. 2 giờ nữa là mấy giờ?"
            dap_an = h + 2
            goi_y_text = "Cộng thêm thời gian."
            loai_toan = "thoi_gian"

    elif "Lớp 3" in lop:
        if "nhân" in bai_lower:
            base = random.randint(6, 9)
            mult = random.randint(2, 9)
            de_latex = f"Tính: ${base} \\times {mult} = ?$"
            dap_an = base * mult
            goi_y_text = f"Nhớ lại bảng nhân {base}."
            loai_toan = "phep_nhan"
        elif "chia" in bai_lower:
            b = random.randint(2, 8)
            a = random.randint(10, 50)
            de_latex = f"Tìm số dư trong phép chia: ${a} : {b}$"
            dap_an = a % b
            goi_y_text = "Thực hiện phép chia và lấy phần dư."
            loai_toan = "chia_co_du"
        else:
             a, b = random.randint(5, 20), random.randint(2, 10)
             de_latex = f"Tính diện tích hình chữ nhật: dài ${a}$cm, rộng ${b}$cm."
             dap_an = a * b
             goi_y_text = "Dài nhân Rộng."
             loai_toan = "hinh_hoc"

    elif "Lớp 4" in lop:
        if "trung bình" in bai_lower:
            a, b, c = random.randint(10, 50), random.randint(10, 50), random.randint(10, 50)
            total = a + b + c
            rem = total % 3
            c -= rem
            de_latex = f"Tìm trung bình cộng của: ${a}, {b}, {c}$"
            dap_an = (a + b + c) // 3
            goi_y_text = "Tổng chia cho số các số hạng."
            loai_toan = "trung_binh_cong"
        elif "phân số" in bai_lower:
            tu, mau = random.randint(1, 10), random.randint(2, 10)
            k = random.randint(2, 5)
            tu_k, mau_k = tu * k, mau * k
            de_latex = f"Rút gọn phân số: $\\frac{{{tu_k}}}{{{mau_k}}}$ về tối giản (Nhập tử số)"
            dap_an = tu // math.gcd(tu, mau)
            goi_y_text = "Chia cả tử và mẫu cho ước chung lớn nhất."
            loai_toan = "rut_gon_phan_so"
        else:
             a = random.randint(1000, 9000)
             de_latex = f"Làm tròn số ${a}$ đến hàng trăm:"
             question_type = "mcq"
             res = round(a, -2)
             dap_an = str(res)
             options = [str(res), str(res+100), str(res-100)]
             loai_toan = "lam_tron"

    elif "Lớp 5" in lop:
        if "cộng" in bai_lower:
            a = round(random.uniform(1, 20), 2)
            b = round(random.uniform(1, 20), 2)
            de_latex = f"Tính: ${a} + {b}$"
            dap_an = round(a + b, 2)
            goi_y_text = "Đặt dấu phẩy thẳng cột."
            loai_toan = "cong_so_thap_phan"
        elif "tam giác" in bai_lower:
            a = random.randint(5, 20)
            h = random.randint(5, 20)
            de_latex = f"Diện tích tam giác đáy ${a}$cm, cao ${h}$cm ($cm^2$):"
            dap_an = (a * h) / 2
            goi_y_text = "Đáy nhân cao chia 2."
            goi_y_latex = "S = \\frac{a \\times h}{2}"
            loai_toan = "dien_tich_tam_giac"
        else:
             r = random.randint(1, 10)
             de_latex = f"Chu vi hình tròn r=${r}$cm (lấy $\\pi=3.14$):"
             dap_an = round(r * 2 * 3.14, 2)
             loai_toan = "chu_vi_tron"

    elif "Lớp 6" in lop:
        if "lũy thừa" in bai_lower:
            base = random.randint(2, 5)
            exp = random.randint(2, 4)
            de_latex = f"Giá trị của ${base}^{exp}$ là?"
            dap_an = base ** exp
            goi_y_text = "Nhân cơ số với chính nó n lần."
            loai_toan = "luy_thua"
        elif "nguyên tố" in bai_lower:
            primes = [2, 3, 5, 7, 11, 13]
            composites = [4, 6, 8, 9, 10, 12]
            p = random.choice(primes)
            de_latex = f"Số nào là số nguyên tố?"
            question_type = "mcq"
            dap_an = str(p)
            options = [str(p), str(random.choice(composites)), str(random.choice(composites))]
            goi_y_text = "Chỉ có 2 ước là 1 và chính nó."
            loai_toan = "so_nguyen_to"
        else:
             a = random.randint(-10, -1)
             b = random.randint(-10, -1)
             de_latex = f"Tính: ${a} + ({b})$"
             dap_an = a + b
             goi_y_text = "Cộng hai số âm."
             loai_toan = "cong_so_nguyen"

    elif "Lớp 7" in lop:
        if "hữu tỉ" in bai_lower:
            tu = random.randint(1, 5)
            de_latex = f"Tính: $\\frac{{{tu}}}{{2}} + \\frac{{{tu}}}{{2}}$"
            dap_an = tu
            goi_y_text = "Cộng tử giữ nguyên mẫu."
            loai_toan = "cong_phan_so"
        elif "góc" in bai_lower:
            angle = random.randint(30, 150)
            de_latex = f"Góc đối đỉnh với góc ${angle}^\\circ$ bằng?"
            dap_an = angle
            goi_y_text = "Góc đối đỉnh thì bằng nhau."
            loai_toan = "goc_doi_dinh"
        else:
             sq = random.choice([4, 9, 16, 25])
             de_latex = f"Tính $\\sqrt{{{sq}}}$"
             dap_an = int(math.sqrt(sq))
             loai_toan = "can_bac_hai"

    elif "Lớp 8" in lop:
        question_type = "mcq"
        if "đa thức" in bai_lower:
            a = random.randint(2, 5)
            de_latex = f"Rút gọn: $x(x + {a}) - x^2$"
            ans_correct = f"${a}x$"
            dap_an = ans_correct
            options = [f"${a}x$", f"$-{a}x$", f"$2x^2$"]
            goi_y_text = "Nhân đơn thức rồi trừ."
            goi_y_latex = f"x^2 + {a}x - x^2 = {a}x"
            loai_toan = "rut_gon_da_thuc"
        elif "hằng đẳng thức" in bai_lower:
            a = random.randint(1, 5)
            de_latex = f"Khai triển: $(x - {a})^2$"
            ans_correct = f"$x^2 - {2*a}x + {a**2}$"
            dap_an = ans_correct
            options = [ans_correct, f"$x^2 + {2*a}x + {a**2}$", f"$x^2 - {a**2}$"]
            goi_y_text = "Bình phương một hiệu."
            goi_y_latex = "(A-B)^2 = A^2 - 2AB + B^2"
            loai_toan = "hang_dang_thuc"
        else:
             a = random.randint(2, 5)
             b = random.randint(1, 9)
             de_latex = f"Tính giá trị $y = {a}x + {b}$ tại $x=1$"
             dap_an = f"{a+b}"
             options = [f"{a+b}", f"{a-b}", f"{b}"]
             loai_toan = "gia_tri_ham_so"

    elif "Lớp 9" in lop:
        question_type = "mcq"
        if "căn thức" in bai_lower:
            a = random.randint(2, 5)
            de_latex = f"Điều kiện của $\\sqrt{{x - {a}}}$"
            ans_correct = f"$x \\ge {a}$"
            dap_an = ans_correct
            options = [ans_correct, f"$x < {a}$", f"$x \\le {a}$"]
            goi_y_text = "Biểu thức trong căn không âm."
            loai_toan = "dk_can_thuc"
        elif "hệ phương trình" in bai_lower:
            x = random.randint(1, 3)
            y = random.randint(1, 3)
            c1 = x + y
            c2 = x - y
            de_latex = f"Nghiệm hệ: $\\begin{{cases}} x+y={c1} \\\\ x-y={c2} \\end{{cases}}$"
            ans_correct = f"$({x}; {y})$"
            dap_an = ans_correct
            options = [ans_correct, f"$({y}; {x})$", f"$({x}; -{y})$"]
            goi_y_text = "Cộng đại số."
            loai_toan = "he_phuong_trinh"
        else:
             x1, x2 = 2, 3
             S = x1 + x2
             P = x1 * x2
             de_latex = f"Tổng 2 nghiệm của $x^2 - {S}x + {P} = 0$"
             ans_correct = f"{S}"
             dap_an = ans_correct
             options = [f"{S}", f"-{S}", f"{P}"]
             goi_y_text = "Định lý Vi-ét: $x_1+x_2 = -b/a$"
             loai_toan = "vi_et"

    else:
        a, b = random.randint(1, 20), random.randint(1, 20)
        de_latex = f"Tính: ${a} + {b} = ?$"
        dap_an = a + b
        loai_toan = "cong_co_ban"

    if question_type == "mcq" and options: random.shuffle(options)
              
    return de_latex, question_type, dap_an, options, goi_y_text, goi_y_latex, loai_toan

def phan_tich_loi_sai(user_ans, true_ans, q_type):
    hint_msg = "Chưa đúng rồi! (Tsis yog lawm)"
    if q_type == "number" and isinstance(true_ans, (int, float)):
        try:
            diff = abs(user_ans - true_ans)
            if diff == 0: return "Tuyệt vời!"
            if user_ans == -true_ans:
                hint_msg = "Bạn bị nhầm dấu rồi! (Tsis yog, saib dua)"
            elif diff <= 2:
                hint_msg = "Gần đúng rồi! Tính lại cẩn thận nhé."
        except: pass
    return hint_msg

def dich_sang_mong_giu_cong_thuc(text):
    parts = re.split(r'(\$.*?\$)', text)
    translated_parts = []
    for part in parts:
        if part.startswith('$') and part.endswith('$'):
            translated_parts.append(part)
        else:
            if part.strip():
                try:
                    trans = GoogleTranslator(source='vi', target='hmn').translate(part)
                    translated_parts.append(trans)
                except:
                    translated_parts.append(part)
            else:
                translated_parts.append(part)
    return "".join(translated_parts)

def text_to_speech_html(text, lang='vi'):
    clean_text = text.replace("$", "")
    clean_text = re.sub(r'\\frac\{(.+?)\}\{(.+?)\}', r'\1 phần \2', clean_text)
    clean_text = re.sub(r'(\w)\^2', r'\1 bình phương ', clean_text)
    clean_text = re.sub(r'(\w)\^3', r'\1 lập phương ', clean_text)
    clean_text = re.sub(r'(\w)\^(\d+)', r'\1 mũ \2 ', clean_text)
    
    vars_math = ["xy", "xyz", "ab", "abc"]
    for v in vars_math:
        if v in clean_text:
            spaced_v = " ".join(list(v))
            clean_text = clean_text.replace(v, spaced_v)

    replacements = {
        "\\begin{cases}": "hệ phương trình ", "\\end{cases}": "", "\\\\": " và ",
        "\\times": " nhân ", "\\cdot": " nhân ", ":": " chia ", "+": " cộng ",
        "-": " trừ ", "\\le": " nhỏ hơn hoặc bằng ", "\\ge": " lớn hơn hoặc bằng ",
        "\\neq": " khác ", "\\approx": " xấp xỉ ", "\\circ": " độ ", "\\hat": " góc ",
        "\\sqrt": " căn bậc hai của ", "\\pm": " cộng trừ ", "\\pi": " pi ",
        ">": " lớn hơn ", "<": " nhỏ hơn ", "=": " bằng "
    }
    for k, v in replacements.items():
        clean_text = clean_text.replace(k, v)
    clean_text = clean_text.replace("{", "").replace("}", "")

    tts = gTTS(text=clean_text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    md = f"""<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>"""
    return md

# --- CSS (TỔNG HỢP) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    .stApp { background-color: #f0f4f8; background-image: radial-gradient(#dde1e7 1px, transparent 1px); background-size: 20px 20px; }
    
    /* STYLE CHO GIA SƯ TOÁN (TỪ FILE CŨ) */
    .hmong-header-container {
        background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        overflow: hidden; margin-bottom: 30px; border: 2px solid #e0e0e0;
    }
    .hmong-top-bar {
        background: linear-gradient(90deg, #1a237e, #3949ab); color: white; padding: 10px 20px;
        text-align: center; text-transform: uppercase;
    }
    .hmong-main-title { padding: 30px 20px; text-align: center; background: white; }
    .hmong-main-title h1 { color: #d32f2f; font-size: 2.5rem; font-weight: 900; margin: 0; text-shadow: 2px 2px 0px #ffcdd2; }
    .hmong-pattern {
        height: 12px;
        background: repeating-linear-gradient(45deg, #d32f2f, #d32f2f 15px, #ffeb3b 15px, #ffeb3b 30px, #388e3c 30px, #388e3c 45px, #1976d2 45px, #1976d2 60px);
        width: 100%;
    }
    .problem-box {
        background-color: white; padding: 30px; border-radius: 20px;
        border: 2px solid #e0e0e0; border-top: 8px solid #1a237e;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px;
    }
    
    /* STYLE CHO TRANG CHỦ & MENU */
    .main-header {
        background: linear-gradient(90deg, #1a237e, #3949ab);
        color: white; padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .feature-card {
        background: white; padding: 20px; border-radius: 15px;
        border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center; transition: transform 0.3s;
    }
    .feature-card:hover { transform: translateY(-5px); border-color: #1a237e; }
    
    .stButton>button {
        background: linear-gradient(to right, #d32f2f, #b71c1c); color: white; border-radius: 30px;
        font-weight: bold; border: none; box-shadow: 0 4px 6px rgba(211, 47, 47, 0.3);
    }
    .stButton>button:hover { transform: scale(1.05); color: white; }
    
    /* GAMIFICATION */
    .score-card {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border: 2px solid #ffb74d; border-radius: 15px; padding: 15px;
        text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .rank-title { color: #e65100; font-weight: bold; font-size: 1.2rem; text-transform: uppercase; }
    .corn-icon { font-size: 2rem; }

    /* AI TUTOR & HINT */
    .ai-tutor-box { background-color: #e3f2fd; border-left: 5px solid #2196f3; padding: 20px; border-radius: 10px; margin-top: 15px; }
    .hint-container { background-color: #e8f5e9; border-left: 5px solid #4caf50; padding: 15px; border-radius: 8px; margin-top: 20px; color: #1b5e20; }
    .hmong-hint { background-color: #fce4ec; border-left: 5px solid #e91e63; padding: 15px; border-radius: 8px; margin-top: 10px; font-style: italic; color: #880e4f; }
    .error-box { background-color: #ffebee; border: 1px solid #ef9a9a; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px; color: #c62828; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- TRANG 1: TRANG CHỦ ---
def page_home():
    st.markdown("""
    <div class="main-header">
        <h1>🏫 TRƯỜNG PTDTBT TH&THCS NA Ư</h1>
        <h3>CỔNG THÔNG TIN GIÁO DỤC SỐ - BẢN MƯỜNG</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h1>🏔️</h1>
            <h3>Gia Sư Toán AI</h3>
            <p>Luyện tập từng bài, nhận ngô, đổi quà. Hỗ trợ tiếng Mông.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h1>📝</h1>
            <h3>Sinh Đề Tự Động</h3>
            <p>Tạo phiếu bài tập ôn luyện, đề kiểm tra 15 phút, 1 tiết chỉ trong 1 giây.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h1>📸</h1>
            <h3>Chấm Bài AI Vision</h3>
            <p>Chụp ảnh bài làm trong vở, AI sẽ chấm điểm và chỉ ra lỗi sai.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info(f"📊 Thống kê: Đã có **{st.session_state.visit_count}** lượt truy cập vào hệ thống.")

# --- TRANG 2: GIA SƯ TOÁN (TÍCH HỢP CODE TỪ FILE UPLOAD) ---
def page_tutor():
    # Header phong cách H'Mông
    st.markdown(f"""
    <div class="hmong-header-container">
        <div class="hmong-top-bar">GIA SƯ TOÁN HỌC</div>
        <div class="hmong-main-title">
            <h1>LUYỆN TẬP TOÁN AI</h1>
            <div class="visit-counter">Lượt truy cập: {st.session_state.visit_count}</div>
        </div>
        <div class="hmong-pattern"></div>
    </div>
    """, unsafe_allow_html=True)

    # Khởi tạo state cho Gia sư nếu chưa có
    if 'de_bai' not in st.session_state:
        st.session_state.de_bai = ""
        st.session_state.q_type = "number"
        st.session_state.dap_an = 0
        st.session_state.options = []
        st.session_state.goi_y_text = ""
        st.session_state.goi_y_latex = ""
        st.session_state.loai_toan = ""
        st.session_state.show_hint = False
        st.session_state.submitted = False
        st.session_state.show_ai_tutor = False

    def click_sinh_de(lop, bai):
        db, qt, da, ops, gyt, gyl, lt = tao_de_toan(lop, bai)
        st.session_state.de_bai = db
        st.session_state.q_type = qt
        st.session_state.dap_an = da
        st.session_state.options = ops
        st.session_state.goi_y_text = gyt
        st.session_state.goi_y_latex = gyl
        st.session_state.loai_toan = lt
        st.session_state.show_hint = False
        st.session_state.submitted = False
        st.session_state.show_ai_tutor = False

    def ai_giai_thich_chi_tiet(loai_toan, de_bai, dap_an):
        explanation = "### 🤖 Gia sư AI giải thích chi tiết:\n"
        # (Logic giải thích đơn giản hóa để tiết kiệm dòng code, bạn có thể thêm chi tiết như file cũ)
        if loai_toan == "so_sanh": explanation += "- Hãy đếm và so sánh hai số.\n- Miệng cá sấu luôn quay về phía số lớn hơn."
        elif loai_toan == "hinh_hoc_1": explanation += "- Quan sát kỹ số cạnh và hình dáng.\n- Tam giác có 3 cạnh."
        elif loai_toan == "cong_co_ban": explanation += "- Đây là phép cộng cơ bản. Hãy dùng que tính để đếm nhé."
        elif loai_toan == "cong_qua_10": explanation += "- Tách số hạng thứ hai để cộng với số đầu cho tròn 10."
        elif loai_toan == "phep_nhan": explanation += "- Phép nhân là cách viết gọn của phép cộng nhiều số giống nhau."
        elif loai_toan == "rut_gon_phan_so": explanation += "- Chia cả tử và mẫu cho ước chung lớn nhất."
        elif loai_toan == "he_phuong_trinh": explanation += "- Cộng hoặc trừ hai phương trình để triệt tiêu một ẩn."
        else: explanation += f"- Đáp án đúng là: **{dap_an}**. Hãy kiểm tra lại các bước tính toán."
        return explanation

    # Layout chính của trang Gia sư
    col_trai, col_phai = st.columns([1.6, 1])

    with col_trai:
        # Bộ chọn bài học (Đặt ở đây cho dễ thao tác)
        st.subheader("📚 CHỌN BÀI HỌC")
        c1, c2, c3 = st.columns(3)
        with c1: lop_chon = st.selectbox("Lớp:", list(CHUONG_TRINH_HOC.keys()))
        with c2: chuong_chon = st.selectbox("Chương:", list(CHUONG_TRINH_HOC[lop_chon].keys()))
        with c3: bai_chon = st.selectbox("Bài:", CHUONG_TRINH_HOC[lop_chon][chuong_chon])

        if st.button("✨ TẠO CÂU HỎI MỚI (AI Generated)", type="primary"):
            click_sinh_de(lop_chon, bai_chon)

        # Hiển thị câu hỏi
        if st.session_state.de_bai:
            st.markdown('<div class="problem-box">', unsafe_allow_html=True)
            st.markdown("### ❓ Câu hỏi:")
            st.markdown(f"## {st.session_state.de_bai}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("### 🤖 Công cụ hỗ trợ AI:")
            col_tool1, col_tool2 = st.columns(2)
            with col_tool1:
                if st.button("🗣️ Đọc đề (Giọng AI)"):
                    audio_html = text_to_speech_html(st.session_state.de_bai)
                    st.markdown(audio_html, unsafe_allow_html=True)
            with col_tool2:
                if st.button("🌏 Dịch H'Mông"):
                    bd = dich_sang_mong_giu_cong_thuc(st.session_state.de_bai)
                    st.info(f"**H'Mông:** {bd}")

            if st.session_state.show_ai_tutor:
                st.markdown('<div class="ai-tutor-box">', unsafe_allow_html=True)
                explanation = ai_giai_thich_chi_tiet(st.session_state.loai_toan, st.session_state.de_bai, st.session_state.dap_an)
                st.markdown(explanation)
                st.markdown('</div>', unsafe_allow_html=True)

    with col_phai:
        st.subheader("✍️ Làm bài")
        
        # Thẻ điểm Gamification
        st.markdown('<div class="score-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="rank-title">🎖️ {st.session_state.user_rank}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="corn-icon">🌽 x {st.session_state.corn_count}</div>', unsafe_allow_html=True)
        st.caption("Thu thập ngô để thăng cấp!")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.de_bai:
            with st.form("form_lam_bai"):
                user_ans = None
                if st.session_state.q_type == "mcq":
                    st.markdown("**Chọn đáp án đúng:**")
                    if st.session_state.options: 
                        user_ans = st.radio("Đáp án:", st.session_state.options, label_visibility="collapsed")
                else:
                    if isinstance(st.session_state.dap_an, int) or (isinstance(st.session_state.dap_an, float) and st.session_state.dap_an.is_integer()):
                        user_ans = st.number_input("Nhập đáp án (Số nguyên):", step=1, format="%d")
                    else:
                        user_ans = st.number_input("Nhập đáp án:", step=0.01, format="%.2f")

                btn_nop = st.form_submit_button("✅ Kiểm tra")
                
                if btn_nop and user_ans is not None:
                    st.session_state.submitted = True
                    is_correct = False
                    if st.session_state.q_type == "mcq":
                        if user_ans == st.session_state.dap_an: is_correct = True
                    else:
                        if isinstance(st.session_state.dap_an, str):
                            if str(user_ans) == st.session_state.dap_an: is_correct = True
                        else:
                            if abs(user_ans - float(st.session_state.dap_an)) <= 0.05: is_correct = True

                    if is_correct:
                        st.session_state.corn_count += 1
                        update_rank()
                        st.balloons()
                        st.success(f"CHÍNH XÁC! Bạn nhận được 1 bắp ngô! 🌽")
                        st.session_state.show_hint = False
                        st.session_state.show_ai_tutor = False
                    else:
                        adaptive_msg = phan_tich_loi_sai(user_ans, st.session_state.dap_an, st.session_state.q_type)
                        st.markdown(f'<div class="error-box">{adaptive_msg}</div>', unsafe_allow_html=True)
                        st.session_state.show_hint = True
            
            if st.session_state.show_hint:
                if st.button("🤖 Nhờ Gia sư AI giảng bài chi tiết"):
                    st.session_state.show_ai_tutor = True
                
                st.markdown("---")
                st.markdown('<div class="hint-container">', unsafe_allow_html=True)
                st.markdown(f"**💡 Gợi ý nhanh:** {st.session_state.goi_y_text}")
                if st.session_state.goi_y_latex: st.latex(st.session_state.goi_y_latex)
                st.markdown('</div>', unsafe_allow_html=True)
                
                translation = dich_sang_mong_giu_cong_thuc(st.session_state.goi_y_text)
                st.markdown('<div class="hmong-hint">', unsafe_allow_html=True)
                st.markdown(f"**🗣️ H'Mông:** {translation}")
                if st.session_state.goi_y_latex: st.latex(st.session_state.goi_y_latex)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("👈 Chọn bài học và nhấn nút 'Tạo câu hỏi mới'.")

# --- TRANG 3: SINH ĐỀ TỰ ĐỘNG ---
def page_generator():
    st.title("📝 Tự Động Sinh Đề Kiểm Tra")
    st.write("Tạo phiếu bài tập để in ấn hoặc ôn luyện offline.")
    
    c1, c2, c3 = st.columns(3)
    with c1: lop = st.selectbox("Lớp", list(CHUONG_TRINH_HOC.keys()), key="gen_lop")
    with c2: chuong = st.selectbox("Chủ đề", list(CHUONG_TRINH_HOC[lop].keys()), key="gen_chuong")
    with c3: so_cau = st.slider("Số lượng câu hỏi", 5, 20, 10)
    
    if st.button("🚀 Sinh đề ngay"):
        de_thi_text = f"TRƯỜNG PTDTBT TH&THCS NA Ư\nĐỀ ÔN TẬP TOÁN {lop.upper()}\nChủ đề: {chuong}\n"
        de_thi_text += "="*40 + "\n\n"
        
        bai_list = CHUONG_TRINH_HOC[lop][chuong]
        list_qa = []
        for i in range(so_cau):
            bai = random.choice(bai_list)
            db, qt, da, ops, gyt, _, _ = tao_de_toan(lop, bai)
            cau_hoi = f"Câu {i+1}: {db}\n"
            if qt == 'mcq': cau_hoi += "\n".join([f"   [ ] {opt}" for opt in ops]) + "\n"
            else: cau_hoi += "   Trả lời: ........................\n"
            de_thi_text += cau_hoi + "\n"
            list_qa.append((cau_hoi, da))
            
        st.text_area("Xem trước đề thi:", value=de_thi_text, height=400)
        st.download_button(label="📥 Tải phiếu bài tập (TXT)", data=de_thi_text, file_name=f"De_Toan_{lop}.txt", mime="text/plain")
        with st.expander("Xem đáp án (Dành cho Giáo viên)"):
            for i, (q, a) in enumerate(list_qa): st.write(f"**Câu {i+1}:** {a}")

# --- TRANG 4: CHẤM BÀI QUA ẢNH ---
def page_vision():
    st.title("📸 Chấm Bài & Giải Toán Qua Ảnh")
    st.write("Học sinh chụp ảnh bài làm hoặc đề bài trong sách, AI sẽ nhận xét và hướng dẫn.")
    
    uploaded_file = st.file_uploader("Tải ảnh lên (PNG, JPG)", type=["png", "jpg", "jpeg"])
    col_img, col_result = st.columns(2)
    
    if uploaded_file is not None:
        with col_img:
            image = Image.open(uploaded_file)
            st.image(image, caption="Ảnh bài làm", use_column_width=True)
        with col_result:
            st.subheader("🤖 AI Nhận xét:")
            if st.button("🔍 Phân tích ngay"):
                with st.spinner("Đang đọc chữ viết tay và phân tích lỗi sai..."):
                    time.sleep(2) 
                    st.success("Đã phân tích xong!")
                    st.markdown("""
                    **Kết quả nhận diện (Demo):**
                    - Bài toán: $2x + 5 = 15$
                    - Bài làm: $2x = 20 \Rightarrow x = 10$
                    **❌ Lỗi sai:** Cộng 5 vào 15 thay vì trừ 5.
                    **✅ Đáp án đúng:** $x = 5$
                    **💡 Lời khuyên:** Nhớ đổi dấu khi chuyển vế nhé!
                    """)
                    st.info("Tiếng Mông: Thaum hloov sab, nco ntsoov hloov cim!")

# --- ĐIỀU HƯỚNG CHÍNH (SIDEBAR MENU) ---
with st.sidebar:
    st.markdown("<div style='text-align: center; font-size: 60px;'>🏔️</div>", unsafe_allow_html=True)
    st.markdown("### MENU CHỨC NĂNG")
    
    page = st.radio(
        "Chọn trang:", 
        ["Trang chủ", "Gia sư Toán AI", "Sinh đề tự động", "Chấm bài qua ảnh"],
        index=0
    )
    
    st.markdown("---")
    if page != "Trang chủ":
        st.write(f"🌽 Ngô của bạn: **{st.session_state.corn_count}**")

# --- ROUTING ---
if page == "Trang chủ": page_home()
elif page == "Gia sư Toán AI": page_tutor()
elif page == "Sinh đề tự động": page_generator()
elif page == "Chấm bài qua ảnh": page_vision()

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>© 2025 Hệ sinh thái Giáo dục Na Ư - Phát triển bởi Gia sư AI</div>", unsafe_allow_html=True)
