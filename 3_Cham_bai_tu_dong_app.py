import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
API_KEY = "AIzaSyCNot2QXsBZyU21n5itZiCcQCw0mCp1xRw"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')
# ==========================================

st.set_page_config(page_title="Siêu Trợ Lý Chấm Bài", layout="wide")
st.title("💯 Siêu Trợ Lý Chấm Bài (Bản Kỷ Luật Thép)")

col_mon, col_lop = st.columns(2)
with col_mon:
    mon_hoc = st.selectbox("📚 Môn học:", ["Toán học", "Tiếng Việt", "Tin học", "Lịch sử & Địa lý", "Khoa học"])
with col_lop:
    lop_hoc = st.selectbox("🏫 Khối lớp:", ["Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5"])

st.subheader("1. Nạp Đáp Án")
dap_an = st.text_area("Dán Hướng dẫn chấm/Đáp án vào đây:", height=150)

st.markdown("---")

st.subheader("2. Soi bài kiểm tra (Khung hình siêu to)")
st.info("💡 MẸO SƯ PHẠM: Hãy XOAY NGANG TỜ GIẤY A4 ra cho vừa khít màn hình nhé!")
anh_chup = st.camera_input("📸 Camera Máy Tính (Bấm nút Take Photo để chụp)")

st.markdown("---")

if st.button(f"🔎 BẮT ĐẦU CHẤM BÀI NÀY", type="primary"):
    if dap_an.strip() == "":
        st.error("⚠️ Thầy/Cô chưa dán Đáp án kìa!")
    elif anh_chup is None:
        st.error("⚠️ Thầy/Cô chưa bấm chụp ảnh bài làm ở khung Camera!")
    else:
        image = Image.open(anh_chup)
        
        with st.spinner('AI đang kiểm tra tính hợp lệ của bài thi...'):
            # LỆNH MỚI: BẮT AI KIỂM TRA ẢNH TRƯỚC VÀ KHÔNG ĐƯỢC BỊA CHUYỆN
            prompt = f"""
            Bạn là một giáo viên Tiểu học chấm thi môn {mon_hoc} lớp {lop_hoc} cực kỳ tận tâm, tinh mắt và TRUNG THỰC TỐI ĐA.
            
            BƯỚC 1: KIỂM TRA TÍNH HỢP LỆ (QUAN TRỌNG NHẤT)
            Hãy nhìn thật kỹ vào hình ảnh bài làm. 
            Nếu nội dung trong ảnh KHÔNG PHẢI là môn {mon_hoc} (ví dụ: yêu cầu chấm Toán nhưng ảnh lại là bài văn, bài tiếng Anh, hoặc không có số liệu Toán học), HÃY DỪNG LẠI NGAY LẬP TỨC. 
            Bạn chỉ được phép trả lời một câu duy nhất: "🚨 CẢNH BÁO: Hình ảnh tải lên không khớp với môn {mon_hoc}. Trợ lý từ chối chấm bài này để đảm bảo tính chính xác!" và KHÔNG LÀM THÊM BƯỚC NÀO NỮA.
            Tuyệt đối không được tưởng tượng hay bịa ra kết quả tính toán nếu trong ảnh không có.

            BƯỚC 2: CHẤM BÀI (Chỉ thực hiện nếu ảnh đúng là môn {mon_hoc})
            Nếu ảnh đúng môn học, hãy đối chiếu chữ viết tay với ĐÁP ÁN CHUẨN:
            [ĐÁP ÁN CHUẨN]:
            {dap_an}
            
            HÃY TRÌNH BÀY BẢNG KẾT QUẢ THEO 3 PHẦN:
            1. BÀI LÀM CỦA HỌC SINH: Trích xuất chính xác những gì học sinh đã viết (để Thầy/Cô kiểm chứng AI đọc đúng không).
            2. PHÂN TÍCH VÀ CHẤM ĐIỂM: Chỉ ra câu đúng/sai dựa vào đáp án. Căn cứ thang điểm, chấm tổng trên 10.
            3. LỜI PHÊ: Dùng giọng điệu sư phạm.
            """
            
            response = model.generate_content([prompt, image])
            
            if "CẢNH BÁO" in response.text:
                st.error("🚨 PHÁT HIỆN LỖI: BÀI LÀM KHÔNG KHỚP MÔN HỌC!")
                st.markdown(response.text)
            else:
                st.success("🎉 Đã chấm xong! Kết quả chi tiết:")
                st.markdown(response.text)
