import streamlit as st
import random
import math
from deep_translator import GoogleTranslator

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gia sư Toán AI - Na Ư (Lớp 1-9)",
    page_icon="📐",
    layout="wide"
)

# --- CSS LÀM ĐẸP GIAO DIỆN ---
st.markdown("""
<style>
    /* Màu nền Gradient đẹp mắt */
    .stApp {
        background: linear-gradient(to right, #e0eafc, #cfdef3);
    }
    /* Khung tiêu đề trường học */
    .school-header {
        background-color: #1a237e;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    /* Khung bài tập */
    .problem-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #ff6f00;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        font-size: 1.2rem;
    }
    /* Nút bấm xịn hơn */
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
        width: 100%;
    }
    .success-msg {
        color: #2e7d32;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .error-msg {
        color: #c62828;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC AI SINH ĐỀ THEO LỚP ---

def sinh_de_tieu_hoc(lop):
    """Sinh đề cho lớp 1 đến lớp 5"""
    de_bai, dap_an, goi_y = "", 0, ""
    
    if lop in ["Lớp 1", "Lớp 2"]:
        # Cộng trừ cơ bản
        pheptoan = random.choice(['+', '-'])
        if lop == "Lớp 1":
            a = random.randint(1, 10)
            b = random.randint(1, 10)
        else: # Lớp 2 (phạm vi 100)
            a = random.randint(10, 50)
            b = random.randint(1, 40)
            
        if pheptoan == '+':
            de_bai = f"Tính phép cộng: {a} + {b} = ?"
            dap_an = a + b
            goi_y = f"Em hãy đếm hoặc đặt tính rồi tính: {a} cộng thêm {b}."
        else:
            # Đảm bảo trừ ra số dương
            lon = max(a, b)
            be = min(a, b)
            de_bai = f"Tính phép trừ: {lon} - {be} = ?"
            dap_an = lon - be
            goi_y = f"Em hãy bớt đi {be} đơn vị từ số {lon}."

    elif lop == "Lớp 3":
        # Nhân chia (Bảng cửu chương)
        pheptoan = random.choice(['*', '/'])
        if pheptoan == '*':
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            de_bai = f"Tính tích: {a} x {b} = ?"
            dap_an = a * b
            goi_y = f"Em hãy nhớ lại bảng cửu chương {a} hoặc {b}."
        else:
            b = random.randint(2, 9)
            ket_qua = random.randint(2, 9)
            a = b * ket_qua # Đảm bảo chia hết
            de_bai = f"Tính thương: {a} : {b} = ?"
            dap_an = ket_qua
            goi_y = f"Số nào nhân với {b} thì bằng {a}?"

    elif lop in ["Lớp 4", "Lớp 5"]:
        # Hình học: Chu vi, Diện tích
        dang = random.choice(["Hình chữ nhật", "Hình vuông"])
        if dang == "Hình vuông":
            canh = random.randint(5, 20)
            loai_tinh = random.choice(["Chu vi", "Diện tích"])
            if loai_tinh == "Chu vi":
                de_bai = f"Một miếng bìa hình vuông có cạnh {canh}cm. Tính chu vi?"
                dap_an = canh * 4
                goi_y = "Chu vi hình vuông = Cạnh nhân 4."
            else:
                de_bai = f"Một viên gạch hình vuông có cạnh {canh}cm. Tính diện tích?"
                dap_an = canh * canh
                goi_y = "Diện tích hình vuông = Cạnh nhân Cạnh."
        else: # Hình chữ nhật
            dai = random.randint(10, 30)
            rong = random.randint(2, dai - 5)
            de_bai = f"Mảnh vườn hình chữ nhật có dài {dai}m, rộng {rong}m. Tính diện tích?"
            dap_an = dai * rong
            goi_y = "Diện tích hình chữ nhật = Dài nhân Rộng."

    return de_bai, dap_an, goi_y

def sinh_de_thcs(lop):
    """Sinh đề cho lớp 6 đến lớp 9"""
    de_bai, dap_an, goi_y = "", 0, ""

    if lop == "Lớp 6":
        # Lũy thừa và Số nguyên
        dang = random.choice(["Lũy thừa", "Tìm x cơ bản"])
        if dang == "Lũy thừa":
            co_so = random.randint(2, 5)
            so_mu = random.randint(2, 3)
            de_bai = f"Tính giá trị lũy thừa: {co_so}^{so_mu} ( {co_so} mũ {so_mu} )"
            dap_an = co_so ** so_mu
            goi_y = f"Lấy số {co_so} nhân với chính nó {so_mu} lần."
        else:
            x = random.randint(2, 20)
            a = random.randint(10, 50)
            tong = x + a
            de_bai = f"Tìm số tự nhiên x biết: x + {a} = {tong}"
            dap_an = x
            goi_y = f"Muốn tìm số hạng chưa biết, ta lấy Tổng ({tong}) trừ đi số hạng đã biết ({a})."

    elif lop == "Lớp 7":
        # Tỉ lệ thức hoặc Căn bậc hai cơ bản
        dang = random.choice(["Tỉ lệ thức", "Làm tròn"])
        if dang == "Tỉ lệ thức":
            a = random.randint(2, 10)
            b = random.randint(2, 10)
            c = random.randint(2, 10)
            # x/a = b/c => x = (a*b)/c. Chọn số sao cho đẹp
            x = b * c 
            # Đổi lại đề: x/a = c => x = a*c
            de_bai = f"Tìm x biết: x / {a} = {c}"
            dap_an = a * c
            goi_y = f"Muốn tìm số bị chia x, ta lấy thương ({c}) nhân với số chia ({a})."
        else:
            so_thuc = random.uniform(10, 100)
            de_bai = f"Làm tròn số {so_thuc:.3f} đến chữ số thập phân thứ nhất?"
            dap_an = round(so_thuc, 1)
            goi_y = "Nếu chữ số thập phân thứ hai >= 5 thì cộng thêm 1 vào số trước nó."

    elif lop == "Lớp 8":
        # Phương trình bậc nhất (Logic cũ nhưng hay)
        a = random.randint(2, 10)
        b = random.randint(1, 20) * random.choice([-1, 1])
        if b < 0:
            de_bai = f"Giải phương trình: {a}x - {abs(b)} = 0"
        else:
            de_bai = f"Giải phương trình: {a}x + {b} = 0"
        dap_an = round(-b / a, 2)
        goi_y = f"Chuyển {b} sang vế phải đổi dấu, rồi chia cho {a}."

    elif lop == "Lớp 9":
        # Căn bậc hai hoặc Hình học
        dang = random.choice(["Căn bậc hai", "Pythagoras"])
        if dang == "Căn bậc hai":
            kq = random.randint(2, 15)
            so = kq * kq
            de_bai = f"Tính căn bậc hai số học của {so} (√{so})?"
            dap_an = kq
            goi_y = f"Số nào bình phương lên bằng {so}?"
        else:
            # Định lý Pythagoras tìm cạnh huyền
            c1 = random.randint(3, 10)
            c2 = random.randint(3, 10)
            # Chọn bộ số Pythagoras
            bo_so = random.choice([(3,4,5), (6,8,10), (5,12,13), (9,12,15)])
            c1, c2, ch = bo_so
            de_bai = f"Tam giác vuông có 2 cạnh góc vuông là {c1}cm và {c2}cm. Tính cạnh huyền?"
            dap_an = ch
            goi_y = f"Áp dụng định lý Pythagoras: Cạnh huyền = Căn bậc hai của ({c1}^2 + {c2}^2)."

    return de_bai, dap_an, goi_y

# Hàm dịch thuật
def dich_sang_mong(text):
    try:
        translated = GoogleTranslator(source='vi', target='hmn').translate(text)
        return translated
    except:
        return "Đang kết nối AI ngôn ngữ..."

# --- GIAO DIỆN CHÍNH ---

# 1. Header Trường học
st.markdown("""
<div class="school-header">
    <h3>SỞ GIÁO DỤC VÀ ĐÀO TẠO TỈNH ĐIỆN BIÊN</h3>
    <h1>🏫 TRƯỜNG PTDTBT TH&THCS NA Ư</h1>
    <p>ĐỊA CHỈ: XÃ SAM MỨN, HUYỆN ĐIỆN BIÊN</p>
    <h2>🚀 SẢN PHẨM: GIA SƯ TOÁN HỌC AI TOÀN CẤP (LỚP 1-9)</h2>
</div>
""", unsafe_allow_html=True)

# 2. Sidebar (Thanh bên trái)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=100)
    st.header("📚 Cấu hình học tập")
    
    # Chọn cấp học
    cap_hoc = st.radio("Chọn cấp học:", ["Tiểu học (Lớp 1-5)", "THCS (Lớp 6-9)"])
    
    # Chọn lớp cụ thể dựa trên cấp học
    if cap_hoc == "Tiểu học (Lớp 1-5)":
        lop_hoc = st.selectbox("Chọn lớp:", ["Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5"])
    else:
        lop_hoc = st.selectbox("Chọn lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"])
        
    st.info(f"💡 Đang chọn chế độ ôn tập cho: **{lop_hoc}**")
    
    if st.button("🗑️ Xóa lịch sử làm bài"):
        st.session_state.de_bai_hien_tai = ""
        st.rerun()

# 3. Khu vực chính
col_trai, col_phai = st.columns([1.5, 1])

# Khởi tạo Session State
if 'de_bai_hien_tai' not in st.session_state:
    st.session_state.de_bai_hien_tai = ""
    st.session_state.dap_an_hien_tai = 0
    st.session_state.goi_y_hien_tai = ""
    st.session_state.lop_hien_tai = "" # Lưu lớp để tránh hiển thị đề cũ khi đổi lớp

with col_trai:
    st.subheader(f"📝 Đề bài Toán {lop_hoc}:")
    
    # Nút sinh đề
    if st.button("🎲 TẠO ĐỀ BÀI MỚI (AI)", type="primary"):
        # Reset trạng thái
        st.session_state.da_nop = False
        st.session_state.lop_hien_tai = lop_hoc
        
        # Gọi hàm sinh đề tương ứng
        if "Tiểu học" in cap_hoc:
            db, da, gy = sinh_de_tieu_hoc(lop_hoc)
        else:
            db, da, gy = sinh_de_thcs(lop_hoc)
        
        st.session_state.de_bai_hien_tai = db
        st.session_state.dap_an_hien_tai = da
        st.session_state.goi_y_hien_tai = gy
    
    # Hiển thị đề bài
    if st.session_state.de_bai_hien_tai:
        st.markdown(f"""
        <div class="problem-card">
            <b>Đề bài:</b> {st.session_state.de_bai_hien_tai}
        </div>
        """, unsafe_allow_html=True)

        # Nút dịch
        col_dich_1, col_dich_2 = st.columns(2)
        with col_dich_1:
            if st.button("🗣️ Dịch đề sang tiếng H'Mông"):
                ban_dich = dich_sang_mong(st.session_state.de_bai_hien_tai)
                st.success(f"**H'Mông:** {ban_dich}")

with col_phai:
    st.subheader("✍️ Khu vực làm bài")
    
    if st.session_state.de_bai_hien_tai:
        # Form nhập liệu
        with st.form("form_nop_bai"):
            cau_tra_loi = st.number_input("Nhập kết quả của em:", step=0.01, format="%.2f")
            da_nop = st.form_submit_button("✅ Kiểm tra kết quả")
            
            if da_nop:
                # So sánh đáp án (sai số 0.1 cho phép tính xấp xỉ)
                if abs(cau_tra_loi - st.session_state.dap_an_hien_tai) <= 0.1:
                    st.balloons()
                    st.markdown(f'<p class="success-msg">TUYỆT VỜI! Em làm rất đúng!</p>', unsafe_allow_html=True)
                    st.write(f"Đáp án chính xác là: **{st.session_state.dap_an_hien_tai}**")
                else:
                    st.markdown(f'<p class="error-msg">Chưa đúng rồi, em thử lại nhé!</p>', unsafe_allow_html=True)
                    
                    # Hiện gợi ý
                    st.warning("💡 **Gợi ý:** " + st.session_state.goi_y_hien_tai)
                    
                    # Tự động dịch gợi ý nếu cần
                    with st.expander("Xem gợi ý tiếng H'Mông"):
                         st.write(dich_sang_mong(st.session_state.goi_y_hien_tai))

# Footer
st.markdown("---")
st.caption("© 2025 Nhóm tác giả Trường PTDTBT TH&THCS Na Ư - Điện Biên. Ứng dụng hỗ trợ học sinh vùng cao học Toán song ngữ.")
