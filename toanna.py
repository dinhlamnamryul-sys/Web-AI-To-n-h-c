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
        "Chương 1: Các số từ 0 đến 10": ["Các số 0, 1, 2, 3, 4, 5", "Các số 6, 7, 8, 9, 10", "So sánh số"],
        "Chương 3: Phép cộng, trừ trong phạm vi 10": ["Phép cộng trong phạm vi 10", "Phép trừ trong phạm vi 10"],
        "Chương 4: Các số trong phạm vi 100": ["Phép cộng (không nhớ)", "Phép trừ (không nhớ)"]
    },
    "Lớp 2": {
        "Chương 2: Phép cộng, trừ qua 10": ["Phép cộng qua 10", "Phép trừ qua 10"],
        "Chương 4: Phép nhân, Phép chia": ["Bảng nhân 2, 5", "Bảng chia 2, 5"]
    },
    "Lớp 3": {
        "Chương 1: Phép nhân và chia trong phạm vi 1000": ["Bảng nhân 3, 4, 6, 7, 8, 9", "Bảng chia 3, 4, 6, 7, 8, 9"],
        "Chương 2: Một số hình phẳng": ["Chu vi hình chữ nhật", "Chu vi hình vuông"], 
        "Chương 4: Diện tích": ["Diện tích hình chữ nhật", "Diện tích hình vuông"]
    },
    "Lớp 4": {
        "Chương 2: Bốn phép tính số tự nhiên": ["Phép cộng, trừ", "Phép nhân, chia"],
        "Chương 4: Phân số": ["Rút gọn phân số", "Cộng phân số", "Nhân phân số"]
    },
    "Lớp 5": {
        "Chương 2: Số thập phân": ["Cộng số thập phân", "Nhân số thập phân"],
        "Chương 3: Hình học": ["Chu vi hình tròn", "Diện tích hình thang"]
    },
    "Lớp 6": {
        "Chương 1: Tập hợp số tự nhiên": ["Lũy thừa với số mũ tự nhiên", "Thứ tự thực hiện phép tính"],
        "Chương 2: Số nguyên": ["Cộng trừ số nguyên", "Nhân chia số nguyên"]
    },
    "Lớp 7": {
        "Chương 1: Số hữu tỉ": ["Lũy thừa của số hữu tỉ", "Cộng trừ số hữu tỉ"],
        "Chương 2: Số thực": ["Căn bậc hai số học", "Làm tròn số"]
    },
    "Lớp 8": {
        "Chương 1: Đa thức": ["Nhân đa thức", "Hằng đẳng thức"],
        "Chương 3: Phân thức đại số": ["Cộng trừ phân thức"]
    },
    "Lớp 9": {
        "Chương 1: Hệ phương trình": ["Giải hệ phương trình"],
        "Chương 3: Căn thức": ["Căn bậc hai", "Trục căn thức"]
    }
}

# --- CSS LÀM ĐẸP GIAO DIỆN ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(to right, #f0f2f5, #ffffff); }
    .school-header {
        background: linear-gradient(135deg, #1565C0, #1976D2);
        color: white; padding: 20px; border-radius: 15px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px;
    }
    .problem-box {
        background-color: white; 
        padding: 30px; 
        border-radius: 20px;
        border: 2px solid #e3f2fd;
        box-shadow: 0 6px 15px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button { border-radius: 25px; font-weight: 600; width: 100%; height: 50px; }
    h3 { color: #0d47a1; }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def sinh_so(lop, min_v=1, max_v=10):
    if "Lớp 1" in lop: return random.randint(1, 10)
    if "Lớp 2" in lop: return random.randint(2, 20)
    if "Lớp 3" in lop: return random.randint(10, 50)
    if "Lớp 4" in lop or "Lớp 5" in lop: return random.randint(10, 100)
    if "Lớp 6" in lop or "Lớp 7" in lop: return random.randint(-20, 20)
    return random.randint(-50, 50)

def tao_de_toan(lop, bai_hoc):
    """
    Sinh đề bài dưới dạng LaTeX string (kẹp giữa dấu $).
    Trả về: (Câu hỏi hiển thị, Đáp án số, Gợi ý text, Gợi ý LaTeX)
    """
    bai_lower = bai_hoc.lower()
    de_latex = ""  # Chuỗi đề bài dạng LaTeX để hiển thị
    dap_an = 0
    goi_y_text = ""
    goi_y_latex = ""

    # 1. SỐ HỌC (CỘNG, TRỪ, NHÂN, CHIA)
    if any(x in bai_lower for x in ["cộng", "tổng"]):
        a = sinh_so(lop, 1, 20)
        b = sinh_so(lop, 1, 20)
        # Nếu lớp 1-3, đảm bảo dương
        if "Lớp 6" not in lop and "Lớp 7" not in lop and "Lớp 8" not in lop and "Lớp 9" not in lop:
            a, b = abs(a), abs(b)
        
        # LaTeX: dùng dấu + bình thường
        if b < 0:
            de_latex = f"Tính: ${a} + ({b}) = ?$"
        else:
            de_latex = f"Tính: ${a} + {b} = ?$"
            
        dap_an = a + b
        goi_y_text = "Thực hiện phép cộng:"
        goi_y_latex = f"{a} + {b}"

    elif any(x in bai_lower for x in ["trừ", "hiệu"]):
        a = sinh_so(lop, 5, 20)
        b = sinh_so(lop, 1, a)
        # LaTeX: dấu -
        if b < 0:
            de_latex = f"Tính: ${a} - ({b}) = ?$"
        else:
            de_latex = f"Tính: ${a} - {b} = ?$"
        
        dap_an = a - b
        goi_y_text = "Thực hiện phép trừ:"
        goi_y_latex = f"{a} - {b}"

    elif any(x in bai_lower for x in ["nhân", "tích"]):
        a = sinh_so(lop, 2, 9)
        b = sinh_so(lop, 2, 9)
        # LaTeX: dùng \times cho dấu nhân đẹp
        if b < 0:
            de_latex = f"Tính: ${a} \\times ({b}) = ?$"
        else:
            de_latex = f"Tính: ${a} \\times {b} = ?$"
            
        dap_an = a * b
        goi_y_text = "Thực hiện phép nhân:"
        goi_y_latex = f"{a} \\times {b}"

    elif any(x in bai_lower for x in ["chia", "thương"]):
        b = sinh_so(lop, 2, 9)
        if b == 0: b = 2
        kq = sinh_so(lop, 2, 9)
        a = abs(b * kq)
        
        # LaTeX: dùng : hoặc \div (chia hết dùng :)
        de_latex = f"Tính: ${a} : {b} = ?$"
        dap_an = kq
        goi_y_text = "Thực hiện phép chia:"
        goi_y_latex = f"{a} : {b}"

    # 2. PHÂN SỐ (Lớp 4, 5, 6, 7)
    elif "phân số" in bai_lower:
        if "cộng" in bai_lower:
            t1, m1 = random.randint(1, 5), random.randint(2, 5)
            t2, m2 = random.randint(1, 5), m1 # Cùng mẫu cho dễ trước
            de_latex = f"Tính: $\\frac{{{t1}}}{{{m1}}} + \\frac{{{t2}}}{{{m2}}} = ?$"
            dap_an = (t1 + t2) / m1
            goi_y_text = "Cộng tử số, giữ nguyên mẫu số:"
            goi_y_latex = f"\\frac{{{t1} + {t2}}}{{{m1}}}"
        elif "nhân" in bai_lower:
            t1, m1 = random.randint(1, 5), random.randint(2, 5)
            t2, m2 = random.randint(1, 5), random.randint(2, 5)
            de_latex = f"Tính: $\\frac{{{t1}}}{{{m1}}} \\times \\frac{{{t2}}}{{{m2}}} = ?$"
            dap_an = (t1 * t2) / (m1 * m2)
            goi_y_text = "Tử nhân tử, mẫu nhân mẫu:"
            goi_y_latex = f"\\frac{{{t1} \\times {t2}}}{{{m1} \\times {m2}}}"
        else: # Rút gọn hoặc mặc định
            val = random.randint(2, 5)
            t, m = 3 * val, 4 * val # Ví dụ 6/8
            de_latex = f"Rút gọn phân số (nhập kết quả thập phân): $\\frac{{{t}}}{{{m}}} = ?$"
            dap_an = t / m
            goi_y_text = "Chia cả tử và mẫu cho ước chung lớn nhất:"
            goi_y_latex = f"\\frac{{{t} : {val}}}{{{m} : {val}}}"

    # 3. LŨY THỪA (Lớp 6, 7)
    elif "lũy thừa" in bai_lower:
        base = random.randint(2, 5)
        exp = random.randint(2, 3)
        # LaTeX: base^exp
        de_latex = f"Tính: ${base}^{{{exp}}} = ?$"
        dap_an = base ** exp
        goi_y_text = f"Nhân {base} với chính nó {exp} lần:"
        expansion = " \\times ".join([str(base)] * exp)
        goi_y_latex = f"{base}^{{{exp}}} = {expansion}"

    # 4. CĂN THỨC (Lớp 7, 9)
    elif "căn" in bai_lower:
        kq = random.randint(2, 12)
        n = kq**2
        # LaTeX: \sqrt{n}
        de_latex = f"Tính: $\\sqrt{{{n}}} = ?$"
        dap_an = kq
        goi_y_text = f"Số nào bình phương lên bằng {n}?"
        goi_y_latex = f"\\sqrt{{{n}}} = {kq} \\quad (\\text{{vì }} {kq}^2 = {n})"

    # 5. HÌNH HỌC (Công thức chu vi/diện tích)
    elif "vuông" in bai_lower:
        a = random.randint(3, 10)
        if "chu vi" in bai_lower:
            de_latex = f"Hình vuông cạnh ${a}cm$. Tính Chu vi ($cm$)?"
            dap_an = a * 4
            goi_y_text = "Công thức chu vi hình vuông:"
            goi_y_latex = f"P = a \\times 4 = {a} \\times 4"
        else:
            de_latex = f"Hình vuông cạnh ${a}cm$. Tính Diện tích ($cm^2$)?"
            dap_an = a * a
            goi_y_text = "Công thức diện tích hình vuông:"
            goi_y_latex = f"S = a^2 = {a}^2"

    elif "chữ nhật" in bai_lower:
        a, b = random.randint(5, 10), random.randint(2, 4)
        if "chu vi" in bai_lower:
            de_latex = f"HCN có dài ${a}cm$, rộng ${b}cm$. Tính Chu vi ($cm$)?"
            dap_an = (a + b) * 2
            goi_y_text = "Công thức chu vi HCN:"
            goi_y_latex = f"P = (a + b) \\times 2 = ({a} + {b}) \\times 2"
        else:
            de_latex = f"HCN có dài ${a}cm$, rộng ${b}cm$. Tính Diện tích ($cm^2$)?"
            dap_an = a * b
            goi_y_text = "Công thức diện tích HCN:"
            goi_y_latex = f"S = a \\times b = {a} \\times {b}"
            
    elif "tròn" in bai_lower: # Lớp 5
        r = random.randint(2, 5)
        de_latex = f"Hình tròn bán kính $r = {r}$. Tính Chu vi (lấy $\pi \\approx 3.14$)?"
        dap_an = r * 2 * 3.14
        goi_y_text = "Công thức chu vi hình tròn:"
        goi_y_latex = f"C = r \\times 2 \\times 3.14 = {r} \\times 2 \\times 3.14"

    # 6. ĐẠI SỐ / HỆ PHƯƠNG TRÌNH (Lớp 8, 9)
    elif "hệ phương trình" in bai_lower:
        x = random.randint(2, 5)
        y = random.randint(1, 3)
        S = x + y
        D = x - y
        # LaTeX: Hệ phương trình dùng cases
        # Lưu ý: Trong f-string cần double ngoặc nhọn {{ }} cho LaTeX
        de_latex = f"Giải hệ phương trình (tìm x): $$\\begin{{cases}} x + y = {S} \\\\ x - y = {D} \\end{{cases}}$$"
        dap_an = x
        goi_y_text = "Cộng đại số hai phương trình:"
        goi_y_latex = f"(x+y) + (x-y) = {S} + {D} \\Rightarrow 2x = {S+D}"

    else:
        # Fallback: Phép cộng cơ bản
        a, b = random.randint(1, 10), random.randint(1, 10)
        de_latex = f"Tính: ${a} + {b} = ?$"
        dap_an = a + b
        goi_y_text = "Phép cộng:"
        goi_y_latex = f"{a} + {b}"

    return de_latex, dap_an, goi_y_text, goi_y_latex

# Hàm dịch thuật
def dich_sang_mong(text):
    try:
        # Loại bỏ các ký tự LaTeX trước khi dịch để tránh lỗi
        clean_text = text.replace("$", "").replace("\\", "").replace("{", "").replace("}", "")
        return GoogleTranslator(source='vi', target='hmn').translate(clean_text)
    except:
        return "..."

# --- GIAO DIỆN CHÍNH ---

# 1. Header
st.markdown("""
<div class="school-header">
    <h3>SỞ GIÁO DỤC VÀ ĐÀO TẠO TỈNH ĐIỆN BIÊN</h3>
    <h1>🏫 TRƯỜNG PTDTBT TH&THCS NA Ư</h1>
    <h2>🚀 GIA SƯ TOÁN AI - CÔNG NGHỆ LATEX</h2>
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
    st.session_state.show_hint = False

def click_sinh_de():
    db, da, gyt, gyl = tao_de_toan(lop_chon, bai_chon)
    st.session_state.de_bai = db
    st.session_state.dap_an = da
    st.session_state.goi_y_text = gyt
    st.session_state.goi_y_latex = gyl
    st.session_state.show_hint = False

with col_trai:
    st.subheader(f"📖 {bai_chon}")
    
    if st.button("✨ TẠO CÂU HỎI MỚI", type="primary", on_click=click_sinh_de):
        pass
    
    if st.session_state.de_bai:
        # HIỂN THỊ ĐỀ BÀI ĐẸP VỚI LATEX
        st.markdown('<div class="problem-box">', unsafe_allow_html=True)
        st.markdown("### ❓ Câu hỏi:")
        # Render công thức toán học to rõ
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
            user_ans = st.number_input("Nhập đáp án:", step=0.01, format="%.2f")
            btn_nop = st.form_submit_button("✅ Kiểm tra")
            
            if btn_nop:
                # Logic kiểm tra đáp án
                is_correct = False
                if isinstance(st.session_state.dap_an, int) or float(st.session_state.dap_an).is_integer():
                     # Nếu đáp án là số nguyên, kiểm tra chính xác hoặc sai số rất nhỏ
                     is_correct = abs(user_ans - st.session_state.dap_an) < 0.001
                else:
                     # Nếu là số thực, cho phép sai số 0.05
                     is_correct = abs(user_ans - st.session_state.dap_an) <= 0.05

                if is_correct:
                    st.balloons()
                    st.success("CHÍNH XÁC! 👏")
                else:
                    st.error(f"Sai rồi. Đáp án đúng là: {st.session_state.dap_an:.2f}")
                    st.session_state.show_hint = True
        
        # HIỂN THỊ GỢI Ý NẾU CẦN
        if st.session_state.show_hint:
            st.markdown("---")
            st.info(f"💡 **Gợi ý:** {st.session_state.goi_y_text}")
            # Hiển thị công thức gợi ý bằng LaTeX
            if st.session_state.goi_y_latex:
                st.latex(st.session_state.goi_y_latex)
                
            with st.expander("Xem dịch gợi ý"):
                 st.write(dich_sang_mong(st.session_state.goi_y_text))

    else:
        st.info("👈 Hãy chọn bài học ở cột bên trái và nhấn nút 'Tạo câu hỏi mới'.")

# Footer
st.markdown("---")
st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư. Ứng dụng tích hợp công nghệ hiển thị Toán học LaTeX.")
