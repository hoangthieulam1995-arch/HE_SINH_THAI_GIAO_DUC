import streamlit as st
import google.generativeai as genai

# --- LẤY CHÌA KHÓA TỪ KÉT SẮT ---
try:
    API_KEY = st.secrets["MY_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Khởi tạo bộ não AI
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Chưa tìm thấy chìa khóa API. Vui lòng kiểm tra lại két sắt Secrets.")

# --- GIAO DIỆN TRANG CHỦ ---
st.set_page_config(page_title="Đạo Diễn Trò Chơi", page_icon="🎮", layout="wide")
st.title("🎮 Siêu App: Đạo Diễn Trò Chơi 4.0")
st.write("Biến mọi bài học khô khan thành một chuyến phiêu lưu kỳ thú!")
st.markdown("---")

# --- TẠO BỘ NHỚ TẠM THỜI (Để App chạy được 2 nhịp) ---
if "y_tuong" not in st.session_state:
    st.session_state.y_tuong = ""

# ======================================================
# NHỊP 1: TÌM KIẾM Ý TƯỞNG CỐT TRUYỆN
# ======================================================
st.header("1️⃣ Khởi tạo Ý tưởng")
col1, col2 = st.columns(2)

with col1:
    khoi_lop = st.selectbox("Chọn đối tượng học sinh:", 
                            ["Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5"], 
                            index=2) # Mặc định để Lớp 3
with col2:
    bai_hoc = st.text_input("Nhập bài học/chuẩn đầu ra:", 
                            placeholder="VD: Bảng cửu chương 3, Dấu ngoặc kép, Từ láy...")

if st.button("🪄 Gợi ý 3 Ý Tưởng Cốt Truyện"):
    if bai_hoc:
        with st.spinner("AI đang vắt óc sáng tạo cốt truyện..."):
            # Lệnh ngầm gửi cho AI
            lenh_goi_y = f"""
            Đóng vai một chuyên gia thiết kế trò chơi giáo dục tiểu học xuất sắc.
            Nhiệm vụ: Đề xuất 3 ý tưởng/cốt truyện trò chơi để dạy bài '{bai_hoc}' cho học sinh '{khoi_lop}'.
            Yêu cầu mỗi ý tưởng:
            - Có tên trò chơi thật lôi cuốn, dễ thương.
            - Nêu ngắn gọn bối cảnh/câu chuyện.
            - Phải có hoạt động kích thích tư duy tập thể và thi đấu đồng đội.
            - Phù hợp để thiết kế lên slide trình chiếu bằng máy chiếu lớp học.
            Trình bày rõ ràng thành 3 mục riêng biệt.
            """
            response = model.generate_content(lenh_goi_y)
            # Lưu kết quả vào bộ nhớ tạm
            st.session_state.y_tuong = response.text
            st.rerun() # Tải lại trang để hiện kết quả
    else:
        st.warning("Thầy/Cô vui lòng nhập tên bài học trước nhé!")

# Hiển thị kết quả của Nhịp 1
if st.session_state.y_tuong:
    st.success("Tén tèn! Đây là các ý tưởng dành cho Thầy/Cô:")
    st.markdown(st.session_state.y_tuong)

    # ======================================================
    # NHỊP 2: SẢN XUẤT KỊCH BẢN CHI TIẾT
    # ======================================================
    st.markdown("---")
    st.header("2️⃣ Sản xuất Kịch bản chi tiết")
    st.write("Thầy/Cô ưng ý tưởng số mấy ở trên? (Hoặc có thể tự gõ thêm yêu cầu riêng vào ô dưới)")
    lua_chon = st.text_area("Nhập ý tưởng Thầy/Cô chọn:", 
                            placeholder="VD: Tôi chọn ý tưởng số 2. Hãy thêm một vòng đối kháng...")

    if st.button("🎬 Viết Kịch Bản Toàn Tập"):
        if lua_chon:
            with st.spinner("Đang đạo diễn kịch bản, viết lời dẫn MC, thiết kế bộ câu hỏi..."):
                # Lệnh ngầm gửi cho AI
                lenh_kich_ban = f"""
                Dựa vào bài học '{bai_hoc}' cho '{khoi_lop}' và lựa chọn sau: '{lua_chon}'.
                Hãy viết một kịch bản trò chơi trên máy chiếu chi tiết từ A-Z.
                Cấu trúc kịch bản bắt buộc gồm:
                1. Lời dẫn dắt cực kỳ hấp dẫn của MC (có nhân vật dẫn chuyện hóa thân).
                2. Chia làm các vòng thi (ưu tiên vòng đối kháng). Mỗi vòng viết sẵn ít nhất 2 câu hỏi/thử thách ví dụ chi tiết.
                3. Đạo diễn âm thanh: Ghi chú rõ hiệu ứng âm thanh cần dùng (ví dụ: mở loa tiếng 'tinh tinh' khi trả lời đúng, tiếng nhạc hồi hộp).
                4. Gợi ý Hình ảnh: Viết 2 đoạn Prompt bằng tiếng Anh để giáo viên copy mang đi dùng AI tạo ảnh nền cho slide.
                """
                response_kb = model.generate_content(lenh_kich_ban)
                st.info("KỊCH BẢN HOÀN CHỈNH:")
                st.markdown(response_kb.text)
                st.balloons() # Thả bóng bay chúc mừng
        else:
            st.warning("Vui lòng nhập ý tưởng Thầy/Cô chọn vào ô trống nhé!")
