import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & GIAO DIỆN CAO CẤP
# ---------------------------------------------------------
st.set_page_config(
    page_title="MAMALALA - Hệ Thống F&B Thông Minh",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&display=swap'); "
    "html, body, [class*='css'] { font-family: 'Quicksand', sans-serif; } "
    ".main-header { background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%); padding: 25px; border-radius: 20px; color: #D81B60; text-align: center; font-weight: 800; box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4); margin-bottom: 10px; } "
    ".sub-header { text-align: center; color: #555; font-weight: 600; margin-bottom: 25px; } "
    ".product-card { background: #FFFFFF; border-radius: 16px; padding: 18px; border: 2px solid #FFE4E8; box-shadow: 0 6px 12px rgba(255, 182, 193, 0.2); margin-bottom: 15px; } "
    ".fortune-box { background: linear-gradient(135deg, #a8edda 0%, #fed6e3 100%); border-radius: 15px; padding: 20px; text-align: center; font-weight: bold; color: #333; box-shadow: 0 4px 10px rgba(0,0,0,0.1); } "
    ".stButton>button { border-radius: 12px; font-weight: 700; background-color: #FF6B81; color: white; border: none; } "
    ".stButton>button:hover { background-color: #FF4757; color: white; } "
    "</style>",
    unsafe_allow_html=True
)

# Hiển thị banner ảnh an toàn
try:
    st.image("IMG_4632.jpeg", use_container_width=True)
except Exception:
    st.info("💡 Mẹo: Tải ảnh `IMG_4632.jpeg` lên kho GitHub để hiển thị Banner xinh xắn nhé!")

st.markdown("<div class='main-header'><h1>🧋 MAMALALA TEA & COFFEE STUDIO</h1></div>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>📍 32 Võ Văn Hát, P. Long Trường, TP. Thủ Đức • ☎️ Hotline: 0987.xxx.xxx</p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. KHỞI TẠO SESSION STATE TOÀN HỆ THỐNG
# ---------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []
if "orders_db" not in st.session_state:
    st.session_state.orders_db = []  # Lưu lịch sử tất cả đơn hàng để làm báo cáo
if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = [
        {"name": "Minh Thư", "rating": 5, "comment": "Trà sữa đậm vị, trân châu dẻo ngon xuất sắc!", "date": "17/10/2026"},
        {"name": "Gia Hân", "rating": 5, "comment": "Quán xinh, nhân viên phục vụ nhiệt tình nha.", "date": "16/10/2026"}
    ]
if "minigame_discount" not in st.session_state:
    st.session_state.minigame_discount = 0
if "promo_discount" not in st.session_state:
    st.session_state.promo_discount = 0

# ---------------------------------------------------------
# 3. DỮ LIỆU SẢN PHẨM & TÙY CHỌN
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

SIZE_OPTIONS = {"S (Vừa vặn - Năng lượng nhẹ)": 0, "M (Chuẩn gu - Uống cực đã)": 5000, "L (Khổng lồ - Thỏa mãn 100%)": 10000}
TOPPING_OPTIONS = {"🧋 Trân châu đen dẻo": 5000, "💎 Trân châu trắng giòn": 7000, "🍧 Thạch trái cây": 5000, "🍮 Pudding trứng": 8000, "🧀 Kem Cheese Macchiato": 10000}
SUGAR_LEVELS = ["100% (Chuẩn vị)", "70% (Vừa ngọt)", "50% (Ít ngọt)", "30% (Thanh nhẹ)", "0% (Không đường)"]
ICE_LEVELS = ["100% (Đầy đủ đá)", "70% (Vừa đá)", "50% (Ít đá)", "30% (Sương sương)", "0% (Không đá)"]
VOUCHER_CODES = {"THUDUC20": 20, "MAMALALA50": 50, "XINCHAO": 10}

# ---------------------------------------------------------
# 4. THANH SIDEBAR: MINIGAME & TIỆN ÍCH
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/emoji/96/bubble-tea.png", width=70)
    st.title("🏡 MAMALALA Hub")
    st.info("📍 **Địa chỉ:** 32 Võ Văn Hát, P. Long Trường, TP. Thủ Đức")
    st.text("⏰ Mở cửa: 08:00 - 22:30")
    
    st.markdown("---")
    st.header("🎰 Vòng Quay May Mắn")
    if st.button("🎡 QUAY NHẬN VOUCHER", use_container_width=True):
        won = random.choices([0, 5, 10, 15, 20, 50], weights=[20, 30, 25, 15, 8, 2])[0]
        st.session_state.minigame_discount = won
        if won > 0:
            st.balloons()
            st.success(f"🎉 Trúng Voucher **{won}%**!")
        else:
            st.info("😅 Chúc bạn may mắn lần sau!")
            
    if st.session_state.minigame_discount > 0:
        st.caption(f"🎁 Đã lưu Voucher: **-{st.session_state.minigame_discount}%**")

    st.markdown("---")
    st.header("🎟️ Nhập Mã Ưu Đãi")
    code_input = st.text_input("Mã giảm giá:", placeholder="Ví dụ: THUDUC20").strip().upper()
    if st.button("Áp dụng mã"):
        if code_input in VOUCHER_CODES:
            st.session_state.promo_discount = VOUCHER_CODES[code_input]
            st.success(f"Áp dụng thành công mã {code_input} (-{VOUCHER_CODES[code_input]}%)")
        else:
            st.error("Mã không tồn tại hoặc đã hết hạn!")

# ---------------------------------------------------------
# 5. HỆ THỐNG TABS ĐIỀU HƯỚNG CHÍNH
# ---------------------------------------------------------
tab_order, tab_fortune, tab_cart, tab_tracking, tab_review, tab_admin = st.tabs([
    "🍹 Đặt Món", 
    "🔮 Quẻ Bói", 
    "🛒 Giỏ Hàng", 
    "📦 Theo Dõi Đơn",
    "⭐ Đánh Giá",
    "📊 Quản Trị (Admin)"
])

# ==================== TAB 1: ĐẶT MÓN ====================
with tab_order:
    c_left, c_right = st.columns([1.2, 0.8])
    with c_left:
        st.subheader("📝 Menu & Tùy Chỉnh Ly Nước")
        search_kw = st.text_input("🔍 Tìm kiếm nhanh đồ uống:", placeholder="Nhập tên món...")
        category_name = st.selectbox("📂 Danh mục:", list(MENU_CATEGORIES.keys()))
        current_menu = MENU_CATEGORIES[category_name]
        
        filtered = {k: v for k, v in current_menu.items() if search_kw.lower() in k.lower()} if search_kw else current_menu
        
        if not filtered:
            st.warning("Không tìm thấy món phù hợp.")
        else:
            selected_tea = st.selectbox("☕ Chọn món:", list(filtered.keys()))
            info = filtered[selected_tea]
            
            st.markdown(f"<div class='product-card'><h3 style='color:#D81B60; margin:0;'>{selected_tea} <span style='font-size:0.8rem; background:#FFD1DC; color:#D81B60; padding:3px 8px; border-radius:10px;'>{info['tag']}</span></h3><p style='color:#555; margin-top:5px;'><i>{info['desc']}</i></p><b style='color:#E91E63; font-size:1.1rem;'>Giá gốc: {info['price']:,} VNĐ</b></div>", unsafe_allow_html=True)
            
            q1, q2 = st.columns([1, 2])
            with q1:
                qty = st.number_input("Số lượng:", min_value=1, value=1, step=1)
            with q2:
                sz = st.selectbox("Size:", list(SIZE_OPTIONS.keys()))
                
            s1, s2 = st.columns(2)
            with s1:
                sugar = st.selectbox("Đường:", SUGAR_LEVELS)
            with s2:
                ice = st.selectbox("Đá:", ICE_LEVELS)
                
            toppings = st.multiselect("➕ Topping thêm:", options=list(TOPPING_OPTIONS.keys()))
            note = st.text_input("✍️ Ghi chú cho Barista:", placeholder="Ví dụ: Ít đá, nhiều trân châu...")

            unit_price = info['price'] + SIZE_OPTIONS[sz] + sum(TOPPING_OPTIONS[t] for t in toppings)
            item_total = unit_price * qty
            st.markdown(f"#### 💰 Thành tiền 1 phần: <span style='color:#D81B60'>{unit_price:,} VNĐ</span>", unsafe_allow_html=True)

            if st.button("➕ THÊM VÀO GIỎ HÀNG", type="primary", use_container_width=True):
                top_str = ", ".join([t.split()[1] if len(t.split())>1 else t for t in toppings]) if toppings else "Không"
                st.session_state.cart.append({
                    "Tên món": selected_tea, "Size": sz.split()[0], "Đường": sugar.split()[0],
                    "Đá": ice.split()[0], "Topping": top_str, "Ghi chú": note or "-",
                    "Đơn giá": unit_price, "Số lượng": qty, "Thành tiền": item_total
                })
                st.toast(f"Đã thêm {qty}x {selected_tea} vào giỏ!", icon="✨")

    with c_right:
        st.subheader("🛒 Giỏ Hàng Nhanh")
        if not st.session_state.cart:
            st.info("Giỏ hàng đang trống.")
        else:
            for i, itm in enumerate(st.session_state.cart, 1):
                st.markdown(f"**{i}. {itm['Tên món']}** (Size {itm['Size']}) x{itm['Số lượng']}")
                st.caption(f"Topping: {itm['Topping']} | Ghi chú: {itm['Ghi chú']}")
                st.markdown(f"👉 **{itm['Thành tiền']:,} VNĐ**")
                st.markdown("---")
            st.markdown(f"### Tạm tính: <span style='color:#E91E63'>{sum(x['Thành tiền'] for x in st.session_state.cart):,} VNĐ</span>", unsafe_allow_html=True)

# ==================== TAB 2: QUẺ BÓI ====================
with tab_fortune:
    st.subheader("🔮 Hôm nay bạn nên uống gì?")
    if st.button("✨ GIEO QUẺ NGẪU NHIÊN", use_container_width=True):
        all_d = []
        for cat in MENU_CATEGORIES.values():
            all_d.extend(list(cat.keys()))
        picked = random.choice(all_d)
        st.markdown(f"<div class='fortune-box'><h2>🌟 Món vũ trụ chọn cho bạn:</h2><h1 style='color:#D81B60;'>{picked}</h1><p><i>'Uống món này năng lượng tràn trề cả ngày!'</i></p></div>", unsafe_allow_html=True)

# ==================== TAB 3: GIỎ HÀNG & THANH TOÁN ====================
with tab_cart:
    st.subheader("🛒 Thanh Toán Đơn Hàng")
    c_info1, c_info2 = st.columns(2)
    with c_info1:
        c_name = st.text_input("👤 Tên khách hàng:", placeholder="Nhập tên của bạn...")
        c_phone = st.text_input("📞 Số điện thoại:", placeholder="Nhập SĐT nhận hàng...")
    with c_info2:
        o_type = st.radio("🛵 Hình thức:", ["Tại quán", "Mang đi", "Giao hàng tận nơi"], horizontal=True)
        address_table = st.text_input("📍 Số bàn / Địa chỉ:", placeholder="Bàn số mấy hoặc địa chỉ nhà...")
        
    if not st.session_state.cart:
        st.warning("Chưa có món nào trong giỏ hàng.")
    else:
        df_c = pd.DataFrame(st.session_state.cart)
        st.dataframe(df_c[["Tên món", "Size", "Đường", "Đá", "Topping", "Số lượng", "Thành tiền"]], use_container_width=True, hide_index=True)
        
        if st.button("🗑️ Xóa toàn bộ giỏ hàng"):
            st.session_state.cart = []
            st.rerun()
            
        t_price = df_c["Thành tiền"].sum()
        total_disc = min(100, st.session_state.minigame_discount + st.session_state.promo_discount)
        final_p = int(t_price * (1 - total_disc / 100))
        
        st.markdown("---")
        st.markdown(f"### 💵 Tổng tiền gốc: **{t_price:,} VNĐ**")
        if total_disc > 0:
            st.markdown(f"### 🎁 Giảm giá tổng ({total_disc}%): <span style='color:green'>-{int(t_price * total_disc / 100):,} VNĐ</span>", unsafe_allow_html=True)
        st.markdown(f"## 💳 THANH TOÁN: <span style='color:#D81B60'>{final_p:,} VNĐ</span>", unsafe_allow_html=True)
        
        if st.button("✅ XÁC NHẬN ĐẶT HÀNG", type="primary", use_container_width=True):
            order_id = f"MAMA{random.randint(1000, 9999)}"
            new_order = {
                "Mã đơn": order_id, "Khách hàng": c_name or "Khách lẻ", "SĐT": c_phone or "-",
                "Hình thức": o_type, "Địa chỉ/Bàn": address_table or "-", "Chi tiết giỏ": st.session_state.cart.copy(),
                "Tổng tiền": final_p, "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Trạng thái": "Đang pha chế ☕"
            }
            st.session_state.orders_db.append(new_order)
            st.session_state.cart = []
            st.snow()
            st.success(f"🎉 Đặt hàng thành công! Mã đơn của bạn là: **{order_id}**")

# ==================== TAB 4: THEO DÕI ĐƠN HÀNG ====================
with tab_tracking:
    st.subheader("📦 Tra Cứu Trạng Thái Đơn Hàng")
    search_id = st.text_input("Nhập mã đơn hàng (Ví dụ: MAMA1234):").strip().upper()
    if search_id:
        found = [o for o in st.session_state.orders_db if o["Mã đơn"] == search_id]
        if found:
            ord_item = found[0]
            st.info(f"📋 **Mã đơn:** {ord_item['Mã đơn']} | **Khách:** {ord_item['Khách hàng']}")
            st.success(f"🔄 **Trạng thái hiện tại:** {ord_item['Trạng thái']}")
            st.write(f"⏰ Thời gian đặt: {ord_item['Thời gian']}")
            st.write(f"💵 Tổng tiền thanh toán: **{ord_item['Tổng tiền']:,} VNĐ**")
        else:
            st.error("Không tìm thấy mã đơn hàng này!")

# ==================== TAB 5: ĐÁNH GIÁ ====================
with tab_review:
    st.subheader("⭐ Khách Hàng Nói Gì Về MAMALALA")
    for fb in st.session_state.feedbacks:
        st.markdown(f"**{fb['name']}** - {'⭐' * fb['rating']} ({fb['date']})")
        st.write(f"💬 \"{fb['comment']}\"")
        st.markdown("---")
        
    st.markdown("### Gửi đánh giá của bạn:")
    fb_name = st.text_input("Tên của bạn:")
    fb_rate = st.slider("Số sao:", 1, 5, 5)
    fb_cmt = st.text_area("Cảm nhận của bạn:")
    if st.button("Gửi đánh giá"):
        if fb_name and fb_cmt:
            st.session_state.feedbacks.insert(0, {"name": fb_name, "rating": fb_rate, "comment": fb_cmt, "date": datetime.now().strftime("%d/%m/%Y")})
            st.success("Cảm ơn đánh giá tuyệt vời của bạn!")
            st.rerun()
        else:
            st.warning("Vui lòng điền đủ tên và nội dung đánh giá.")

# ==================== TAB 6: QUẢN TRỊ ADMIN ====================
with tab_admin:
    st.subheader("📊 Trang Quản Trị & Thống Kê Doanh Thu")
    if not st.session_state.orders_db:
        st.info("Chưa có đơn hàng nào được ghi nhận trong hệ thống.")
    else:
        df_orders = pd.DataFrame(st.session_state.orders_db)
        total_rev = df_orders["Tổng tiền"].sum()
        total_orders = len(df_orders)
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("💰 Tổng doanh thu", f"{total_rev:,} VNĐ")
        col_m2.metric("📦 Tổng số đơn hàng", f"{total_orders} đơn")
        
        st.markdown("---")
        st.subheader("📋 Danh sách đơn hàng thực tế")
        st.dataframe(df_orders[["Mã đơn", "Khách hàng", "Hình thức", "Tổng tiền", "Thời gian", "Trạng thái"]], use_container_width=True, hide_index=True)
