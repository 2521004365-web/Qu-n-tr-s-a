import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & GIAO DIỆN SÁNG TẠO
# ---------------------------------------------------------
st.set_page_config(
    page_title="MAMALALA - 32 Võ Văn Hát",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS giao diện Pastel & hiệu ứng cao cấp
st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&display=swap'); "
    "html, body, [class*='css'] { font-family: 'Quicksand', sans-serif; } "
    ".main-header { background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%); padding: 20px; border-radius: 20px; color: #D81B60; text-align: center; font-weight: 800; box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4); margin-bottom: 10px; } "
    ".sub-header { text-align: center; color: #666; font-weight: 600; margin-bottom: 25px; } "
    ".product-card { background: #FFFFFF; border-radius: 16px; padding: 18px; border: 2px solid #FFE4E8; box-shadow: 0 6px 12px rgba(255, 182, 193, 0.2); margin-bottom: 15px; } "
    ".fortune-box { background: linear-gradient(135deg, #a8edda 0%, #fed6e3 100%); border-radius: 15px; padding: 20px; text-align: center; font-weight: bold; color: #333; box-shadow: 0 4px 10px rgba(0,0,0,0.1); } "
    ".stButton>button { border-radius: 12px; font-weight: 700; background-color: #FF6B81; color: white; border: none; } "
    ".stButton>button:hover { background-color: #FF4757; color: white; } "
    "</style>",
    unsafe_allow_html=True
)

# Hiển thị banner ảnh (Tên file: IMG_4632.jpeg)
try:
    st.image("IMG_4632.jpeg", use_container_width=True)
except Exception:
    st.info("💡 Mẹo: Tải ảnh `IMG_4632.jpeg` lên kho GitHub để hiển thị Banner xinh xắn nhé!")

st.markdown("<div class='main-header'><h1>🧋 MAMALALA TEA & COFFEE</h1></div>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>📍 32 Võ Văn Hát, P. Long Trường, TP. Thủ Đức • Hotline: 0987.xxx.xxx</p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. CƠ SỞ DỮ LIỆU MENUS & TOPPING
# ---------------------------------------------------------
MENU_CATEGORIES = {
    "🧋 Trà Sữa Signatures": {
        "Trà Sữa Truyền Thống MAMALALA": {"price": 20000, "desc": "Vị đậm đà, béo ngậy chuẩn gu truyền thống", "tag": "🔥 Best Seller"},
        "Sữa Tươi Trân Châu Đường Đen": {"price": 35000, "desc": "Sữa tươi thanh trùng + trân châu đường đen dẻo thơm", "tag": "👑 Masterpiece"},
        "Matcha Freeze Uji Nhật Bản": {"price": 35000, "desc": "Trà xanh chuẩn Uji thơm thanh béo ngậy", "tag": "🌿 Healthy"},
        "Cacao Latte Macchiato": {"price": 35000, "desc": "Cacao nguyên chất phủ lớp kem cheese đậm đà", "tag": "🍫 Đậm vị"},
    },
    "🍓 Trà Trái Cây Tươi Mới": {
        "Trà Xanh Hoa Nhài Thanh Lương": {"price": 32000, "desc": "Thanh mát giải nhiệt, hương nhài tự nhiên 100%", "tag": "🌸 Fragrant"},
        "Trà Gạo Rang Genmaicha": {"price": 35000, "desc": "Hương gạo rang Genmaicha Nhật Bản thư thái", "tag": "⭐ Top Order"},
        "Sữa Dâu Sấy Thật Giòn Rụm": {"price": 38000, "desc": "Mứt dâu tươi kết hợp dâu sấy thăng hoa giòn rụm", "tag": "📸 Trending"},
        "Trà Dưa Lưới Nhiệt Đới": {"price": 32000, "desc": "Thức uống tươi mát mọng nước cho ngày nắng", "tag": "🍹 Tropical"},
    }
}

SIZE_OPTIONS = {
    "S (Vừa vặn - Năng lượng nhẹ)": 0,
    "M (Chuẩn gu - Uống cực đã)": 5000,
    "L (Khổng lồ - Thỏa mãn 100%)": 10000
}

TOPPING_OPTIONS = {
    "🧋 Trân châu đen dẻo dẻo": 5000,
    "💎 Trân châu trắng giòn sần sật": 7000,
    "🍧 Thạch trái cây nhiệt đới": 5000,
    "🍮 Pudding trứng béo ngậy": 8000,
    "🧀 Kem Cheese Macchiato đặc biệt": 10000
}

SUGAR_LEVELS = [
    "100% (Chuẩn vị ngọt thanh)",
    "70% (Nên thử - Vừa ngọt)",
    "50% (Ít ngọt)",
    "30% (Thanh nhẹ)",
    "0% (Không đường)"
]

ICE_LEVELS = [
    "100% (Đầy đủ đá)",
    "70% (Vừa đá)",
    "50% (Ít đá)",
    "30% (Sương sương)",
    "0% (Không đá)"
]

VOUCHER_CODES = {
    "THUDUC20": 20,
    "MAMALALA50": 50,
    "XINCHAO": 10
}

# Khởi tạo Session State
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "minigame_discount" not in st.session_state:
    st.session_state.minigame_discount = 0
if "promo_discount" not in st.session_state:
    st.session_state.promo_discount = 0

# ---------------------------------------------------------
# 3. SIDEBAR: TƯƠNG TÁC & MINIGAME & ĐỊA CHỈ
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/emoji/96/bubble-tea.png", width=70)
    st.title("🏡 MAMALALA Store")
    st.info("📍 **Địa chỉ:** 32 Võ Văn Hát, P. Long Trường, TP. Thủ Đức")
    st.text("⏰ Giờ mở cửa: 08:00 - 22:30")
    st.text("🛵 Ship nhanh Thủ Đức & lân cận")
    
    st.markdown("---")
    st.header("🎰 Vòng Quay May Mắn")
    if st.button("🎡 QUAY VOUCHER NGAY", use_container_width=True):
        prizes = [0, 5, 10, 15, 20, 50]
        weights = [20, 30, 25, 15, 8, 2]
        won = random.choices(prizes, weights=weights)[0]
        st.session_state.minigame_discount = won
        if won > 0:
            st.balloons()
            st.success(f"🎉 Trúng ngay Voucher **{won}%**!")
        else:
            st.info("😅 Chúc bạn may mắn lượt sau!")
            
    if st.session_state.minigame_discount > 0:
        st.caption(f"🎁 Voucher Minigame: **-{st.session_state.minigame_discount}%**")

    st.markdown("---")
    st.header("🎟️ Nhập Mã Giảm Giá")
    code_input = st.text_input("Mã khuyến mãi:", placeholder="Ví dụ: THUDUC20").strip().upper()
    if st.button("Áp dụng mã"):
        if code_input in VOUCHER_CODES:
            st.session_state.promo_discount = VOUCHER_CODES[code_input]
            st.success(f"Đã áp dụng mã {code_input}: Giảm {VOUCHER_CODES[code_input]}%")
        else:
            st.error("Mã không hợp lệ! Gợi ý: THUDUC20, MAMALALA50")

# ---------------------------------------------------------
# 4. TÁCH TABS CHỨC NĂNG SÁNG TẠO
# ---------------------------------------------------------
tab_order, tab_fortune, tab_cart, tab_feedback = st.tabs([
    "🍹 Đặt Đồ Uống", 
    "🔮 Quẻ Bói Đồ Uống", 
    "🛒 Giỏ Hàng & Thanh Toán",
    "⭐ Đánh Giá & Góp Ý"
])

# ==================== TAB 1: ĐẶT ĐỒ UỐNG ====================
with tab_order:
    col_left, col_right = st.columns([1.2, 0.8])
    
    with col_left:
        st.subheader("📝 Chọn Món & Tùy Chỉnh Chi Tiết")
        
        search_kw = st.text_input("🔍 Tìm kiếm đồ uống siêu tốc:", placeholder="Nhập tên món (Dâu, Matcha, Trà sữa...)")
        category_name = st.selectbox("📂 Chọn nhóm đồ uống:", list(MENU_CATEGORIES.keys()))
        current_menu = MENU_CATEGORIES[category_name]
        
        if search_kw:
            filtered_menu = {k: v for k, v in current_menu.items() if search_kw.lower() in k.lower()}
        else:
            filtered_menu = current_menu
            
        if not filtered_menu:
            st.warning("Không tìm thấy món phù hợp. Bạn thử tìm từ khóa khác xem sao nhé!")
        else:
            selected_tea = st.selectbox("☕ Chọn món uống:", list(filtered_menu.keys()))
            tea_info = filtered_menu[selected_tea]
            
            st.markdown(f"<div class='product-card'><h3 style='color:#D81B60; margin:0;'>{selected_tea} <span style='font-size:0.8rem; background:#FFD1DC; color:#D81B60; padding:3px 8px; border-radius:10px;'>{tea_info['tag']}</span></h3><p style='color:#555; margin-top:5px;'><i>{tea_info['desc']}</i></p><b style='color:#E91E63; font-size:1.1rem;'>Giá niêm yết: {tea_info['price']:,} VNĐ</b></div>", unsafe_allow_html=True)
            
            c_qty, c_size = st.columns([1, 2])
            with c_qty:
                quantity = st.number_input("Số lượng (Ly):", min_value=1, value=1, step=1)
            with c_size:
                selected_size = st.selectbox("Kích cỡ Size:", list(SIZE_OPTIONS.keys()))
                
            c_sugar, c_ice = st.columns(2)
            with c_sugar:
                selected_sugar = st.selectbox("Mức độ ngọt:", SUGAR_LEVELS)
            with c_ice:
                selected_ice = st.selectbox("Mức đá:", ICE_LEVELS)
                
            selected_toppings = st.multiselect("➕ Thêm Toppings:", options=list(TOPPING_OPTIONS.keys()))
            note = st.text_input("✍️ Ghi chú cho Barista pha chế:", placeholder="Ví dụ: Trà đậm, ít béo, giao giờ nghỉ trưa...")

            base_price = tea_info['price']
            size_price = SIZE_OPTIONS[selected_size]
            topping_price = sum(TOPPING_OPTIONS[t] for t in selected_toppings)
            unit_price = base_price + size_price + topping_price
            item_total = unit_price * quantity

            st.markdown(f"#### 💰 Tạm tính 1 ly: <span style='color:#D81B60'>{unit_price:,} VNĐ</span>", unsafe_allow_html=True)

            if st.button("➕ THÊM VÀO GIỎ HÀNG", type="primary", use_container_width=True):
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
                st.toast(f"Đã thêm {quantity}x {selected_tea} vào giỏ thành công!", icon="✨")

    with col_right:
        st.subheader("🛒 Giỏ Hàng Nhanh")
        if not st.session_state.cart:
            st.info("Giỏ hàng chưa có món nào. Chọn món ngay bên trái nha!")
        else:
            for idx, item in enumerate(st.session_state.cart, 1):
                st.markdown(f"**{idx}. {item['Tên món']}** (Size {item['Size']}) x{item['Số lượng']}")
                st.caption(f"Topping: {item['Topping']} | Ghi chú: {item['Ghi chú']}")
                st.markdown(f"👉 **{item['Thành tiền']:,} VNĐ**")
                st.markdown("---")
            total_temp = sum(i['Thành tiền'] for i in st.session_state.cart)
            st.markdown(f"### Tạm tính: <span style='color:#E91E63'>{total_temp:,} VNĐ</span>", unsafe_allow_html=True)

# ==================== TAB 2: QUẺ BÓI ĐỒ UỐNG ====================
with tab_fortune:
    st.subheader("🔮 Hôm nay bạn nên uống gì?")
    st.caption("Nếu đang phân vân không biết chọn gì, hãy để 'Vũ trụ MAMALALA' quyết định giúp bạn!")
    
    if st.button("✨ GIEO QUẺ ĐỒ UỐNG NGÂU NHIÊN", use_container_width=True):
        all_drinks = []
        for cat in MENU_CATEGORIES.values():
            all_drinks.extend(list(cat.keys()))
        picked = random.choice(all_drinks)
        
        quotes = [
            "Món này sẽ mang lại năng lượng siêu tích cực cho bạn hôm nay!",
            "Một sự lựa chọn hoàn hảo để xua tan mọi mệt mỏi!",
            "Uống món này vào là đẹp trai/xinh gái lên 300% liền!",
            "Vũ trụ bảo rằng hôm nay bạn rất hợp với vị ngọt ngào này!"
        ]
        
        st.markdown(f"<div class='fortune-box'><h2>🌟 Món quà từ vũ trụ:</h2><h1 style='color:#D81B60;'>{picked}</h1><p><i>\"{random.choice(quotes)}\"</i></p></div>", unsafe_allow_html=True)

# ==================== TAB 3: GIỎ HÀNG & THANH TOÁN ====================
with tab_cart:
    st.subheader("🛒 Chi Tiết Đơn Hàng & Thanh Toán")
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        customer_name = st.text_input("👤 Tên khách hàng / Người nhận:", placeholder="Ví dụ: Anh Minh, Chị Thư...")
        phone_num = st.text_input("📞 Số điện thoại liên hệ:", placeholder="Nhập SĐT để shop gọi xác nhận...")
    with col_info2:
        order_type = st.radio("🛵 Hình thức nhận hàng:", ["Uống tại quán (Nhập số bàn)", "Mang về (Take-away)", "Giao hàng tận nơi (Ship)"], horizontal=True)
        table_or_address = st.text_input("📍 Số bàn / Địa chỉ giao hàng:", placeholder="32 Võ Văn Hát hoặc Bàn 05...")
        
    if not st.session_state.cart:
        st.warning("Giỏ hàng của bạn đang trống!")
    else:
        df_cart = pd.DataFrame(st.session_state.cart)
        st.dataframe(
            df_cart[["Tên món", "Size", "Đường", "Đá", "Topping", "Ghi chú", "Số lượng", "Đơn giá", "Thành tiền"]],
            use_container_width=True,
            hide_index=True
        )
        
        if st.button("🗑️ Xóa sạch toàn bộ giỏ hàng"):
            st.session_state.cart = []
            st.session_state.invoice_paid = False
            st.rerun()
            
        total_price = df_cart["Thành tiền"].sum()
        total_discount = min(100, st.session_state.minigame_discount + st.session_state.promo_discount)
        final_price = int(total_price * (1 - total_discount / 100))
        
        st.markdown("---")
        st.markdown(f"### 💵 Tổng tiền món gốc: **{total_price:,} VNĐ**")
        if total_discount > 0:
            st.markdown(f"### 🎁 Ưu đãi áp dụng ({total_discount}%): <span style='color:green'>-{int(total_price * total_discount / 100):,} VNĐ</span>", unsafe_allow_html=True)
        st.markdown(f"## 💳 TỔNG THỰC THU: <span style='color:#D81B60'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)
        
        if st.button("✅ XÁC NHẬN THANH TOÁN & IN HÓA ĐƠN", type="primary", use_container_width=True):
            st.session_state.invoice_paid = True
            st.snow()

# ==================== TAB 4: ĐÁNH GIÁ & GÓP Ý ====================
with tab_feedback:
    st.subheader("⭐ Đánh Giá Chất Lượng Phục Vụ")
    rating = st.slider("Bạn cảm thấy trải nghiệm tại MAMALALA như thế nào?", 1, 5, 5)
    feedback_text = st.text_area("Lời nhắn gửi đến quán:", placeholder="Hãy cho MAMALALA biết cảm nhận của bạn nhé...")
    if st.button("📩 Gửi Phản Hồi"):
        st.balloons()
        st.success("Cảm ơn bạn rất nhiều! Phản hồi của bạn sẽ giúp MAMALALA hoàn thiện hơn mỗi ngày ❤️")

# ---------------------------------------------------------
# 5. XUẤT HÓA ĐƠN ĐẸP VÀ TẢI FILE TXT
# ---------------------------------------------------------
if st.session_state.get("invoice_paid") and st.session_state.cart:
    st.markdown("---")
    st.success("🎉 Đơn hàng đã thanh toán thành công! Dưới đây là Hóa đơn chi tiết:")
    
    invoice_box = st.container(border=True)
    with invoice_box:
        st.markdown("<h2 style='text-align: center; color: #D81B60; margin-bottom:0;'>🧋 MAMALALA TEA & COFFEE</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color:#777;'>📍 32 Võ Văn Hát, P. Long Trường, TP. Thủ Đức</p>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #333;'>HÓA ĐƠN BÁN HÀNG</h4>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**⏰ Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            st.write(f"**👤 Khách hàng:** {customer_name if customer_name else 'Khách vãng lai'}")
            st.write(f"**📞 SĐT:** {phone_num if phone_num else '-'}")
        with c2:
            st.write(f"**🛵 Hình thức:** {order_type}")
            st.write(f"**📍 Địa chỉ/Bàn:** {table_or_address if table_or_address else '-'}")
            
        st.markdown("---")
        st.table(pd.DataFrame(st.session_state.cart)[["Tên món", "Size", "Topping", "Số lượng", "Thành tiền"]])
        
        ca, cb = st.columns(2)
        with ca:
            st.write(f"**Tổng tiền hàng:** {total_price:,} VNĐ")
            st.write(f"**Giảm giá:** {total_discount}%")
        with cb:
            st.markdown(f"### THỰC THU: <span style='color:#D81B60'>{final_price:,} VNĐ</span>", unsafe_allow_html=True)
            
    # Chuẩn bị file tải về TXT
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    txt_content = f"{'='*45}\n   MAMALALA TEA & COFFEE STUDIO\n   32 Vo Van Hat, Long Truong, TP. Thu Duc\n{'='*45}\n"
    txt_content += f"Ngay: {now_str}\n"
    txt_content += f"Khach hang: {customer_name if customer_name else 'Khach vang lai'}\n"
    txt_content += f"SDT: {phone_num if phone_num else '-'}\n"
    txt_content += f"Hinh thuc: {order_type} ({table_or_address if table_or_address else '-'})\n"
    txt_content += f"{'-'*45}\n"
    for item in st.session_state.cart:
        txt_content += f"- {item['Tên món']} (Size {item['Size']}) x{item['Số lượng']}: {item['Thành tiền']:,} VND\n"
        if item['Topping'] != "Không":
            txt_content += f"  + Topping: {item['Topping']}\n"
    txt_content += f"{'-'*45}\nTiet kiem: {total_discount}%\nTONG THANH TOAN: {final_price:,} VND\n{'='*45}\nCam on & Hen gap lai quy khach!"

    st.download_button(
        label="📥 Tải hóa đơn file (.TXT)",
        data=txt_content,
        file_name=f"HoaDon_MAMALALA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )

```
