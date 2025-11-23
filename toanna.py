import streamlit as st
import random
import math
from deep_translator import GoogleTranslator

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gia sư Toán AI - KNTT (Lớp 1-9)",
    page_icon="📐",
    layout="wide"
)

# --- DỮ LIỆU CHƯƠNG TRÌNH HỌC (SÁCH KẾT NỐI TRI THỨC) ---
CHUONG_TRINH_HOC = {
    "Lớp 1": {
        "Chương 1: Các số từ 0 đến 10": ["Các số 0, 1, 2, 3, 4, 5", "Các số 6, 7, 8, 9, 10", "Nhiều hơn, ít hơn, bằng nhau", "So sánh số"],
        "Chương 2: Làm quen với một số hình phẳng": ["Ôn tập hình vuông, tròn, tam giác"], 
        "Chương 3: Phép cộng, trừ trong phạm vi 10": ["Phép cộng trong phạm vi 10", "Phép trừ trong phạm vi 10", "Bảng cộng, bảng trừ"],
        "Chương 4: Các số trong phạm vi 100": ["Các số có hai chữ số", "So sánh số có hai chữ số", "Phép cộng (không nhớ) trong phạm vi 100", "Phép trừ (không nhớ) trong phạm vi 100"]
    },
    "Lớp 2": {
        "Chương 1: Ôn tập và bổ sung": ["Ôn tập các số đến 100", "Số hạng - Tổng", "Số bị trừ - Hiệu"],
        "Chương 2: Phép cộng, trừ qua 10": ["Phép cộng qua 10 trong phạm vi 20", "Phép trừ qua 10 trong phạm vi 20", "Bài toán về nhiều hơn, ít hơn"],
        "Chương 3: Làm quen với khối lượng, dung tích": ["Ki-lô-gam", "Lít"],
        "Chương 4: Phép nhân, Phép chia": ["Làm quen với phép nhân", "Bảng nhân 2, 5", "Làm quen với phép chia", "Bảng chia 2, 5"],
        "Chương 5: Các số đến 1000": ["Các số tròn trăm", "Phép cộng, trừ trong phạm vi 1000"]
    },
    "Lớp 3": {
        "Chương 1: Phép nhân và chia trong phạm vi 1000": ["Bảng nhân 3, 4, 6, 7, 8, 9", "Bảng chia 3, 4, 6, 7, 8, 9", "Tìm thành phần chưa biết"],
        "Chương 2: Một số hình phẳng": ["Chu vi hình chữ nhật, hình vuông"], 
        "Chương 3: Các số đến 10 000": ["Các số có 4 chữ số", "Phép cộng, trừ các số trong phạm vi 10 000"],
        "Chương 4: Diện tích": ["Diện tích hình chữ nhật", "Diện tích hình vuông"]
    },
    "Lớp 4": {
        "Chương 1: Số tự nhiên": ["Các số có nhiều chữ số", "So sánh số", "Làm tròn số"],
        "Chương 2: Bốn phép tính số tự nhiên": ["Phép cộng, phép trừ", "Phép nhân, phép chia", "Tính chất giao hoán, kết hợp", "Trung bình cộng"],
        "Chương 3: Hình học và Đo lường": ["Đổi đơn vị đo"], 
        "Chương 4: Phân số": ["Khái niệm phân số", "Quy đồng mẫu số", "Cộng, trừ, nhân, chia phân số"]
    },
    "Lớp 5": {
        "Chương 1: Ôn tập phân số": ["Hỗn số", "Ôn tập phép tính phân số"],
        "Chương 2: Số thập phân": ["Khái niệm số thập phân", "So sánh số thập phân", "Cộng, trừ, nhân, chia số thập phân"],
        "Chương 3: Hình học": ["Chu vi, Diện tích"], 
        "Chương 4: Số đo thời gian, Vận tốc": ["Cộng trừ số đo thời gian", "Vận tốc, Quãng đường, Thời gian"]
    },
    "Lớp 6": {
        "Chương 1: Tập hợp số tự nhiên": ["Tập hợp", "Phép tính lũy thừa", "Thứ tự thực hiện phép tính", "Dấu hiệu chia hết"],
        "Chương 2: Số nguyên": ["Tập hợp số nguyên", "Phép cộng, trừ số nguyên", "Phép nhân, chia số nguyên"],
        "Chương 3: Phân số và Số thập phân": ["Mở rộng phân số", "Các phép tính phân số/số thập phân"]
    },
    "Lớp 7": {
        "Chương 1: Số hữu tỉ": ["Cộng, trừ, nhân, chia số hữu tỉ", "Lũy thừa của số hữu tỉ"],
        "Chương 2: Số thực": ["Căn bậc hai số học", "Làm tròn số", "Số vô tỉ"],
        "Chương 3: Biểu thức đại số": ["Đơn thức, Đa thức một biến", "Phép cộng trừ đa thức"]
    },
    "Lớp 8": {
        "Chương 1: Đa thức": ["Đơn thức, Đa thức nhiều biến", "Hằng đẳng thức đáng nhớ", "Phân tích đa thức thành nhân tử"],
        "Chương 2: Hàm số và Đồ thị": ["Hàm số bậc nhất", "Đồ thị hàm số bậc nhất"],
        "Chương 3: Phân thức đại số": ["Rút gọn phân thức", "Cộng trừ phân thức"]
    },
    "Lớp 9": {
        "Chương 1: Hệ phương trình": ["Phương trình bậc nhất hai ẩn", "Hệ hai phương trình bậc nhất hai ẩn"],
        "Chương 2: Phương trình bậc hai": ["Phương trình quy về bậc nhất", "Phương trình bậc hai một ẩn", "Hệ thức Viète"],
        "Chương 3: Căn thức": ["Căn bậc hai", "Căn bậc ba", "Biến đổi căn thức"]
    }
}

# --- CSS LÀM ĐẸP GIAO DIỆN ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(to right, #f8f9fa, #e9ecef); }
    .school-header {
        background: linear-gradient(135deg, #0d47a1, #1976d2);
        color: white; padding: 25px; border-radius: 15px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin-bottom: 25px;
    }
    .problem-card {
        background-color: white; padding: 30px; border-radius: 15px;
        border-left: 8px solid #ff9800; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        font-size: 1.3rem; margin-bottom: 20px;
        color: #333;
    }
    .hint-box {
        background-color: #e3f2fd; padding: 15px; border-radius: 10px;
        border: 1px dashed #2196f3; margin-top: 10px;
    }
    .success-msg { color: #2e7d32; font-weight: 700; font-size: 1.2rem; }
    .error-msg { color: #c62828; font-weight: 700; }
    .stButton>button { border-radius: 25px; font-weight: 600; padding: 0.5rem 1rem; }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def format_bieu_thuc(so, truoc_co_so=True):
    """
    Hàm định dạng hiển thị số âm/dương gọn gàng.
    Ví dụ: thay vì '+ -5', trả về '- 5'.
    """
    if so < 0:
        return f"- {abs(so)}"
    else:
        if truoc_co_so:
            return f"+ {so}"
        return f"{so}"

def sinh_so_ngau_nhien(lop):
    """Hàm phụ trợ sinh số phù hợp cấp độ"""
    if "Lớp 1" in lop: return random.randint(1, 10), random.randint(1, 10)
    if "Lớp 2" in lop: return random.randint(10, 90), random.randint(1, 20)
    if "Lớp 3" in lop: return random.randint(100, 900), random.randint(2, 9)
    if "Lớp 4" in lop or "Lớp 5" in lop: return random.randint(1000, 9000), random.randint(10, 99)
    # Lớp 6-9: Có thể có số âm
    if "Lớp 6" in lop: return random.randint(-50, 50), random.randint(-20, 20)
    return random.randint(-100, 100), random.randint(-100, 100)

def tao_de_toan(lop, bai_hoc):
    """
    Hàm Factory sinh đề dựa trên từ khóa trong Tên Bài Học.
    Cập nhật: Tạo gợi ý chi tiết kèm công thức Toán học (LaTeX).
    """
    bai_hoc_lower = bai_hoc.lower()
    de_bai, dap_an, goi_y = "", 0, ""

    # --- 1. SỐ HỌC CƠ BẢN ---
    if any(x in bai_hoc_lower for x in ["cộng", "tổng", "thêm"]):
        a, b = sinh_so_ngau_nhien(lop)
        if b < 0:
            de_bai = f"Tính: {a} - {abs(b)} = ?"
            goi_y = f"Đây là phép cộng số nguyên. Em hãy thực hiện: ${a} - {abs(b)}$"
        else:
            de_bai = f"Tính: {a} + {b} = ?"
            goi_y = f"Đặt tính rồi tính: Lấy hàng đơn vị cộng hàng đơn vị, hàng chục cộng hàng chục.\\nVí dụ: ${a} + {b} = ...$"
        dap_an = a + b
        
    elif any(x in bai_hoc_lower for x in ["trừ", "hiệu", "bớt", "ít hơn"]):
        a, b = sinh_so_ngau_nhien(lop)
        if "Lớp 6" not in lop and "Lớp 7" not in lop and "Lớp 8" not in lop and "Lớp 9" not in lop:
            a, b = max(a, b), min(a, b)
        
        if b < 0: 
            de_bai = f"Tính: {a} - ({b}) = ?"
            goi_y = f"Trừ cho một số âm là cộng với số đối của nó: ${a} - ({b}) = {a} + {abs(b)}$"
        else:
            de_bai = f"Tính: {a} - {b} = ?"
            goi_y = f"Đặt tính rồi tính: Lấy hàng đơn vị trừ hàng đơn vị. Nếu không đủ thì mượn 1 ở hàng chục.\\n${a} - {b} = ...$"
        dap_an = a - b
        
    elif any(x in bai_hoc_lower for x in ["nhân", "tích", "gấp"]):
        if "Lớp 2" in lop: a, b = random.randint(2, 5), random.randint(1, 10)
        elif "Lớp 3" in lop: a, b = random.randint(2, 9), random.randint(2, 9)
        else: a, b = sinh_so_ngau_nhien(lop)
        
        if b < 0:
            de_bai = f"Tính: {a} x ({b}) = ?"
        else:
            de_bai = f"Tính: {a} x {b} = ?"
        dap_an = a * b
        goi_y = f"Em hãy nhớ lại bảng cửu chương hoặc thực hiện phép nhân:\\n${a} \\times {b} = ?$"

    elif any(x in bai_hoc_lower for x in ["chia", "thương"]):
        if "Lớp 2" in lop: b = random.choice([2, 5])
        elif "Lớp 3" in lop: b = random.randint(2, 9)
        else: b = random.randint(2, 20)
        if b == 0: b = 2
        kq = random.randint(2, 10)
        a = b * kq
        de_bai = f"Tính: {a} : {b} = ?"
        dap_an = kq
        goi_y = f"Đặt tính chia: Số nào nhân với ${b}$ thì bằng ${a}$?\\n$\\frac{{{a}}}{{{b}}} = ?$"

    # --- 2. SO SÁNH ---
    elif "so sánh" in bai_hoc_lower:
        a, b = sinh_so_ngau_nhien(lop)
        while a == b: b = sinh_so_ngau_nhien(lop)[1]
        de_bai = f"Điền dấu (1 là >, 2 là <): {a} ... {b} (Nhập 1 nếu lớn hơn, 2 nếu nhỏ hơn)"
        dap_an = 1 if a > b else 2
        goi_y = f"So sánh từ hàng cao nhất (bên trái) sang hàng thấp nhất (bên phải).\\n${a}$ so với ${b}$ thế nào?"

    # --- 3. HÌNH HỌC ---
    elif "vuông" in bai_hoc_lower and ("chu vi" in bai_hoc_lower or "diện tích" in bai_hoc_lower):
        canh = random.randint(2, 20)
        if "chu vi" in bai_hoc_lower:
            de_bai = f"Hình vuông cạnh {canh}cm. Tính Chu vi (cm)?"
            dap_an = canh * 4
            goi_y = f"Công thức Chu vi hình vuông cạnh $a$: $P = a \\times 4$.\\nÁp dụng: $P = {canh} \\times 4$"
        else:
            de_bai = f"Hình vuông cạnh {canh}cm. Tính Diện tích (cm²)?"
            dap_an = canh * canh
            goi_y = f"Công thức Diện tích hình vuông cạnh $a$: $S = a \\times a$ (hoặc $a^2$).\\nÁp dụng: $S = {canh} \\times {canh}$"
            
    elif "chữ nhật" in bai_hoc_lower and ("chu vi" in bai_hoc_lower or "diện tích" in bai_hoc_lower):
        d = random.randint(5, 20)
        r = random.randint(1, d-1)
        if "chu vi" in bai_hoc_lower:
            de_bai = f"HCN có dài {d}cm, rộng {r}cm. Tính Chu vi (cm)?"
            dap_an = (d + r) * 2
            goi_y = f"Công thức Chu vi HCN: $P = (dài + rộng) \\times 2$.\\nÁp dụng: $P = ({d} + {r}) \\times 2$"
        else:
            de_bai = f"HCN có dài {d}cm, rộng {r}cm. Tính Diện tích (cm²)?"
            dap_an = d * r
            goi_y = f"Công thức Diện tích HCN: $S = dài \\times rộng$.\\nÁp dụng: $S = {d} \\times {r}$"

    # --- 4. ĐẠI SỐ & GIẢI TÍCH ---
    elif "lũy thừa" in bai_hoc_lower:
        base = random.randint(2, 5)
        exp = random.randint(2, 4)
        de_bai = f"Tính: {base}^{exp} = ?"
        dap_an = base ** exp
        # Gợi ý chi tiết dạng a x a x ...
        expansion = " \\times ".join([str(base)] * exp)
        goi_y = f"Lũy thừa bậc $n$ của $a$ là tích của $n$ thừa số $a$: \\n$${base}^{exp} = {expansion}$$"
        
    elif "làm tròn" in bai_hoc_lower:
        val = random.uniform(10, 100)
        de_bai = f"Làm tròn số {val:.3f} đến chữ số thập phân thứ nhất."
        dap_an = round(val, 1)
        goi_y = f"Quy tắc làm tròn: Nếu chữ số ngay sau hàng làm tròn $\\ge 5$ thì cộng thêm 1, ngược lại giữ nguyên.\\nSố cần xét là chữ số thứ 2 sau dấu phẩy của ${val:.3f}$."
        
    elif "phương trình" in bai_hoc_lower and "hệ" not in bai_hoc_lower:
        # ax + b = 0
        a = random.randint(2, 10)
        b = random.randint(1, 20) * random.choice([-1, 1])
        dau_b = format_bieu_thuc(b)
        
        de_bai = f"Tìm x biết: {a}x {dau_b} = 0 (Làm tròn 2 chữ số thập phân)"
        dap_an = round(-b/a, 2)
        
        # Gợi ý từng bước giải phương trình
        if b < 0:
            buoc1 = f"{a}x = {abs(b)}"
        else:
            buoc1 = f"{a}x = -{b}"
            
        goi_y = f"**Bước 1:** Chuyển hệ số tự do sang vế phải và đổi dấu:\\n$${a}x {dau_b} = 0 \\Rightarrow {buoc1}$$ \\n**Bước 2:** Chia cả hai vế cho ${a}$ để tìm $x$:\\n$$x = \\frac{{{buoc1.split('=')[1].strip()}}}{{{a}}}$$"
        
    elif "hệ phương trình" in bai_hoc_lower:
        x = random.randint(5, 20)
        y = random.randint(1, x)
        S = x + y
        D = x - y
        de_bai = f"Cho hệ: x + y = {S} và x - y = {D}. Tìm giá trị của x?"
        dap_an = x
        goi_y = f"Dùng phương pháp cộng đại số:\\nCộng hai phương trình vế theo vế:\\n$(x + y) + (x - y) = {S} + {D}$ \\n$\\Rightarrow 2x = {S + D} \\Rightarrow x = ?$"
        
    elif "căn" in bai_hoc_lower:
        kq = random.randint(2, 15)
        n = kq**2
        de_bai = f"Tính căn bậc hai số học của {n}?"
        dap_an = kq
        goi_y = f"Căn bậc hai số học của số không âm $a$ là số $x$ sao cho $x^2 = a$.\\nKí hiệu: $\\sqrt{{a}} = x$.\\nỞ đây em cần tìm số nào bình phương lên bằng ${n}$?\\n$$\\sqrt{{{n}}} = ? \\text{{ vì }} ?^2 = {n}$$"

    # --- 5. FALLBACK ---
    else:
        a, b = sinh_so_ngau_nhien(lop)
        de_bai = f"Bài toán ôn tập: Tính {a} + {b}"
        dap_an = a + b
        goi_y = f"Thực hiện phép tính cộng cơ bản: ${a} + {b}$"

    return de_bai, dap_an, goi_y

# Hàm dịch thuật
def dich_sang_mong(text):
    try:
        # Loại bỏ các ký tự LaTeX ($) trước khi dịch để tránh lỗi, hoặc chỉ dịch phần text cơ bản
        # Ở đây ta chỉ dịch đơn giản, Google Translate có thể không hiểu LaTeX
        clean_text = text.replace("$", "").replace("\\", "") 
        return GoogleTranslator(source='vi', target='hmn').translate(clean_text)
    except:
        return "Lỗi kết nối dịch thuật."

# --- GIAO DIỆN CHÍNH ---

# 1. Header
st.markdown("""
<div class="school-header">
    <h3>SỞ GIÁO DỤC VÀ ĐÀO TẠO TỈNH ĐIỆN BIÊN</h3>
    <h1>🏫 TRƯỜNG PTDTBT TH&THCS NA Ư</h1>
    <h2>🚀 GIA SƯ TOÁN AI - KẾT NỐI TRI THỨC (LỚP 1-9)</h2>
</div>
""", unsafe_allow_html=True)

# 2. Sidebar - MENU CHỌN BÀI HỌC
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3426/3426653.png", width=80)
    st.header("📚 MỤC LỤC SÁCH GIÁO KHOA")
    
    # Cấp 1: Chọn Lớp
    ds_lop = list(CHUONG_TRINH_HOC.keys())
    lop_chon = st.selectbox("1️⃣ Chọn Lớp:", ds_lop)
    
    # Cấp 2: Chọn Chương (Dựa theo Lớp)
    du_lieu_lop = CHUONG_TRINH_HOC[lop_chon]
    ds_chuong = list(du_lieu_lop.keys())
    chuong_chon = st.selectbox("2️⃣ Chọn Chương:", ds_chuong)
    
    # Cấp 3: Chọn Bài (Dựa theo Chương)
    ds_bai = du_lieu_lop[chuong_chon]
    bai_chon = st.selectbox("3️⃣ Chọn Bài học:", ds_bai)
    
    st.markdown("---")
    st.info(f"📍 Đang học: **{lop_chon}**\n\n📂 **{chuong_chon}**\n\n📝 **{bai_chon}**")
    
    if st.button("🔄 Đặt lại trạng thái"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# 3. Khu vực chính
col_trai, col_phai = st.columns([1.6, 1])

# Khởi tạo Session State
if 'de_bai' not in st.session_state:
    st.session_state.de_bai = ""
    st.session_state.dap_an = 0
    st.session_state.goi_y = ""
    st.session_state.bai_hien_tai = ""

# Logic nút bấm sinh đề
def click_sinh_de():
    db, da, gy = tao_de_toan(lop_chon, bai_chon)
    st.session_state.de_bai = db
    st.session_state.dap_an = da
    st.session_state.goi_y = gy
    st.session_state.bai_hien_tai = bai_chon
    st.session_state.da_nop = False

with col_trai:
    st.subheader(f"📖 {bai_chon}")
    
    if st.button("✨ TẠO CÂU HỎI MỚI CHO BÀI NÀY", type="primary", on_click=click_sinh_de):
        pass
    
    # Hiển thị đề bài
    if st.session_state.de_bai:
        st.markdown(f"""
        <div class="problem-card">
            <b>❓ Câu hỏi:</b> {st.session_state.de_bai}
        </div>
        """, unsafe_allow_html=True)

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if st.button("🗣️ Dịch sang tiếng H'Mông"):
                bd = dich_sang_mong(st.session_state.de_bai)
                st.info(f"**H'Mông:** {bd}")

with col_phai:
    st.subheader("✍️ Bảng làm bài")
    
    if st.session_state.de_bai:
        with st.form("form_lam_bai"):
            user_ans = st.number_input("Nhập đáp án của em:", step=0.01, format="%.2f")
            btn_nop = st.form_submit_button("✅ Nộp bài")
            
            if btn_nop:
                st.session_state.da_nop = True
                if abs(user_ans - st.session_state.dap_an) <= 0.05: # Chấp nhận sai số nhỏ
                    st.balloons()
                    st.markdown(f'<p class="success-msg">CHÍNH XÁC! Em rất giỏi!</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="error-msg">Sai rồi. Đáp án đúng là: {st.session_state.dap_an}</p>', unsafe_allow_html=True)
                    
                    # --- PHẦN GỢI Ý CHI TIẾT ---
                    st.markdown("### 💡 Gợi ý chi tiết:")
                    with st.container():
                         # Sử dụng st.markdown để render LaTeX
                         st.markdown(st.session_state.goi_y)
                    
                    with st.expander("Xem gợi ý tiếng H'Mông"):
                         st.write(dich_sang_mong(st.session_state.goi_y))
    else:
        st.info("👈 Hãy chọn bài học và nhấn nút 'Tạo câu hỏi mới' để bắt đầu.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <small>© 2025 Dự án Chuyển đổi số - Trường PTDTBT TH&THCS Na Ư.<br>
    Hệ thống hỗ trợ học tập bám sát chương trình Giáo dục phổ thông mới (2018).</small>
</div>
""", unsafe_allow_html=True)
