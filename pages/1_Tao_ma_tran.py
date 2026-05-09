import streamlit as st
import google.generativeai as genai

# ==========================================
API_KEY = "AIzaSyDMAh_Me-btyp6LMLeeMHtqxLKDWw92TOw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') 
# ==========================================

st.set_page_config(page_title="Siêu App Tạo Ma Trận", layout="wide")
st.title("🌟 Siêu App Tạo Ma Trận (Tùy chỉnh Chủ đề cụ thể)")

col_mon, col_lop = st.columns(2)
with col_mon:
    mon_hoc = st.selectbox("📚 Môn học:", ["Toán học", "Tiếng Việt", "Tin học", "Lịch sử & Địa lý", "Khoa học"])
with col_lop:
    lop_hoc = st.selectbox("🏫 Khối lớp:", ["Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5"])

st.subheader("🎯 Nhập các chủ đề bạn muốn kiểm tra")
st.info("💡 Mẹo: Bạn chỉ cần nhập những chủ đề/bài học sẽ xuất hiện trong bài kiểm tra này (ví dụ: Chủ đề 6, Chủ đề 7). AI sẽ chỉ tập trung vào đó.")

# Ô nhập chủ đề được làm to ra để cậu giáo dễ kiểm soát
chu_de_kiem_tra = st.text_area("Danh sách các chủ đề/mạch kiến thức kiểm tra:", 
                                value="Chủ đề 6: [Tên chủ đề]\nChủ đề 7: [Tên chủ đề]", 
                                height=150)

col1, col2 = st.columns(2)
with col1:
    st.subheader("1. Tỷ lệ mức độ (%)")
    m1, m2, m3 = st.columns(3)
    muc_1 = m1.number_input("Mức 1", value=40)
    muc_2 = m2.number_input("Mức 2", value=30)
    muc_3 = m3.number_input("Mức 3", value=30)
    
    st.subheader("2. Khung bảng 10 cột chuẩn trường")
    khung_truong = st.text_area("Lệnh gộp ô (Không nên sửa):", 
                                value="""Vẽ bảng HTML (<table>) có viền:
- Dòng 1: Cột 1 'Mạch kiến thức' (rowspan=2). Các mức 1, 2, 3 và Tổng gộp 2 cột ngang (colspan=2).
- Dòng 2: Các ô 'TN' và 'TL'.
- Mỗi chủ đề: Gộp 3 dòng dọc (rowspan=3) để ghi 'Số câu', 'Câu số', 'Số điểm'.""", height=150)

with col2:
    st.subheader("3. Thông số đề")
    tong_cau = st.number_input("Tổng số câu hỏi trong đề:", value=10)
    tong_diem = st.number_input("Thang điểm tổng:", value=10)

if st.button(f"🚀 TẠO MA TRẬN CHỦ ĐỀ MÔN {mon_hoc.upper()}", type="primary"):
    if (muc_1 + muc_2 + muc_3) != 100:
        st.error("Tổng tỷ lệ phải bằng 100%!")
    else:
        with st.spinner('AI đang tính toán ma trận cho các chủ đề đã chọn...'):
            prompt = f"""
            Bạn là giáo viên chuyên môn {mon_hoc} dạy {lop_hoc}.
            Hãy lập ma trận đề kiểm tra CHỈ KHỐNG CHẾ TRONG CÁC CHỦ ĐỀ SAU:
            {chu_de_kiem_tra}
            
            - Tổng câu: {tong_cau}, Tổng điểm: {tong_diem}.
            - Tỷ lệ: Mức 1 ({muc_1}%), Mức 2 ({muc_2}%), Mức 3 ({muc_3}%).
            
            YÊU CẦU TRÌNH BÀY:
            Xuất CHỈ 1 BẢNG HTML DUY NHẤT (border="1") theo đúng cấu trúc gộp ô:
            {khung_truong}
            Lưu ý: Chỉ tập trung kiến thức vào các chủ đề tôi đã cung cấp bên trên.
            """
            response = model.generate_content(prompt)
            st.markdown(response.text, unsafe_allow_html=True)
            doc_file = f"<meta charset='utf-8'><body>{response.text}</body>"
            st.download_button("📥 TẢI FILE WORD MA TRẬN", data=doc_file, file_name=f"Ma_tran_Chu_de_{mon_hoc}.doc", mime="application/msword")
