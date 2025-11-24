# ... (GIỮ NGUYÊN PHẦN IMPORT, CẤU HÌNH, CSS, DỮ LIỆU CHUONG_TRINH_HOC, VÀ HÀM tao_de_toan Ở TRÊN) ...

# --- GIAO DIỆN CHÍNH ---

# Header với bộ đếm (Giữ nguyên)
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

# --- KHỞI TẠO STATE ---
if 'de_bai' not in st.session_state:
    st.session_state.de_bai = ""
    st.session_state.q_type = "number"
    st.session_state.dap_an = 0
    st.session_state.options = []
    st.session_state.goi_y_text = ""
    st.session_state.goi_y_latex = ""
    st.session_state.show_hint = False
    st.session_state.submitted = False
    st.session_state.current_lesson = "" # Để theo dõi bài học hiện tại

# --- THANH TÌM KIẾM & ĐIỀU HƯỚNG (Đã sửa đổi theo yêu cầu) ---

st.markdown("### 🔍 Bạn muốn ôn tập kiến thức nào?")

# 1. Chọn Lớp (Đóng vai trò thanh tìm kiếm lớn)
ds_lop = list(CHUONG_TRINH_HOC.keys())
# Index = None để ô trống lúc đầu, tạo cảm giác như thanh tìm kiếm
lop_chon = st.selectbox(
    "Gõ hoặc chọn lớp học (Ví dụ: Lớp 5, Lớp 9...)", 
    ds_lop, 
    index=None, 
    placeholder="Chọn lớp học..."
)

# Chỉ hiện các lựa chọn tiếp theo nếu đã chọn Lớp
if lop_chon:
    du_lieu_lop = CHUONG_TRINH_HOC[lop_chon]
    ds_chuong = list(du_lieu_lop.keys())
    
    col_nav1, col_nav2 = st.columns(2)
    
    with col_nav1:
        chuong_chon = st.selectbox("📂 Chọn Chủ đề / Chương:", ds_chuong)
    
    with col_nav2:
        ds_bai = du_lieu_lop[chuong_chon]
        # Khi chọn bài học, tự động sinh đề luôn bằng callback
        bai_chon = st.selectbox("📖 Chọn Bài học:", ds_bai)

    # LOGIC TỰ ĐỘNG SINH ĐỀ KHI CHỌN BÀI MỚI
    # Nếu bài học thay đổi so với lần trước, tự động tạo câu hỏi mới
    if bai_chon != st.session_state.current_lesson:
        st.session_state.current_lesson = bai_chon
        # Gọi hàm sinh đề
        db, qt, da, ops, gyt, gyl = tao_de_toan(lop_chon, bai_chon)
        st.session_state.de_bai = db
        st.session_state.q_type = qt
        st.session_state.dap_an = da
        st.session_state.options = ops
        st.session_state.goi_y_text = gyt
        st.session_state.goi_y_latex = gyl
        st.session_state.show_hint = False
        st.session_state.submitted = False
        # Rerun để hiển thị ngay lập tức
        st.rerun()

    # --- HIỂN THỊ BÀI TẬP ---
    st.markdown("---")
    
    col_trai, col_phai = st.columns([1.6, 1])

    # Hàm dùng cho nút "Đổi câu hỏi khác"
    def click_sinh_de_moi():
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
        # Hiển thị đề bài (Đã tự động sinh ở trên)
        if st.session_state.de_bai:
            st.markdown(f'<div class="problem-box">', unsafe_allow_html=True)
            st.markdown(f"### ❓ Câu hỏi: {bai_chon}")
            st.markdown(f"## {st.session_state.de_bai}")
            st.markdown('</div>', unsafe_allow_html=True)

            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                # Nút này chỉ dùng khi muốn đổi câu hỏi KHÁC cùng bài
                st.button("🔄 Đổi câu hỏi khác", on_click=click_sinh_de_moi)
            with col_btn2:
                if st.button("🗣️ Dịch H'Mông"):
                    text_to_translate = st.session_state.de_bai.replace("$", "")
                    bd = dich_sang_mong(text_to_translate)
                    st.info(f"**H'Mông:** {bd}")

    with col_phai:
        if st.session_state.de_bai:
            st.markdown("### ✍️ Trả lời")
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
                    
                translation = dich_sang_mong(st.session_state.goi_y_text)
                st.markdown('<div class="hmong-hint">', unsafe_allow_html=True)
                st.markdown(f"**🗣️ H'Mông:** {translation}")
                if st.session_state.goi_y_latex:
                    st.latex(st.session_state.goi_y_latex)
                st.markdown('</div>', unsafe_allow_html=True)

else:
    # Màn hình chào mừng khi chưa chọn lớp
    st.info("👈 Hãy chọn Lớp học ở trên để bắt đầu!")
    st.markdown("""
    <div style="text-align: center; opacity: 0.5;">
        <h3>Hướng dẫn:</h3>
        <p>1. Chọn Lớp học (Lớp 1 - Lớp 9).</p>
        <p>2. Chọn Chủ đề và Bài học tương ứng.</p>
        <p>3. Hệ thống sẽ tự động đưa ra câu hỏi.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("© 2025 Trường PTDTBT TH&THCS Na Ư - Bản Mường.")
