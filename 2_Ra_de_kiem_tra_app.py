
import streamlit as st
import google.generativeai as genai
import markdown

# ==========================================
API_KEY = "AIzaSyBEPxyy7JbLF_l7-xIyMlNt6nYZvrKyxQU"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
# ==========================================

st.set_page_config(page_title="Siêu App Ra Đề", layout="wide")
st.title("📝 Siêu App Ra Đề (Chỉ ra đề theo chủ đề yêu cầu)")

col_mon, col_lop = st.columns(2)
with col_mon:
    mon_hoc = st.selectbox("📚 Môn học:", ["Toán học", "Tiếng Việt", "Tin học", "Lịch sử & Địa lý", "Khoa học"])
with col_lop:
    lop_hoc = st.selectbox("🏫 Khối lớp:", ["Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5"])

st.subheader("📥 Dán Ma Trận đã khống chế chủ đề")
ma_tran_pasted = st.text_area("Copy bảng ma trận (chỉ gồm các chủ đề bạn muốn) từ Word và dán vào đây:", height=250)

yeu_cau_them = st.text_input("Yêu cầu thêm (nếu có):", value="Câu hỏi tình huống sinh động, bám sát thực tế.")

if st.button(f"🚀 TẠO ĐỀ KIỂM TRA ĐÚNG CHỦ ĐỀ", type="primary"):
    if ma_tran_pasted.strip() == "":
        st.error("Cậu giáo hãy dán ma trận vào đã!")
    else:
        with st.spinner('AI đang sáng tác đề kiểm tra theo đúng chủ đề trong ma trận...'):
            prompt = f"""
            Bạn là giáo viên giỏi {mon_hoc} {lop_hoc}.
            Hãy soạn đề kiểm tra CHỈ DỰA TRÊN CÁC CHỦ ĐỀ có trong ma trận sau đây:
            {ma_tran_pasted}
            
            QUY ĐỊNH:
            1. Tuyệt đối không ra đề ngoài các chủ đề đã nêu trong ma trận.
            2. Số lượng câu TN/TL và mức độ phải khớp 100% với ma trận.
            3. {yeu_cau_them}
            4. Phải có ĐÁP ÁN CHI TIẾT ở cuối đề.
            """
            response = model.generate_content(prompt)
            st.markdown(response.text)
            html_text = markdown.markdown(response.text, extensions=['tables'])
            doc_file = f"<meta charset='utf-8'><body>{html_text}</body>"
            st.download_button("📥 TẢI FILE WORD ĐỀ KIỂM TRA", data=doc_file, file_name=f"De_Kiem_Tra_Chu_de_{mon_hoc}.doc", mime="application/msword")
