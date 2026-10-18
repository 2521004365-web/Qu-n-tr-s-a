
import streamlit as st
import pandas as pd
from datetime import datetime
from collections import Counter
import random
import urllib.parse
import uuid
import html

# =========================================================
# MAMALALA 2.0 - TEA & COFFEE STUDIO
# Demo dự án: Streamlit
# =========================================================

st.set_page_config(
    page_title="MAMALALA | Tea & Coffee Studio",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- 1. GIAO DIỆN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --pink: #e85d7f;
    --pink-dark: #bd3458;
    --cream: #fff8f3;
    --ink: #34252b;
    --muted: #796b71;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(
        180deg, #fff9f6 0%, #ffffff 55%, #fff5f8 100%
    );
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

.hero {
    background:
        radial-gradient(circle at 12% 20%, #ffe1e9 0, transparent 35%),
        linear-gradient(120deg, #fff0e8, #ffe0e9 60%, #f6d8e6);
    border: 1px solid #f5d0dc;
    border-radius: 26px;
    padding: 32px;
    margin-bottom: 18px;
}

.hero-kicker {
    color: #a84360;
    font-weight: 800;
    letter-spacing: 2px;
    font-size: .76rem;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    color: #7d2945;
    font-size: clamp(2.1rem, 5vw, 3.6rem);
    line-height: 1.08;
    margin: 10px 0;
}

.hero-copy {
    color: #704c59;
    max-width: 680px;
    font-size: 1rem;
}

.pill {
    display: inline-block;
    background: white;
    color: #a13d5b;
    border: 1px solid #f2cbd6;
    border-radius: 100px;
    padding: 6px 12px;
    margin: 5px 5px 0 0;
    font-size: .8rem;
    font-weight: 700;
}

.product-card {
    background: white;
    border: 1px solid #f1dce2;
    border-radius: 16px;
    padding: 15px;
    box-shadow: 0 6px 20px rgba(112,48,70,.06);
    margin-bottom: 10px;
}

.product-title {
    color: #492b36;
    font-size: 1rem;
    font-weight: 800;
    min-height: 2.6rem;
}

.product-desc {
    color: #796b71;
    font-size: .86rem;
    min-height: 2.8rem;
}

.price {
    color: #c43e65;
    font-size: 1.15rem;
    font-weight: 800;
}

.tag {
    display: inline-block;
    background: #fff0f4;
    color: #b33b5d;
    border-radius: 7px;
    padding: 4px 7px;
    font-size: .7rem;
    font-weight: 800;
}

.section-kicker {
    color: #b44c68;
    font-weight: 800;
    letter-spacing: 1.5px;
    font-size: .75rem;
}

div.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    border: 1px solid #f0c7d2;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(120deg, #e85d7f, #c83f66);
    color: white;
    border: 0;
}

div.stButton > button:hover {
    border-color: #e85d7f;
}

[data-testid="stSidebar"] {
    background: #fff4f6;
    border-right: 1px solid #f4dce3;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #f2dce2;
    padding: 14px;
    border-radius: 14px;
}

.small-muted {
    color: #84757b;
    font-size: .82rem;
}
</style>
""", unsafe_allow_html=True)


# -------------------- 2. MENU --------------------
# Bạn có thể thay URL ảnh bằng ảnh sản phẩm của quán.
# Nếu có ảnh trong GitHub, đặt trong thư mục images/.

MENU = {
    "🧋 Trà Sữa Signatures": [
        {
            "name": "Trà Sữa Truyền Thống MAMALALA",
            "price": 20000,
            "desc": "Đậm trà, béo dịu, chuẩn vị thân quen.",
            "tag": "🔥 BEST SELLER",
            "image": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=800&q=80",
            "mood": ["sweet", "comfort"],
        },
        {
            "name": "Sữa Tươi Trân Châu Đường Đen",
            "price": 35000,
            "desc": "Sữa tươi kết hợp trân châu đường đen.",
            "tag": "👑 SIGNATURE",
            "image": "https://images.unsplash.com/photo-1558857563-b371033873b8?auto=format&fit=crop&w=800&q=80",
            "mood": ["sweet", "comfort"],
        },
        {
            "name": "Matcha Freeze Uji Nhật Bản",
            "price": 35000,
            "desc": "Matcha thơm thanh, hậu vị dịu mát.",
            "tag": "🌿 GREEN PICK",
            "image": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=800&q=80",
            "mood": ["fresh", "focus"],
        },
        {
            "name": "Cacao Latte Macchiato",
            "price": 35000,
            "desc": "Cacao đậm vị cùng lớp sữa mịn.",
            "tag": "🍫 CHOCO LOVE",
            "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=800&q=80",
            "mood": ["comfort", "sweet"],
        },
    ],
    "🍓 Trà Trái Cây Tươi Mới": [
        {
            "name": "Trà Xanh Hoa Nhài Thanh Lương",
            "price": 32000,
            "desc": "Hương nhài nhẹ nhàng, thanh mát.",
            "tag": "🌸 LIGHT & FRESH",
            "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=800&q=80",
            "mood": ["fresh", "calm"],
        },
        {
            "name": "Trà Gạo Rang Genmaicha",
            "price": 35000,
            "desc": "Hương gạo rang ấm áp, vị trà cân bằng.",
            "tag": "⭐ TEA LOVER",
            "image": "https://images.unsplash.com/photo-1544787219-7f47af3fc05e?auto=format&fit=crop&w=800&q=80",
            "mood": ["calm", "focus"],
        },
        {
            "name": "Sữa Dâu MAMALALA",
            "price": 38000,
            "desc": "Hương dâu ngọt ngào, màu hồng xinh.",
            "tag": "📸 PHOTO PICK",
            "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=800&q=80",
            "mood": ["sweet", "comfort"],
        },
        {
            "name": "Trà Dưa Lưới Nhiệt Đới",
            "price": 32000,
            "desc": "Vị trái cây tươi mát cho ngày nắng.",
            "tag": "🍈 TROPICAL",
            "image": "https://images.unsplash.com/photo-1513558161293-cdaf765edfd7?auto=format&fit=crop&w=800&q=80",
            "mood": ["fresh", "calm"],
        },
    ],
}

SIZE_OPTIONS = {"S": 0, "M": 5000, "L": 10000}

TOPPING_OPTIONS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000,
}

SUGAR_LEVELS = ["100%", "70%", "50%", "30%", "0%"]
ICE_LEVELS = ["100%", "70%", "50%", "30%", "0%"]

VOUCHER_CODES = {
    "THUDUC20": 20,
    "MAMALALA50": 50,
    "XINCHAO": 10,
}

ORDER_STATUSES = [
    "Đã tiếp nhận",
    "Đang pha chế",
    "Sẵn sàng nhận",
    "Đang giao",
    "Hoàn tất",
    "Đã hủy",
]

FORTUNES = [
    "Một ngày dịu dàng bắt đầu từ một ngụm trà ngon. 🌷",
    "Bạn xứng đáng có một khoảng nghỉ ngọt ngào hôm nay. 💗",
    "Năng lượng mới đang chờ bạn ở chiếc ly tiếp theo. ✨",
    "Chậm lại một chút, thưởng thức điều mình thích nhé. 🍵",
]


# -------------------- 3. SESSION STATE --------------------

DEFAULTS = {
    "cart": [],
    "orders": [],
    "reviews": [
        {
            "name": "Gia Hân",
            "rating": 5,
            "comment": "Quán xinh, trà thơm và dễ uống.",
            "date": "16/10/2026",
        },
        {
            "name": "Minh Anh",
            "rating": 5,
            "comment": "Trân châu dẻo, đóng gói chỉn chu.",
            "date": "15/10/2026",
        },
    ],
    "spin_discount": 0,
    "promo_discount": 0,
    "used_vouchers": [],
    "last_order_id": None,
    "member_points": 35,
    "fortune": "",
    "mood_pick": "",
    "admin_logged_in": False,
    "admin_attempts": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -------------------- 4. HÀM HỖ TRỢ --------------------

def money(value):
    return f"{int(value):,}".replace(",", ".") + " VNĐ"


def all_products():
    return [
        product
        for category in MENU.values()
        for product in category
    ]


def find_product(name):
    for product in all_products():
        if product["name"] == name:
            return product
    return None


def cart_subtotal():
    return sum(
        item["unit_price"] * item["qty"]
        for item in st.session_state.cart
    )


def current_discount():
    # Tổng giảm giá tối đa 60%, không để voucher xóa toàn bộ tiền hàng.
    return min(
        60,
        st.session_state.spin_discount
        + st.session_state.promo_discount,
    )


def add_to_cart(product, size, sugar, ice, toppings, qty, note):
    unit_price = (
        product["price"]
        + SIZE_OPTIONS[size]
        + sum(TOPPING_OPTIONS[t] for t in toppings)
    )

    st.session_state.cart.append({
        "name": product["name"],
        "size": size,
        "sugar": sugar,
        "ice": ice,
        "toppings": list(toppings),
        "qty": int(qty),
        "note": note.strip() or "-",
        "unit_price": unit_price,
    })


def find_order(order_id):
    return next(
        (
            order for order in st.session_state.orders
            if order["order_id"] == order_id
        ),
        None,
    )


# -------------------- 5. SIDEBAR --------------------

with st.sidebar:
    st.markdown("## 🧋 MAMALALA")
    st.caption("TEA • COFFEE • LITTLE JOY")

    st.markdown("---")
    st.markdown("### 🏡 Thông tin cửa hàng")
    st.write("📍 32 Võ Văn Hát, P. Long Trường, TP. Thủ Đức")
    st.write("⏰ 08:00 – 22:30")
    st.write("☎️ 0987.xxx.xxx")

    st.markdown("---")
    st.markdown("### 🎡 Lucky Sip")
    st.caption("Quay một lượt để nhận ưu đãi vui vẻ.")

    if st.button("🎁 QUAY NHẬN VOUCHER", use_container_width=True):
        st.session_state.spin_discount = random.choices(
            [0, 5, 10, 15, 20],
            weights=[20, 30, 25, 17, 8],
        )[0]

        if st.session_state.spin_discount > 0:
            st.balloons()
            st.success(
                f"Bạn nhận được voucher "
                f"{st.session_state.spin_discount}%!"
            )
        else:
            st.info("Chưa trúng lần này. Hẹn bạn lượt sau!")

    if st.session_state.spin_discount:
        st.caption(
            f"Voucher vòng quay: "
            f"-{st.session_state.spin_discount}%"
        )

    st.markdown("---")
    st.markdown("### 🎟️ Mã giảm giá")

    voucher_code = st.text_input(
        "Nhập mã voucher",
        placeholder="Ví dụ: XINCHAO",
        key="voucher_input",
    ).strip().upper()

    if st.button("ÁP DỤNG MÃ", use_container_width=True):
        if voucher_code in st.session_state.used_vouchers:
            st.error("Mã này đã được sử dụng trong phiên demo.")
        elif voucher_code in VOUCHER_CODES:
            st.session_state.promo_discount = VOUCHER_CODES[voucher_code]
            st.session_state.active_voucher = voucher_code
            st.success(
                f"Đã áp dụng mã giảm "
                f"{VOUCHER_CODES[voucher_code]}%."
            )
        else:
            st.session_state.promo_discount = 0
            st.session_state.active_voucher = ""
            st.error("Mã không hợp lệ.")

    st.caption(
        "Bản demo: giới hạn giảm giá và sử dụng voucher "
        "chỉ được mô phỏng trong phiên hiện tại."
    )


# -------------------- 6. HERO BANNER --------------------

st.markdown("""
<div class="hero">
    <div class="hero-kicker">A LITTLE CUP OF HAPPINESS</div>
    <div class="hero-title">MAMALALA<br>Tea & Coffee Studio</div>
    <div class="hero-copy">
        Chọn vị bạn yêu, tạo chiếc ly của riêng mình
        và để hôm nay ngọt ngào hơn một chút.
    </div>
    <div>
        <span class="pill">✦ Pha chế theo gu</span>
        <span class="pill">♡ Made with care</span>
        <span class="pill">☁️ Sip your mood</span>
    </div>
</div>
""", unsafe_allow_html=True)

hero1, hero2, hero3 = st.columns(3)
hero1.metric("🧋 Sản phẩm", len(all_products()))
hero2.metric("🎀 Điểm Sweet Club", st.session_state.member_points)
hero3.metric("🛒 Món trong giỏ", sum(
    item["qty"] for item in st.session_state.cart
))


# -------------------- 7. TABS --------------------

tab_shop, tab_mood, tab_cart, tab_tracking, tab_club, tab_reviews, tab_admin = st.tabs([
    "🛍️ Cửa hàng",
    "✨ Mood Match",
    "🛒 Giỏ hàng & thanh toán",
    "📦 Theo dõi đơn",
    "🎀 Sweet Club",
    "⭐ Đánh giá",
    "📊 Quản trị",
])


# =========================================================
# TAB 1: CỬA HÀNG
# =========================================================

with tab_shop:
    st.markdown(
        '<div class="section-kicker">FIND YOUR NEW FAVORITE</div>',
        unsafe_allow_html=True,
    )
    st.header("Hôm nay mình uống gì nhỉ?")

    search = st.text_input(
        "🔎 Tìm đồ uống",
        placeholder="Tìm matcha, dâu, trà sữa...",
        key="product_search",
    ).strip().lower()

    categories = ["Tất cả"] + list(MENU.keys())

    category_selected = st.selectbox(
        "Danh mục sản phẩm",
        categories,
        key="product_category",
    )

    if category_selected == "Tất cả":
        product_list = all_products()
    else:
        product_list = MENU[category_selected]

    product_list = [
        p for p in product_list
        if search in p["name"].lower()
        or search in p["desc"].lower()
    ]

    if not product_list:
        st.warning("Không tìm thấy món phù hợp.")
    else:
        cols = st.columns(4)

        for index, product in enumerate(product_list):
            with cols[index % 4]:
                st.image(
                    product["image"],
                    use_container_width=True,
                )

                safe_name = html.escape(product["name"])
                safe_desc = html.escape(product["desc"])
                safe_tag = html.escape(product["tag"])

                st.markdown(
                    f"""
                    <div class="product-card">
                        <span class="tag">{safe_tag}</span>
                        <div class="product-title">{safe_name}</div>
                        <div class="product-desc">{safe_desc}</div>
                        <div class="price">{money(product['price'])}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with st.expander("✨ Tùy chỉnh ly"):
                    size = st.radio(
                        "Size",
                        list(SIZE_OPTIONS.keys()),
                        horizontal=True,
                        key=f"size_{product['name']}",
                    )

                    sugar = st.select_slider(
                        "Đường",
                        options=SUGAR_LEVELS,
                        value="70%",
                        key=f"sugar_{product['name']}",
                    )

                    ice = st.select_slider(
                        "Đá",
                        options=ICE_LEVELS,
                        value="70%",
                        key=f"ice_{product['name']}",
                    )

                    toppings = st.multiselect(
                        "Topping",
                        list(TOPPING_OPTIONS.keys()),
                        key=f"topping_{product['name']}",
                    )

                    qty = st.number_input(
                        "Số lượng",
                        min_value=1,
                        max_value=20,
                        value=1,
                        key=f"qty_{product['name']}",
                    )

                    note = st.text_input(
                        "Ghi chú",
                        placeholder="Ví dụ: ít đá...",
                        key=f"note_{product['name']}",
                    )

                    unit_price = (
                        product["price"]
                        + SIZE_OPTIONS[size]
                        + sum(TOPPING_OPTIONS[t] for t in toppings)
                    )

                    st.write(f"Đơn giá: **{money(unit_price)}**")

                    if st.button(
                        "＋ Thêm vào giỏ",
                        key=f"add_{product['name']}",
                        type="primary",
                        use_container_width=True,
                    ):
                        add_to_cart(
                            product, size, sugar, ice,
                            toppings, qty, note,
                        )
                        st.toast(
                            f"Đã thêm {product['name']} vào giỏ!",
                            icon="🧋",
                        )
                        st.rerun()

    st.markdown("---")
    st.caption(
        "Ảnh minh họa từ nguồn trực tuyến. "
        "Bạn nên thay bằng ảnh thật của MAMALALA để tạo nhận diện riêng."
    )


# =========================================================
# TAB 2: MOOD MATCH
# =========================================================

with tab_mood:
    st.markdown(
        '<div class="section-kicker">MAMALALA PERSONALITY BAR</div>',
        unsafe_allow_html=True,
    )
    st.header("Mood Match — tìm món hợp tâm trạng")

    st.write(
        "Trả lời vài câu hỏi để tìm chiếc ly phù hợp "
        "với mood hôm nay của bạn."
    )

    mood = st.radio(
        "1. Bạn đang cần điều gì?",
        [
            "🌿 Tươi mới, tỉnh táo",
            "☁️ Bình yên, thư giãn",
            "💗 Một chút ngọt ngào",
            "📚 Tập trung học tập",
        ],
    )

    taste = st.radio(
        "2. Bạn thích vị nào?",
        ["Thanh nhẹ", "Ngọt béo", "Trà đậm"],
        horizontal=True,
    )

    vibe = st.radio(
        "3. Chọn vibe hôm nay",
        ["Nhẹ nhàng", "Năng động", "Tự thưởng"],
        horizontal=True,
    )

    mood_key = {
        "🌿 Tươi mới, tỉnh táo": "fresh",
        "☁️ Bình yên, thư giãn": "calm",
        "💗 Một chút ngọt ngào": "sweet",
        "📚 Tập trung học tập": "focus",
    }[mood]

    if st.button(
        "✨ TÌM CHIẾC LY DÀNH CHO MÌNH",
        type="primary",
    ):
        candidates = [
            p for p in all_products()
            if mood_key in p["mood"]
        ]

        if taste == "Thanh nhẹ":
            filtered = [
                p for p in candidates
                if any(word in p["name"].lower()
                       for word in ["trà xanh", "genmaicha", "dưa lưới", "matcha"])
            ]
            if filtered:
                candidates = filtered

        elif taste == "Ngọt béo":
            filtered = [
                p for p in candidates
                if any(word in p["name"].lower()
                       for word in ["sữa", "latte", "trà sữa"])
            ]
            if filtered:
                candidates = filtered

        picked = random.choice(candidates or all_products())
        st.session_state.mood_pick = picked["name"]

    if st.session_state.mood_pick:
        picked = find_product(st.session_state.mood_pick)

        if picked:
            st.image(picked["image"], width=320)
            st.success(
                f"MAMALALA gợi ý: **{picked['name']}**"
            )
            st.write(picked["desc"])
            st.write(f"**{money(picked['price'])}** · Vibe: {vibe}")

            if st.button(
                "🧋 Thêm món gợi ý vào giỏ",
                type="primary",
                key="mood_add",
            ):
                add_to_cart(
                    picked, "M", "70%", "70%", [],
                    1, "Gợi ý từ Mood Match",
                )
                st.toast("Đã thêm vào giỏ!", icon="💗")
                st.rerun()

    st.markdown("---")
    st.subheader("🔮 Một lời nhắn cho hôm nay")

    if st.button("Rút một lời nhắn"):
        st.session_state.fortune = random.choice(FORTUNES)

    if st.session_state.fortune:
        st.info(st.session_state.fortune)


# =========================================================
# TAB 3: GIỎ HÀNG & THANH TOÁN
# =========================================================

with tab_cart:
    st.header("Giỏ hàng của bạn")

    if not st.session_state.cart:
        st.info(
            "Giỏ hàng đang trống. "
            "Hãy ghé Cửa hàng để chọn món nhé! 🧋"
        )
    else:
        for index, item in enumerate(st.session_state.cart):
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 2, 1])

                c1.markdown(f"**{item['name']}**")
                c1.caption(
                    f"Size {item['size']} · Đường {item['sugar']} "
                    f"· Đá {item['ice']}"
                )
                c1.caption(
                    "Topping: "
                    + (", ".join(item["toppings"]) or "Không")
                    + f" · Ghi chú: {item['note']}"
                )

                new_qty = c2.number_input(
                    "Số lượng",
                    min_value=1,
                    max_value=20,
                    value=item["qty"],
                    key=f"cart_quantity_{index}",
                )

                if new_qty != item["qty"]:
                    st.session_state.cart[index]["qty"] = new_qty

                c2.write(f"Đơn giá: {money(item['unit_price'])}")
                c3.markdown(
                    f"**{money(item['unit_price'] * new_qty)}**"
                )

                if c3.button("🗑️ Xóa", key=f"remove_{index}"):
                    st.session_state.cart.pop(index)
                    st.rerun()

        subtotal = cart_subtotal()
        discount = current_discount()
        discount_amount = int(subtotal * discount / 100)
        final_total = subtotal - discount_amount

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Tạm tính", money(subtotal))
        col2.metric(
            f"Giảm giá ({discount}%)",
            "-" + money(discount_amount),
        )
        col3.metric("THANH TOÁN", money(final_total))

        st.markdown("---")
        st.subheader("Thông tin đặt hàng")

        with st.form("checkout_form"):
            customer_name = st.text_input("Tên khách hàng *")
            phone = st.text_input("Số điện thoại *")

            order_type = st.radio(
                "Hình thức nhận",
                ["Tại quán", "Mang đi", "Giao hàng"],
                horizontal=True,
            )

            address = st.text_input(
                "Số bàn / địa chỉ nhận",
                placeholder="Bắt buộc nếu chọn giao hàng",
            )

            payment_method = st.radio(
                "Phương thức thanh toán",
                ["Chuyển khoản QR (demo)", "Tiền mặt khi nhận"],
                horizontal=False,
            )

            submit_order = st.form_submit_button(
                "💗 XÁC NHẬN ĐẶT HÀNG",
                type="primary",
                use_container_width=True,
            )

        if submit_order:
            if not customer_name.strip() or not phone.strip():
                st.error("Vui lòng nhập tên và số điện thoại.")
            elif not phone.strip().replace(" ", "").isdigit():
                st.error("Số điện thoại chỉ nên chứa chữ số.")
            elif order_type == "Giao hàng" and not address.strip():
                st.error("Vui lòng nhập địa chỉ giao hàng.")
            else:
                order_id = "MAMA-" + uuid.uuid4().hex[:8].upper()

                order = {
                    "order_id": order_id,
                    "customer": customer_name.strip(),
                    "phone": phone.strip(),
                    "type": order_type,
                    "address": address.strip() or "-",
                    "items": [dict(item) for item in st.session_state.cart],
                    "subtotal": subtotal,
                    "discount_percent": discount,
                    "discount_amount": discount_amount,
                    "total": final_total,
                    "payment": payment_method,
                    "payment_status": (
                        "Chưa xác nhận"
                        if "QR" in payment_method
                        else "Thanh toán khi nhận"
                    ),
                    "created": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "status": "Đã tiếp nhận",
                }

                st.session_state.orders.append(order)
                st.session_state.last_order_id = order_id
                st.session_state.cart = []

                # Cộng điểm demo khi đơn được tạo.
                # Bản thật nên cộng sau khi đơn hoàn tất.
                st.session_state.member_points += final_total // 10000

                st.session_state.spin_discount = 0
                st.session_state.promo_discount = 0
                st.session_state.active_voucher = ""

                st.success(
                    f"Đặt hàng thành công! Mã đơn: **{order_id}**"
                )
                st.balloons()
                st.rerun()

    # Hiển thị QR cho đơn gần nhất
    last_id = st.session_state.last_order_id
    last_order = find_order(last_id) if last_id else None

    if last_order:
        st.markdown("---")
        st.subheader("🧾 Đơn hàng gần nhất")
        st.write(f"Mã đơn: **{last_order['order_id']}**")
        st.write(f"Tổng tiền: **{money(last_order['total'])}**")
        st.write(f"Trạng thái: **{last_order['status']}**")

        if "QR" in last_order["payment"]:
            st.warning(
                "QR dưới đây là bản minh họa. "
                "Chưa có xác nhận thanh toán tự động."
            )

            # THAY THÔNG TIN MẪU TRƯỚC KHI DÙNG THẬT
            bank_id = "MB"
            account_no = "0987654321"
            account_name = "QUAN TRA SUA MAMALALA"

            transfer_info = f"THANH TOAN {last_order['order_id']}"

            qr_url = (
                f"https://img.vietqr.io/image/"
                f"{bank_id}-{account_no}-compact2.png"
                f"?amount={last_order['total']}"
                f"&addInfo={urllib.parse.quote(transfer_info)}"
                f"&accountName={urllib.parse.quote(account_name)}"
            )

            st.image(
                qr_url,
                width=260,
                caption="QR minh họa — chưa xác nhận đã nhận tiền",
            )
            st.caption(f"Nội dung chuyển khoản: {transfer_info}")


# =========================================================
# TAB 4: THEO DÕI ĐƠN HÀNG
# =========================================================

with tab_tracking:
    st.header("📦 Theo dõi đơn hàng")

    lookup_id = st.text_input(
        "Nhập mã đơn hàng",
        placeholder="Ví dụ: MAMA-AB12CD34",
    ).strip().upper()

    if lookup_id:
        order = find_order(lookup_id)

        if order:
            st.markdown(f"### Đơn {order['order_id']}")
            st.caption(
                f"Thời gian: {order['created']} · "
                f"Hình thức: {order['type']}"
            )

            st.write(f"Khách hàng: {order['customer']}")
            st.write(f"Tổng tiền: **{money(order['total'])}**")
            st.write(f"Thanh toán: {order['payment_status']}")

            status = order["status"]

            if status == "Đã hủy":
                st.error("Đơn hàng đã bị hủy.")
            else:
                st.success(f"Trạng thái hiện tại: **{status}**")

                progress_map = {
                    "Đã tiếp nhận": 0.15,
                    "Đang pha chế": 0.40,
                    "Sẵn sàng nhận": 0.70,
                    "Đang giao": 0.85,
                    "Hoàn tất": 1.0,
                }

                st.progress(progress_map.get(status, 0.0))

                for step in [
                    "Đã tiếp nhận",
                    "Đang pha chế",
                    "Sẵn sàng nhận",
                    "Đang giao",
                    "Hoàn tất",
                ]:
                    marker = "✅" if (
                        step == status or
                        (
                            status in ORDER_STATUSES
                            and status != "Đã hủy"
                            and ORDER_STATUSES.index(step)
                            < ORDER_STATUSES.index(status)
                        )
                    ) else "○"

                    st.write(f"{marker} {step}")

            with st.expander("Xem chi tiết món"):
                for item in order["items"]:
                    st.write(
                        f"- {item['name']} · Size {item['size']} "
                        f"· x{item['qty']} · "
                        f"{money(item['unit_price'] * item['qty'])}"
                    )
        else:
            st.error(
                "Không tìm thấy đơn. "
                "Bản demo chỉ tìm được đơn trong phiên hiện tại."
            )


# =========================================================
# TAB 5: SWEET CLUB
# =========================================================

with tab_club:
    st.markdown(
        '<div class="section-kicker">GOOD SIPS, LOVELY PERKS</div>',
        unsafe_allow_html=True,
    )
    st.header("Sweet Club 🎀")

    member_col1, member_col2 = st.columns([1, 2])

    with member_col1:
        st.markdown("""
        <div class="hero">
            <div class="hero-kicker">YOUR MEMBER CARD</div>
            <div class="hero-title" style="font-size:2rem;">
                Sweetie ♡
            </div>
            <p class="hero-copy">
                Every sip brings you closer to a little treat.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.metric(
            "Điểm hiện có",
            f"{st.session_state.member_points} điểm",
        )

        if st.session_state.member_points >= 100:
            st.success("🏆 Bạn đã đạt mốc quà tặng 100 điểm!")

    with member_col2:
        st.subheader("🎁 Đổi điểm lấy quà")
        st.write("30 điểm — miễn phí 1 topping")
        st.write("60 điểm — voucher 15%")
        st.write("100 điểm — một ly size S")

        if st.session_state.member_points >= 30:
            if st.button("🎁 Đổi 30 điểm lấy topping"):
                st.session_state.member_points -= 30
                st.success("Đổi quà demo thành công!")
                st.rerun()
        else:
            st.info(
                f"Cần thêm {30 - st.session_state.member_points} "
                "điểm để đổi topping."
            )

        st.markdown("---")
        st.subheader("📖 Drink Passport")
        st.write(
            "Thử nhiều dòng đồ uống để trở thành "
            "Fruit Explorer, Tea Lover hoặc Signature Fan."
        )

        tried = st.multiselect(
            "Chọn các dòng đồ uống bạn đã khám phá",
            [
                "Trà sữa",
                "Trà trái cây",
                "Matcha",
                "Cacao",
            ],
            key="drink_passport",
        )

        st.progress(len(tried) / 4)
        st.caption(f"Đã khám phá {len(tried)}/4 dòng đồ uống.")

        if len(tried) == 4:
            st.success("🏅 Huy hiệu demo: MAMALALA Explorer!")

        st.caption(
            "Điểm và bộ sưu tập hiện chỉ lưu trong phiên demo."
        )


# =========================================================
# TAB 6: ĐÁNH GIÁ
# =========================================================

with tab_reviews:
    st.header("⭐ Khách hàng nói gì?")

    reviews = st.session_state.reviews

    if reviews:
        avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
        st.metric("Điểm đánh giá trung bình", f"{avg_rating:.1f}/5")

    for review in reviews:
        with st.container(border=True):
            st.markdown(
                f"**{html.escape(review['name'])}** "
                f"· {'⭐' * review['rating']} "
                f"· {review['date']}"
            )
            st.write(review["comment"])

    st.markdown("---")
    st.subheader("💌 Gửi đánh giá của bạn")

    with st.form("review_form"):
        review_name = st.text_input("Tên của bạn")
        rating = st.slider("Số sao", 1, 5, 5)
        comment = st.text_area(
            "Cảm nhận",
            placeholder="Kể MAMALALA nghe nhé...",
        )

        submit_review = st.form_submit_button("Gửi đánh giá")

    if submit_review:
        if review_name.strip() and comment.strip():
            st.session_state.reviews.insert(
                0,
                {
                    "name": review_name.strip(),
                    "rating": rating,
                    "comment": comment.strip(),
                    "date": datetime.now().strftime("%d/%m/%Y"),
                },
            )

            st.success("Cảm ơn bạn đã gửi đánh giá!")
            st.rerun()
        else:
            st.error("Vui lòng nhập tên và cảm nhận.")


# =========================================================
# TAB 7: ADMIN DASHBOARD
# =========================================================

with tab_admin:
    st.header("📊 MAMALALA Admin Dashboard")

    if not st.session_state.admin_logged_in:
        st.info(
            "Đăng nhập để xem dashboard quản trị demo."
        )

        with st.form("admin_login"):
            password = st.text_input(
                "Mật khẩu demo",
                type="password",
            )
            login = st.form_submit_button("Đăng nhập")

        if login:
            # MẬT KHẨU DEMO, KHÔNG DÙNG CHO WEBSITE THẬT
            if password == "mama2026":
                st.session_state.admin_logged_in = True
                st.session_state.admin_attempts = 0
                st.rerun()
            else:
                st.session_state.admin_attempts += 1
                st.error("Mật khẩu chưa đúng.")

    else:
        if st.button("Đăng xuất Admin"):
            st.session_state.admin_logged_in = False
            st.rerun()

        orders = st.session_state.orders

        revenue = sum(
            o["total"] for o in orders
            if o["status"] != "Đã hủy"
        )

        order_count = len([
            o for o in orders if o["status"] != "Đã hủy"
        ])

        average_order = revenue / order_count if order_count else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("💰 Doanh thu đơn hợp lệ", money(revenue))
        c2.metric("📦 Số đơn chưa hủy", order_count)
        c3.metric("🧾 Giá trị đơn trung bình", money(average_order))

        st.markdown("---")
        st.subheader("Quản lý đơn hàng")

        if orders:
            df = pd.DataFrame([
                {
                    "Mã đơn": o["order_id"],
                    "Khách hàng": o["customer"],
                    "SĐT": o["phone"],
                    "Hình thức": o["type"],
                    "Tổng tiền": o["total"],
                    "Thời gian": o["created"],
                    "Trạng thái": o["status"],
                    "Thanh toán": o["payment_status"],
                }
                for o in orders
            ])

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

            st.subheader("🔄 Cập nhật trạng thái")

            selected_id = st.selectbox(
                "Chọn mã đơn",
                [o["order_id"] for o in orders],
            )

            selected_order = find_order(selected_id)

            new_status = st.selectbox(
                "Trạng thái mới",
                ORDER_STATUSES,
                index=ORDER_STATUSES.index(selected_order["status"]),
            )

            if st.button("Lưu trạng thái đơn"):
                selected_order["status"] = new_status
                st.success("Đã cập nhật trạng thái đơn.")
                st.rerun()

            st.markdown("---")
            st.subheader("📈 Doanh thu theo đơn")

            chart_data = pd.DataFrame([
                {
                    "Mã đơn": o["order_id"],
                    "Doanh thu": o["total"],
                }
                for o in orders
                if o["status"] != "Đã hủy"
            ])

            if not chart_data.empty:
                st.bar_chart(
                    chart_data.set_index("Mã đơn")
                )

            st.subheader("🏆 Món được đặt nhiều")

            item_counter = Counter()

            for order in orders:
                if order["status"] != "Đã hủy":
                    for item in order["items"]:
                        item_counter[item["name"]] += item["qty"]

            if item_counter:
                top_products = pd.DataFrame(
                    item_counter.most_common(),
                    columns=["Tên món", "Số lượng đã đặt"],
                )
                st.dataframe(
                    top_products,
                    use_container_width=True,
                    hide_index=True,
                )

            csv_data = df.to_csv(
                index=False
            ).encode("utf-8-sig")

            st.download_button(
                "⬇️ Tải báo cáo đơn hàng CSV",
                data=csv_data,
                file_name="mamalala_orders.csv",
                mime="text/csv",
            )

        else:
            st.info(
                "Chưa có đơn hàng. Hãy thử đặt một món "
                "để xem dashboard hoạt động."
            )

        st.markdown("---")
        st.subheader("📦 Tổng quan menu")

        menu_df = pd.DataFrame([
            {
                "Tên món": p["name"],
                "Giá": p["price"],
                "Danh mục": category,
            }
            for category, products in MENU.items()
            for p in products
        ])

        st.dataframe(
            menu_df,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Dashboard tính từ dữ liệu trong phiên hiện tại, "
            "không phải báo cáo doanh thu thực tế."
        )


# -------------------- FOOTER --------------------

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#9a858d;font-size:.85rem;">
    MAMALALA TEA & COFFEE STUDIO<br>
    Sip your mood, share your joy ♡
</div>
""", unsafe_allow_html=True)
