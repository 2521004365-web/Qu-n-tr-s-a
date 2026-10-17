import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & CƠ SỞ DỮ LIỆU SẢN PHẨM
# ---------------------------------------------------------
st.set_page_config(
    page_title="MAMALALA Tea & Coffee Studio",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS nâng cấp giao diện visual
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        color: #FF4B4B;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-header {
        text-align: center;
        color: #555;
        font-style: italic;
        margin-bottom: 20px;
    }
    .product-card {
        background-color: #FFF5F5;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #FFE0E0;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Hiển thị banner ảnh (Khắc phục lỗi thiếu file với try...except)
try:
    st.image("IMG_4632.jpeg", use_container_width=True)
except Exception:
    st.info("💡 Tip: Tải ảnh banner `IMG_4632.jpeg` lên GitHub để hiển thị ảnh bìa quán!")

st.markdown("<h1 class='main-header'>🧋 MAMALALA TEA & COFFEE STUDIO</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Thương hiệu trà sữa chuẩn vị - Đậm gu giới trẻ ✨</p>", unsafe_allow_html=True)

# Danh sách menu chia theo danh mục
MENU_CATEGORIES = {
    "🧋 Trà Sữa Truyền Thống": {
        "Trà Sữa Truyền Thống": {"price": 20000, "desc": "Vị đậm đà, béo ngậy chuẩn gu truyền thống", "best": True},
        "Sữa Tươi Trân Châu Đường Đen": {"price": 35000, "desc": "Sữa tươi thanh trùng kết hợp trân châu nấu đường đen dẻo thơm", "best": True},
        "Matcha Freeze Latte": {"price": 35000, "desc": "Trà xanh Uji Nhật Bản béo ngậy thơm nức", "best": False},
        "Cacao Latte Đเข้ม": {"price": 35000, "desc": "Cacao nguyên chất đậm đà phủ lớp kem béo", "best": False},
    },
    "🍓 Trà Trái Cây Đổi Vị": {
        "Trà Xanh Hoa Nhài": {"price": 32000, "desc": "Thanh mát giải nhiệt, hương nhài tự nhiên", "best": False},
        "Trà Gạo Rang Nhật Bản": {"price": 35000, "desc": "Hương gạo rang Genmaicha thơm lừng dễ chịu", "best": True},
        "Sữa Dâu Sấy Thật": {"price": 38000, "desc": "Mứt dâu tươi cùng dâu sấy giòn béo thơm ngọt", "best": True},
        "Trà Dưa Lưới Nhiệt Đới": {"price": 32000, "desc": "Thức uống tươi mát đậm đà hương dưa lưới", "best": False},
    }
}

SIZE_OPTIONS = {
    "S (Nhỏ - Vừa đủ)": 0,
    "M (Lớn - Chuẩn gu)": 5000,
    "L (Đặc biệt - Siêu nhiều)": 10000
}

TOPPING_OPTIONS = {
    "🧋 Trân châu đen dẻo": 5000,
    "💎 Trân châu trắng giòn": 7000,
    "🍧 Thạch trái cây nhiệt đới": 5000,
    "🍮 Pudding trứng béo ngậy": 8000,
    "🧀 Kem Cheese Macchiato": 10000
}

SUGAR_LEVELS = ["100% (Chuẩn vị)", "70% (Vừa ngọt)", "50% (Ít ngọt)", "30% (Thanh nhẹ)", "0% (Không đường)"]
ICE_LEVELS = ["100% (Đầy đủ)", "70% (Vừa đá)", "50% (Ít đá)", "30% (Sương sương)", "0% (Không đá)"]

# Khởi tạo state
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "discount_code" not in st.session_state:
    st.session_state.discount_code = 0

# ---------------------------------------------------------
# 2. THANH BÊN (SIDEBAR) & MINIGAME SÁNG TẠO
# ---------------------------------------------------------
with st.sidebar:
    st.header("🎁 Vòng Quay May Mắn")
    st.caption("Quay ngay để nhận Voucher giảm giá trực tiếp!")
    
    if st.button("🎰 THỬ VẬN MAY", use_container_width=True):
        prizes = [0, 5, 10, 15, 20, 50]
        weights = [30, 30, 20, 10, 8, 2] # Tỷ lệ %
        won = random.choices(prizes, weights=weights)[0]
        st.session_state.discount_code = won
        if won > 0:
            st.balloons()
            st.success(f"🎉 Chúc mừng! Bạn quay trúng Voucher giảm **{won}%**!")
        else:
            st.info("😅 Chúc bạn may mắn lần sau nhé!")
            
    if st.session_state.discount_code > 0:
        st.warning(f"🏷️ Voucher đang áp dụng: **-{st.session_state.discount_code}%**")
        
    st.markdown("---")
    st.markdown("### 📞 Thông tin hỗ trợ")
    st.text("📍 Đ/c: 123 Đường Trà Sữa, Q.1")
    st.text("⏰ Mở cửa: 08:00 - 22:30")
    st.text("☎️ Hotline: 1900 xxxx")

# ---------------------------------------------------------
# 3. TÁCH TÍNH NĂNG THEO TABS
# ---------------------------------------------------------
tab_order, tab_bestseller, tab_history = st.tabs(["🍹 Đặt Đồ Uống", "🔥 Best Seller / Gợi Ý", "📋 Giỏ Hàng & Thanh Toán"])

# ==================== TAB 1: ĐẶT ĐỒ UỐNG ====================
with tab_order:
    col_left, col_right = st.columns([1.2, 0.8])
    
    with col_left:
        st.subheader("📝 Chọn Món & Tùy Chỉnh")
        
        # Tìm kiếm & Lọc
        search_kw = st.text_input("🔍 Tìm nhanh đồ uống:", placeholder="Nhập tên món (ví dụ: Trà sữa, Dâu, Matcha...)")
        
        # Chọn danh mục
        category_name = st.selectbox("📂 Chọn nhóm đồ uống:", list(MENU_CATEGORIES.keys()))
        current_menu = MENU_CATEGORIES[category_name]
        
        # Lọc món theo tìm kiếm
        if search_kw:
            filtered_menu = {k: v for k, v in current_menu.items() if search_kw.lower() in k.lower()}
        else:
            filtered_menu = current_menu
            
        if not filtered_menu:
            st.info("Không tìm thấy món phù hợp với từ khóa.")
        else:
            selected_tea = st.selectbox("☕ Chọn món:", list(filtered_menu.keys()))
            tea_info = filtered_menu[selected_tea]
            
            # Hiển thị mô tả món
            st.markdown(f"""
            <div class='product-card'>
                <b>{selected_tea}</b> {'🔥 (Best Seller)' if tea_info['best'] else ''}<br/>
                <i>{tea_info['desc']}</i><br/>
                <span style='color:#FF4B4B; font-weight:bold;'>Giá gốc: {tea_info['price']:,} VNĐ</span>
            </div>
            """, unsafe_allow_html=True)
            
            c_qty, c_size = st.columns([1, 2])
            with c_qty:
                quantity = st.number_input("Số lượng:", min_value=1, value=1, step=1)
            with c_size:
                selected_size = st.selectbox("Kích cỡ (Size):", list(SIZE_OPTIONS.keys()))
                
            c_sugar, c_ice = st.columns(2)
            with c_sugar:
                selected_sugar = st.selectbox("Mức đường:", SUGAR_LEVELS)
            with c_ice:
                selected_ice = st.selectbox("Mức đá:", ICE_LEVELS)
                
            selected_toppings = st.multiselect(
                "➕ Thêm Topping (Tùy chọn):",
                options=list(TOPPING_OPTIONS.keys())
            )
            
            note = st.text_input("✍️ Ghi chú cho Barista:", placeholder="Ví dụ: Lấy nhiều ống hút, trà đậm...")

            # Tính tiền
            base_price = tea_info['price']
            size_price = SIZE_OPTIONS[selected_size]
            topping_price = sum(TOPPING_OPTIONS[t] for t in selected_toppings)
            unit_price = base_price + size_price + topping_price
            item_total = unit_price * quantity

            st.markdown(f"#### 💰 Đơn giá 1 ly: <span style='color:red'>{unit_price:,} VNĐ</span>", unsafe_allow_html=True)

            if st.button("➕ Thêm vào giỏ hàng", type="primary", use_container_width=True):
                topping_str = ", ".join([t.split()[1] if len(t.split())>1 else t for t in selected_toppings]) if selected_toppings else "Không"
                item_data = {
                    "Tên món": selected_tea,
                    "Size": selected_size.split()[0],
                    "Đường": selected_sugar.split()[0],
                    "Đá": selected_ice.split()[0],
                    "Topping": topping_str,
                    "Ghi chú": note if note else "-",
                    "Đơn giá": unit_price,
                    "Số lượng": quantity,
                    "Thành tiền": item_total
                }
                st.session_state.cart.append(item_data)
                st.session_state.invoice_paid = False
                st.toast(f"Đã thêm {quantity}x {selected_tea} vào giỏ!", icon="✅")

    with col_right:
        st.subheader("🛒 Xem Nhanh Giỏ Hàng")
        if not st.session_state.cart:
            st.info("Giỏ hàng của bạn đang trống.")
        else:
            for idx, item in enumerate(st.session_state.cart, 1):
                st.markdown(f"**{idx}. {item['Tên món']}** (Size {item['Size']}) x{item['Số lượng']}")
                st.caption(f"Đường: {item['Đường']} | Đá: {item['Đá']} | Topping: {item['Topping']}")
                st.markdown(f"➡️ **{item['Thành tiền']:,} VNĐ**")
                st.markdown("---")
            total_temp = sum(i['Thành tiền'] for i in st.session_state.cart)
            st.markdown(f"### Tạm tính: <span style='color:red'>{total_temp:,} VNĐ</span>", unsafe_allow_html=True)

# ==================== TAB 2: BEST SELLER ====================
with tab_bestseller:
    st.subheader("🔥 Top Sản Phẩm Đợt Tốt Nhất Tại MAMALALA")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='product-card'>
            <h3>🧋 Sữa Tươi Trân Châu Đường Đen</h3>
            <p>Trân châu nấu thủ công bằng đường đen Hàn Quốc đun liên tục 4 tiếng, tạo độ dẻo mềm quện cùng sữa tươi thanh trùng béo nhẹ.</p>
            <b>⭐ Đánh giá: 4.9/5 (500+ lượt chọn)</b>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class='product-card'>
            <h3>🍓 Sữa Dâu Sấy Thật</h3>
            <p>Sự kết hợp giữa sốt dâu tằm tươi chua ngọt và lớp dâu sấy thăng hoa giòn rụm bên trên. Món 'ruột' của các tín đồ chụp ảnh!</p>
            <b>⭐ Đánh giá: 4.8/5 (350+ lượt chọn)</b>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 3: GIỎ HÀNG & THANH TOÁN ====================
with tab_history:
    st.subheader("🛒 Chi Tiết Đơn Hàng & Xuất Hóa Đơn")
    
    customer_name = st.text_input("👤 Tên người nhận / Tên bàn:", placeholder="Nhập tên của bạn hoặc số bàn...")
    
    if not st.session_state.cart:
        st.warning("Chưa có sản phẩm nào trong giỏ hàng. Hãy qua tab '🍹 Đặt Đồ Uống' để chọn món!")
    else:
        df_cart = pd.DataFrame(st.session_state.cart)
        st.dataframe(
            df_cart[["Tên món", "Size", "Đường", "Đá", "Topping", "Ghi chú", "Số lượng", "Đơn giá", "Thành tiền"]],
            use_container_width=True,
            hide_index=True
        )
        
        c_btn1, c_btn2 = st.columns([1, 1])
        with c_btn1:
            if st.button("🗑️ Xóa sạch giỏ hàng", use_container_width=True):
                st.session_state.cart = []
                st.session_state.invoice_paid = False
                st.rerun()
                
        # Tính toán thanh toán
        total_price = df_cart["Thành tiền"].sum()
        
        # Áp dụng giảm giá
        discount_percent = st.session_state.discount_code
        manual_discount = st.number_input("🎟️ Nhập % giảm giá bổ sung (nếu có):", min_value=0, max_value=100, value=0, step=5)
        final_discount = min(100, discount_percent + manual_discount)
        
        final_price = int(total_price * (1 - final_discount / 100))
        
        st.markdown("---")
        st.markdown(f"### 💵 Tổng tiền hàng: **{total_price:,} VNĐ**")
        if final_discount > 0:
            st.markdown(f"### 🎁 Giảm giá ({final_discount}%): <span style='color:green'>-{int(total_price * final_discount / 100):,} VNĐ</span>", unsafe_allow_html=True)
        st.markdown(f"## 💳 TỔNG THANH TOÁN: <span style='color:red'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)
        
        if st.button("✅ XÁC NHẬN THANH TOÁN", type="primary", use_container_width=True):
            st.session_state.invoice_paid = True
            st.balloons()

# ---------------------------------------------------------
# 4. TẠO & XUẤT HÓA ĐƠN ĐẸP MẮT
# ---------------------------------------------------------
if st.session_state.get("invoice_paid") and st.session_state.cart:
    st.markdown("---")
    st.success("🎉 Thanh toán thành công! Dưới đây là phiếu hóa đơn của bạn:")
    
    invoice_box = st.container(border=True)
    with invoice_box:
        st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>🧋 MAMALALA TEA & COFFEE</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>HÓA ĐƠN BÁN HÀNG</p>", unsafe_allow_html=True)
        st.write(f"**⏰ Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        st.write(f"**👤 Khách hàng:** {customer_name if customer_name else 'Khách vãng lai'}")
        st.markdown("---")
        
        st.table(pd.DataFrame(st.session_state.cart)[["Tên món", "Size", "Topping", "Số lượng", "Thành tiền"]])
        
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Tổng tiền:** {total_price:,} VNĐ")
            st.write(f"**Ưu đãi:** {final_discount}%")
        with c2:
            st.markdown(f"### THỰC THU: <span style='color:red'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)
            
    # Tải file hóa đơn TXT
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    txt_content = f"{'='*40}\n   MAMALALA TEA & COFFEE - HOA DON\n{'='*40}\n"
    txt_content += f"Ngay: {now_str}\nKhach hang: {customer_name if customer_name else 'Khach vang lai'}\n{'-'*40}\n"
    for item in st.session_state.cart:
        txt_content += f"- {item['Tên món']} ({item['Size']}) x{item['Số lượng']}: {item['Thành tiền']:,} VND\n"
    txt_content += f"{'-'*40}\nTiet kiem: {final_discount}%\nTONG THANH TOAN: {final_price:,} VND\n{'='*40}\nCam on quy khach!"

    st.download_button(
        label="📥 Tải hóa đơn file (.TXT)",
        data=txt_content,
        file_name=f"HoaDon_MAMALALA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )
