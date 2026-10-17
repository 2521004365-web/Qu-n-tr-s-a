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
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 99%, #FECFEF 100%);
        padding: 20px;
        border-radius: 20px;
        color: #D81B60;
        text-align: center;
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4);
        margin-bottom: 10px;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-weight: 600;
        margin-bottom: 25px;
    }
    .product-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 18px;
        border: 2px solid #FFE4E8;
        box-shadow: 0 6px 12px rgba(255, 182, 193, 0.2);
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    .fortune-box {
        background: linear-gradient(135deg, #a8edda 0%, #fed6e3 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        font-weight: bold;
        color: #333;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        background-color: #FF6B81;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF4757;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

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

SUGAR_LEVELS = ["100% (Chuẩn vị ngọt thanh)", "70% (Nên thử - Vừa ngọt)", "50% (Ít ngọt)", "30% (Thanh nhẹ)", "0% (Không đường)"]
ICE_LEVELS = ["100% (Đầy đủ đá)", "70% (Vừa đá)", "50% (Ít đá)", "30% (Sương sương)", "0
