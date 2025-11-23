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
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px;
    }
    .problem-card {
        background-color: white; padding: 25px; border-radius: 15px;
        border-left: 8px solid #ff9800; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        font-size: 1.4rem; margin-bottom: 20px;
        color: #2c3e50; font-weight: 500;
    }
    .hint-container {
        background-color: #e8f5e9; padding: 15px; border-radius: 10px;
        border: 1px solid #c8e6c9; margin-top: 15px;
    }
    .success-msg { color: #2e7d32; font-weight: bold; font-size: 1.2rem; }
    .error-msg { color: #c62828; font-weight: bold; font-size: 1.1rem; }
    .stButton>button { border-radius: 20px; font-weight: 600; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def sinh_so_ngau_nhien(lop):
    """Hàm phụ trợ sinh số phù hợp cấp độ"""
    if "Lớp 1" in lop: return random.randint(1, 10), random.randint(1, 10)
    if "Lớp 2" in lop: return random.randint(10, 90), random.randint(1, 20)
    if "Lớp 3" in lop: return random.randint(100, 900), random.randint(2, 9)
    if "Lớp 4" in lop or "Lớp 5" in lop: return random.randint(1000, 9000), random.randint(10, 99)
    if "Lớp 6" in lop: return random.randint(-50, 50), random.randint(-20, 20)
    return random.randint(-100, 100), random.randint(-100, 100)

def tao_de_toan(lop, bai_hoc):
    """
    Hàm sinh đề và gợi ý chuẩn LaTeX.
    goi_y_text: Lời giải thích ngắn gọn.
    goi_y_latex: Công thức toán học để hiển thị bằng st.latex()
    """
    bai_hoc_lower = bai_hoc.lower()
    de_bai, dap_an = "", 0
    goi_y_text, goi_y_latex = "", ""

    # --- 1. SỐ HỌC CƠ BẢN ---
    if any(x in bai_hoc_lower for x in ["cộng", "tổng", "thêm"]):
        a, b = sinh_so_ngau_nhien(lop)
        if b < 0:
            de_bai = f"Tính: {a} - {abs(b)} = ?"
            goi_y_text = "Thực hiện phép trừ số nguyên:"
            goi_y_latex = f"{a} - {abs(b)}"
        else:
            de_bai = f"Tính: {a} + {b} = ?"
            goi_y_text = "Đặt tính rồi tính:"
            goi_y_latex = f"{a} + {b}"
        dap_an = a + b
        
    elif any(x in bai_hoc_lower for x in ["trừ", "hiệu", "bớt", "ít hơn"]):
        a, b = sinh_so_ngau_nhien(lop)
        if "Lớp 6" not in lop and "Lớp 7" not in lop and "Lớp 8" not in lop and "Lớp 9" not in lop:
            a, b = max(a, b), min(a, b)
        
        if b < 0: 
            de_bai = f"Tính: {a} - ({b}) = ?"
            goi_y_text = "Trừ cho số âm thành cộng số dương:"
            goi_y_latex = f"{a} - ({b}) = {a} + {abs(b)}"
        else:
            de_bai = f"Tính: {a} - {b} = ?"
            goi_y_text = "Thực hiện phép trừ:"
            goi_y_latex = f"{a} - {b}"
        dap_an = a - b
        
    elif any(x in bai_hoc_lower for x in ["nhân", "tích", "gấp"]):
        if "Lớp 2" in lop: a, b = random.randint(2, 5), random.randint(1, 10)
        elif "Lớp 3" in lop: a, b = random.randint(2, 9), random.randint(2, 9)
        else: a, b = sinh_so_ngau_nhien(lop)
        
        if b < 0: de_bai = f"Tính: {a} x ({b}) = ?"
        else: de_bai = f"Tính: {a} x {b} = ?"
        
        dap_an = a * b
        goi_y_text = "Thực hiện phép nhân:"
        goi_y_latex = f"{a} \\times {b}"

    elif any(x in bai_hoc_lower for x in ["chia", "thương"]):
        if "Lớp 2" in lop: b = random.choice([2, 5])
        elif "Lớp 3" in lop: b = random.randint(2, 9)
        else: b = random.randint(2, 20)
        if b == 0: b = 2
        kq = random.randint(2, 10)
        a = b * kq
        
        de_bai = f"Tính: {a} : {b} = ?"
        dap_an = kq
        goi_y_text = "Tìm số nhân với số chia ra số bị chia:"
        goi_y_latex = f"\\frac{{{a}}}{{{b}}} = ?"

    # --- 2. HÌNH HỌC ---
    elif "vuông" in bai_hoc_lower and ("chu vi" in bai_hoc_lower or "diện tích" in bai_hoc_lower):
        canh = random.randint(2, 20)
        if "chu vi" in bai_hoc_lower:
            de_bai = f"Hình vuông cạnh {canh}cm. Tính Chu vi (cm)?"
            dap_an = canh * 4
            goi_y_text = "Chu vi = Cạnh nhân 4"
            goi_y_latex = f"P = {canh} \\times 4"
        else:
            de_bai = f"Hình vuông cạnh {canh}cm. Tính Diện tích (cm²)?"
            dap_an = canh * canh
            goi_y_text = "Diện tích = Cạnh nhân Cạnh"
            goi_y_latex = f"S = {canh} \\times {canh} = {canh}^2"
            
    elif "chữ nhật" in bai_hoc_lower and ("chu vi" in bai_hoc_lower or "diện tích" in bai_hoc_lower):
        d = random.randint(5, 20)
        r = random.randint(1, d-1)
        if "chu vi" in bai_hoc_lower:
            de_bai = f"HCN có dài {d}cm, rộng {r}cm. Tính Chu vi (cm)?"
            dap_an = (d + r) * 2
            goi_y_text = "Chu vi = (Dài + Rộng) nhân 2"
            goi_y_latex = f"P = ({d} + {r}) \\times 2"
        else:
            de_bai = f"HCN có dài {d}cm, rộng {r}cm. Tính Diện tích (cm²)?"
            dap_an = d * r
            goi_y_text = "Diện tích = Dài nhân Rộng"
            goi_y_latex = f"S = {d} \\times {r}"

    # --- 3. ĐẠI SỐ ---
    elif "lũy thừa" in bai_hoc_lower:
        base = random.randint(2, 5)
        exp = random.randint(2, 4)
        de_bai = f"Tính: {base}^{exp} = ?"
        dap_an = base ** exp
        goi_y_text = f"Nhân số {base} với chính nó {exp} lần:"
        # Tạo chuỗi nhân: 2 x 2 x 2
        expansion = " \\times ".join([str(base)] * exp)
        goi_y_latex = f"{base}^{{{exp}}} = {expansion}"
        
    elif "làm tròn" in bai_hoc_lower:
        val = random.uniform(10, 100)
        de_bai = f"Làm tròn số {val:.3f} đến chữ số thập phân thứ nhất."
        dap_an = round(val, 1)
        digit_2 = int((val * 100) % 10)
        goi_y_text = f"Xét chữ số thứ 2 sau dấu phẩy là {digit_2}. Nếu >= 5 thì cộng 1 vào trước nó."
        goi_y_latex = f"{val:.3f} \\approx ?"
        
    elif "phương trình" in bai_hoc_lower and "hệ" not in bai_hoc_lower:
        # ax + b = 0
        a = random.randint(2, 10)
        b = random.randint(1, 20) * random.choice([-1, 1])
        
        # Hiển thị đề bài đẹp
        dau_b = f"- {abs(b)}" if b < 0 else f"+ {b}"
        de_bai = f"Tìm x biết: {a}x {dau_b} = 0"
        dap_an = round(-b/a, 2)
        
        # Gợi ý ngắn gọn
        val_rhs = -b
        goi_y_text = "Chuyển vế rồi chia:"
        goi_y_latex = f"{a}x = {val_rhs} \\Rightarrow x = \\frac{{{val_rhs}}}{{{a}}}"
        
    elif "hệ phương trình" in bai_hoc_lower:
        x = random.randint(5, 20)
        y = random.randint(1, x)
        S = x + y
        D = x - y
        de_bai = f"Cho hệ: x + y = {S} và x - y = {D}. Tìm x?"
        dap_an = x
        goi_y_text = "Cộng hai vế phương trình:"
        goi_y_latex = f"(x+y) + (x-y) = {S} + {D} \\Rightarrow 2x = {S+D}"
        
    elif "căn" in bai_hoc_lower:
        kq = random.randint(2, 15)
        n = kq**2
        de_bai = f"Tính căn bậc hai số học của {n}?"
        dap_an = kq
        goi_y_text = f"Tìm số dương bình phương lên bằng {n}:"
        goi_y_latex = f"\\sqrt{{{n}}} = ? \\quad (\\text{{vì }} ?^2 = {n})"

    else:
        # Fallback
        a, b = sinh_so_ngau_nhien(lop)
        de_bai = f"Tính: {a} + {b} = ?"
        dap_an = a + b
        goi_y_text = "Phép cộng cơ bản:"
        goi_y_latex = f"{a} + {b}"

    return de_bai, dap_an, goi_y_text, goi_y_latex

# Hàm dịch thuật
def dich_sang_mong(text):
    try:
        return GoogleTranslator(source='vi', target='hmn').translate(text)
    except:
        return "..."

# --- GIAO DIỆN CHÍNH ---

# 1. Header
st.markdown("""
<div class="school-header">
    <h3>SỞ GIÁO DỤC VÀ ĐÀO TẠO TỈNH ĐIỆN BIÊN</h3>
    <h1>🏫 TRƯỜNG PTDTBT TH&THCS NA Ư</h1>
    <h2>🚀 GIA SƯ TOÁN AI - KẾT NỐI TRI THỨC (LỚP 1-9)</h2>
</div>
""", unsafe_allow_html=True)

# 2. Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3426/3426653.png", width=80)
    st.header("📚 SÁCH GIÁO KHOA")
    
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
col_trai, col_phai = st.columns([1.5, 1])

# Init Session
if 'de_bai' not in st.session_state:
    st.session_state.de_bai = ""
    st.session_state.dap_an = 0
    st.session_state.goi_y_text = ""
    st.session_state.goi_y_latex = ""

def click_sinh_de():
    db, da, gyt, gyl = tao_de_toan(lop_chon, bai_chon)
    st.session_state.de_bai = db
    st.session_state.dap_an = da
    st.session_state.goi_y_text = gyt
    st.session_state.goi_y_latex = gyl
    st.session_state.da_nop = False
    st.session_state.show_hint = False # Ẩn gợi ý lúc đầu

with col_trai:
    st.subheader(f"📖 {bai_chon}")
    
    if st.button("✨ BÀI TẬP MỚI", type="primary", on_click=click_sinh_de):
        pass
    
    if st.session_state.de_bai:
        st.markdown(f"""
        <div class="problem-card">
            ❓ {st.session_state.de_bai}
        </div>
        """, unsafe_allow_html=True)
        
        # Chỉ hiển thị công thức đề bài nếu cần (ví dụ cho bài căn bậc hai để đẹp hơn)
        if "căn" in st.session_state.de_bai.lower():
             # Trích xuất số để hiển thị latex đề bài
             import re
             num = re.findall(r'\d+', st.session_state.de_bai)
             if num:
                 st.latex(f"\\sqrt{{{num[0]}}} = ?")

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if st.button("🗣️ Dịch H'Mông"):
                bd = dich_sang_mong(st.session_state.de_bai)
                st.info(f"**H'Mông:** {bd}")

with col_phai:
    st.subheader("✍️ Làm bài")
    
    if st.session_state.de_bai:
        with st.form("form_lam_bai"):
            user_ans = st.number_input("Nhập đáp án:", step=0.01, format="%.2f")
            btn_nop = st.form_submit_button("✅ Kiểm tra")
            
            if btn_nop:
                st.session_state.da_nop = True
                # So sánh: Nếu là số nguyên thì so sánh int, nếu float thì so sánh sai số
                is_correct = False
                if float(st.session_state.dap_an).is_integer():
                    is_correct = round(user_ans, 2) == st.session_state.dap_an
                else:
                    is_correct = abs(user_ans - st.session_state.dap_an) <= 0.05

                if is_correct:
                    st.balloons()
                    st.success("CHÍNH XÁC! 👏")
                else:
                    st.error(f"Sai rồi. Đáp án đúng là: {st.session_state.dap_an}")
                    st.session_state.show_hint = True
        
        # Hiển thị gợi ý nếu làm sai hoặc người dùng muốn xem
        if st.session_state.get('show_hint', False):
            st.markdown("---")
            st.markdown("### 💡 Gợi ý:")
            st.write(st.session_state.goi_y_text)
            # DÙNG ST.LATEX ĐỂ HIỂN THỊ CÔNG THỨC CHUẨN ĐẸP KHÔNG LỖI
            if st.session_state.goi_y_latex:
                st.latex(st.session_state.goi_y_latex)
                
            with st.expander("Xem dịch gợi ý"):
                 st.write(dich_sang_mong(st.session_state.goi_y_text))

    else:
        st.info("👈 Chọn bài học rồi nhấn nút tạo bài tập.")

# Footer
st.markdown("---")
st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư.")
