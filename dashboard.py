# dashboard.py
# Abonelik Takip Dashboard'u - v4 (Tasarım güncellemesi)

import streamlit as st
import pandas as pd
from datetime import datetime
from veritabani import abonelikleri_getir, abonelik_ekle, abonelik_sil, baslangic_verisi_yukle

baslangic_verisi_yukle()

st.set_page_config(page_title="Abonelik Takipçi", page_icon="💰", layout="wide")

# Custom CSS
st.markdown("""
<style>
    /* Ana arka plan */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    /* Başlık */
    h1 {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    
    /* Alt başlıklar */
    h2, h3 {
        color: #e0e0e0 !important;
    }
    
    /* Metrik kartları */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stMetricLabel"] {
        color: #9ca3af !important;
        font-size: 0.85rem !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    
    /* Uyarı kutuları */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }
    
    /* Butonlar */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.05);
        color: white;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: rgba(255,0,0,0.2);
        border-color: #ff4444;
    }
    
    /* Form */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
    }
    
    /* Input alanları */
    .stTextInput input, .stNumberInput input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Genel metin */
    .stMarkdown p, .stMarkdown li {
        color: #d1d5db !important;
    }
    
    /* Abonelik satırları */
    [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 4px;
    }
    
    /* Kapat hamburger menu rengini */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.2);
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Veritabanından çek
abonelikler = abonelikleri_getir()

# Hesaplamalar
toplam_aylik = sum(a["tutar_tl"] for a in abonelikler)
aktif_sayisi = len([a for a in abonelikler if a["durum"] == "aktif"])
sorunlu = len([a for a in abonelikler if a["durum"] != "aktif"])

# Başlık
st.title("💰 Abonelik Takipçi")
st.caption(f"📅 {datetime.now().strftime('%d %B %Y, %H:%M')}")

# Üst metrikler
col1, col2, col3, col4 = st.columns(4)
col1.metric("Aylık Toplam", f"₺{toplam_aylik:,.0f}")
col2.metric("Yıllık Toplam", f"₺{toplam_aylik * 12:,.0f}")
col3.metric("Aktif", f"{aktif_sayisi} abonelik")
col4.metric("Sorunlu", f"{sorunlu} abonelik")

st.divider()

# Layout
sol, sag = st.columns([2, 1])

with sol:
    st.subheader("📅 Yaklaşan Yenilemeler")
    bugun = datetime.now().day
    yaklasan = []

    for a in abonelikler:
        fark = a["yenileme"] - bugun
        if 0 <= fark <= 7:
            yaklasan.append((a, fark))
        elif fark < 0 and (fark + 30) <= 7:
            yaklasan.append((a, fark + 30))

    if yaklasan:
        for a, gun in sorted(yaklasan, key=lambda x: x[1]):
            if gun == 0:
                st.error(f"🔴 BUGÜN → {a['servis']} — ₺{a['tutar_tl']:,.0f}")
            elif gun <= 3:
                st.error(f"🟠 {gun} gün → {a['servis']} — ₺{a['tutar_tl']:,.0f}")
            else:
                st.warning(f"🟡 {gun} gün → {a['servis']} — ₺{a['tutar_tl']:,.0f}")
    else:
        st.success("✅ Bu hafta yenilenecek abonelik yok.")

    st.divider()
    st.subheader("📊 Tüm Abonelikler")

    for a in sorted(abonelikler, key=lambda x: x["tutar_tl"], reverse=True):
        c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 1, 1])
        c1.write(f"**{a['servis']}**")
        c2.write(f"₺{a['tutar_tl']:,.0f}/ay")
        c3.write(f"Her ayın {a['yenileme']}'i")
        c4.write("✅" if a["durum"] == "aktif" else "⚠️")
        if c5.button("🗑️", key=f"sil_{a['id']}"):
            abonelik_sil(a["id"])
            st.rerun()

with sag:
    st.subheader("📊 Harcama Dağılımı")
    
    if abonelikler:
        df = pd.DataFrame(abonelikler)
        
        # Servis bazlı bar chart
        servis_df = df[["servis", "tutar_tl"]].set_index("servis")
        st.bar_chart(servis_df)
        
        # En pahalı
        en_pahali = max(abonelikler, key=lambda x: x["tutar_tl"])
        st.metric("👑 En Pahalı", en_pahali["servis"], f"₺{en_pahali['tutar_tl']:,.0f}/ay")

    st.divider()
    st.subheader("➕ Yeni Abonelik")

    with st.form("yeni_abonelik"):
        servis = st.text_input("Servis Adı")
        tutar = st.number_input("Aylık Tutar (₺)", min_value=0, step=10)
        yenileme = st.slider("Yenileme Günü", 1, 30, 15)
        kaynak = st.selectbox("Kaynak", ["Gmail", "App Store", "Banka", "Manuel"])

        if st.form_submit_button("➕ Ekle"):
            if servis and tutar > 0:
                abonelik_ekle(servis, tutar, yenileme, kaynak)
                st.rerun()
            else:
                st.error("Servis adı ve tutar gerekli!")