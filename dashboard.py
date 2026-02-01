import streamlit as st
import sqlite3
import os
from datetime import datetime, timedelta

# Sayfa ayarları
st.set_page_config(
    page_title="Abonelik Takipçi",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800;900&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Ana arka plan */
.stApp {
    background: linear-gradient(180deg, #020617 0%, #0a0f1e 50%, #020617 100%) !important;
}

/* Sidebar gizle */
[data-testid="stSidebar"] { display: none; }

/* Header gizle */
header[data-testid="stHeader"] { background: transparent !important; }

/* Üst boşluğu azalt */
.block-container {
    padding-top: 2rem !important;
    max-width: 1000px !important;
}

/* Başlık stili */
.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #5eead4, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
    letter-spacing: -0.5px;
}

.subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: rgba(148,163,184,0.4);
    margin-top: 4px;
}

.live-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #5eead4;
    margin-right: 4px;
    animation: glow 2s ease-in-out infinite;
}

@keyframes glow { 0%,100%{opacity:0.4} 50%{opacity:1} }
@keyframes slideUp { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }

/* Metric kartlar */
.metric-card {
    background: rgba(15,23,42,0.6);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(94,234,212,0.08);
    border-radius: 16px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
    animation: slideUp 0.6s ease-out;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(94,234,212,0.3), transparent);
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(94,234,212,0.2);
    box-shadow: 0 12px 40px rgba(94,234,212,0.08);
}
.metric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: rgba(148,163,184,0.5);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 800;
    line-height: 1;
}
.metric-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    color: rgba(148,163,184,0.4);
    margin-top: 6px;
}

/* Glass panel */
.glass-panel {
    background: rgba(15,23,42,0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(94,234,212,0.08);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 16px;
    animation: slideUp 0.6s ease-out;
}
.glass-panel:hover {
    border-color: rgba(94,234,212,0.15);
}

/* Bölüm başlığı */
.section-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-icon {
    color: #5eead4;
    font-size: 1.1rem;
}

/* Yenileme satırı */
.renewal-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    margin-bottom: 8px;
    background: rgba(255,255,255,0.02);
    border-radius: 0 12px 12px 0;
    transition: all 0.3s;
}
.renewal-row:hover {
    background: rgba(255,255,255,0.04);
}
.renewal-name {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    color: #e2e8f0;
    font-size: 0.9rem;
}
.renewal-detail {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: rgba(148,163,184,0.5);
    margin-top: 2px;
}
.renewal-amount {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.1rem;
}

/* Abonelik satırı */
.sub-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 18px;
    margin-bottom: 6px;
    background: rgba(15,23,42,0.3);
    border: 1px solid rgba(94,234,212,0.04);
    border-radius: 14px;
    transition: all 0.3s;
}
.sub-row:hover {
    background: rgba(15,23,42,0.6);
    border-color: rgba(94,234,212,0.12);
    transform: translateX(4px);
}

/* SVG Logo */
.brand-logo {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    flex-shrink: 0;
}

.sub-info {
    flex: 1;
}
.sub-name {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    color: #e2e8f0;
    font-size: 0.95rem;
}
.sub-detail {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: rgba(148,163,184,0.4);
    margin-top: 1px;
}
.sub-amount {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.15rem;
    min-width: 80px;
    text-align: right;
}

/* Bar grafik */
.bar-container {
    margin-bottom: 14px;
}
.bar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
}
.bar-name {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    color: #94a3b8;
}
.bar-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #5eead4;
}
.bar-track {
    height: 6px;
    background: rgba(255,255,255,0.03);
    border-radius: 3px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 1s cubic-bezier(0.16,1,0.3,1);
}

/* Kaynak kutuları */
.source-box {
    background: rgba(94,234,212,0.04);
    border: 1px solid rgba(94,234,212,0.06);
    border-radius: 10px;
    padding: 10px 14px;
    flex: 1;
}
.source-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    color: rgba(148,163,184,0.5);
}
.source-value {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: #5eead4;
    margin-top: 2px;
}

/* Footer */
.footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 32px;
    padding-top: 20px;
    border-top: 1px solid rgba(94,234,212,0.04);
}
.footer-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: rgba(148,163,184,0.2);
    letter-spacing: 1px;
}

/* Streamlit widget stilleri */
div[data-testid="stMetric"] { display: none; }

/* Form stilleri */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: rgba(15,23,42,0.6) !important;
    border: 1px solid rgba(94,234,212,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: rgba(94,234,212,0.3) !important;
    box-shadow: 0 0 0 3px rgba(94,234,212,0.05) !important;
}

/* Butonlar */
.stButton > button {
    background: rgba(94,234,212,0.08) !important;
    border: 1px solid rgba(94,234,212,0.15) !important;
    border-radius: 10px !important;
    color: #5eead4 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    background: rgba(94,234,212,0.15) !important;
    border-color: rgba(94,234,212,0.25) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(15,23,42,0.4) !important;
    border: 1px solid rgba(94,234,212,0.08) !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #5eead4 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.4);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(94,234,212,0.06);
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: rgba(148,163,184,0.7) !important;
    border-radius: 10px !important;
    padding: 8px 20px !important;
    letter-spacing: 0.5px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(94,234,212,0.08) !important;
    color: #5eead4 !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(94,234,212,0.2); border-radius: 4px; }

/* Genel metin */
p, span, div { font-family: 'DM Sans', sans-serif; }

/* Toast / alert gizle */
div[data-testid="stStatusWidget"] { display: none; }
</style>
""", unsafe_allow_html=True)

# --- SVG Logolar ---
LOGOS = {
    "Claude Max 5x": '<svg width="38" height="38" viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#D97757"/><path d="M20 8C13.4 8 8 13.4 8 20s5.4 12 12 12 12-5.4 12-12S26.6 8 20 8zm-1.5 17.5l-4-4 1.4-1.4 2.6 2.6 5.6-5.6 1.4 1.4-7 7z" fill="white"/></svg>',
    "Eleven Labs": '<svg width="38" height="38" viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#1a1a2e"/><rect x="14" y="10" width="4" height="20" rx="2" fill="white"/><rect x="22" y="10" width="4" height="20" rx="2" fill="white"/></svg>',
    "ZeroGPT": '<svg width="38" height="38" viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#6C3CE1"/><circle cx="20" cy="20" r="9" stroke="white" stroke-width="3" fill="none"/><path d="M15 25L25 15" stroke="white" stroke-width="2.5" stroke-linecap="round"/></svg>',
    "Canva Pro": '<svg width="38" height="38" viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#00C4CC"/><circle cx="20" cy="20" r="10" fill="#7D2AE8"/><circle cx="20" cy="20" r="5" fill="white"/></svg>',
    "YouTube Premium": '<svg width="38" height="38" viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#FF0000"/><path d="M16 12.5v15l12-7.5-12-7.5z" fill="white"/></svg>',
    "Teuida Languages": '<svg width="38" height="38" viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#FF6B35"/><text x="20" y="26" text-anchor="middle" fill="white" font-size="18" font-weight="800">T</text></svg>',
    "Zero Fasting": '<svg width="38" height="38" viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#FF4757"/><circle cx="20" cy="18" r="8" stroke="white" stroke-width="2.5" fill="none"/><line x1="20" y1="18" x2="20" y2="13" stroke="white" stroke-width="2" stroke-linecap="round"/><line x1="20" y1="18" x2="24" y2="18" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>',
    "Spotify": '<svg width="38" height="38" viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#1DB954"/><path d="M13 22c5-1.5 10-1 14 1" stroke="white" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M14 18c4.5-1.5 9.5-1 13 1.5" stroke="white" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M15 14c4-1.5 9-1 12 2" stroke="white" stroke-width="2.5" stroke-linecap="round" fill="none"/></svg>',
}

def get_logo(name):
    if name in LOGOS:
        return LOGOS[name]
    # Fallback: baş harf logosu
    colors = ['#5eead4','#38bdf8','#a78bfa','#fb923c','#f472b6','#34d399']
    c = colors[sum(ord(ch) for ch in name) % len(colors)]
    return f'<svg width="38" height="38" viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="{c}" opacity="0.15"/><rect width="40" height="40" rx="10" stroke="{c}" stroke-width="1.5" fill="none" opacity="0.3"/><text x="20" y="26" text-anchor="middle" fill="{c}" font-size="18" font-weight="700">{name[0].upper()}</text></svg>'

def tutar_renk(tutar):
    if tutar > 1000: return "#ef4444"
    if tutar > 300: return "#fb923c"
    return "#5eead4"

def bar_renk(tutar):
    if tutar > 1000: return "linear-gradient(90deg, #ef4444, #dc2626)"
    if tutar > 300: return "linear-gradient(90deg, #fb923c, #f59e0b)"
    return "linear-gradient(90deg, #5eead4, #2dd4bf)"

# --- Veritabanı ---
DB_PATH = "abonelikler.db"

def baglanti_kur():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def tablo_olustur():
    conn = baglanti_kur()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS abonelikler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servis TEXT NOT NULL,
            tutar_tl REAL NOT NULL,
            yenileme INTEGER NOT NULL,
            durum TEXT DEFAULT 'aktif',
            kaynak TEXT DEFAULT 'Manuel',
            eklenme_tarihi TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    # Boşsa başlangıç verisi ekle
    sayim = conn.execute("SELECT COUNT(*) FROM abonelikler").fetchone()[0]
    if sayim == 0:
        veriler = [
            ("Claude Max 5x", 3150, 5, "aktif", "Gmail"),
            ("Eleven Labs", 215, 7, "aktif", "Gmail"),
            ("ZeroGPT", 360, 18, "aktif", "Gmail"),
            ("Canva Pro", 470, 12, "bekliyor", "Gmail"),
            ("YouTube Premium", 65, 28, "aktif", "App Store"),
            ("Teuida Languages", 50, 7, "aktif", "App Store"),
            ("Zero Fasting", 80, 16, "aktif", "App Store"),
            ("Spotify", 60, 30, "aktif", "App Store"),
        ]
        for v in veriler:
            conn.execute("INSERT INTO abonelikler (servis, tutar_tl, yenileme, durum, kaynak) VALUES (?,?,?,?,?)", v)
        conn.commit()
    conn.close()

def abonelikleri_getir():
    conn = baglanti_kur()
    rows = conn.execute("SELECT * FROM abonelikler ORDER BY tutar_tl DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def abonelik_ekle(servis, tutar, yenileme, kaynak):
    conn = baglanti_kur()
    conn.execute("INSERT INTO abonelikler (servis, tutar_tl, yenileme, kaynak) VALUES (?,?,?,?)", (servis, tutar, yenileme, kaynak))
    conn.commit()
    conn.close()

def abonelik_sil(id):
    conn = baglanti_kur()
    conn.execute("DELETE FROM abonelikler WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def durum_degistir(id, yeni_durum):
    conn = baglanti_kur()
    conn.execute("UPDATE abonelikler SET durum = ? WHERE id = ?", (yeni_durum, id))
    conn.commit()
    conn.close()

# Tablo oluştur
tablo_olustur()

# --- Header ---
now = datetime.now()
st.markdown(f"""
<div style="margin-bottom: 28px;">
    <div class="main-title">💰 Abonelik Takipçi</div>
    <div class="subtitle"><span class="live-dot"></span> Canlı · {now.strftime('%d %B %Y, %H:%M')}</div>
</div>
""", unsafe_allow_html=True)

# --- Veriler ---
abonelikler = abonelikleri_getir()
toplam = sum(a["tutar_tl"] for a in abonelikler)
aktif = [a for a in abonelikler if a["durum"] == "aktif"]
bekleyen = [a for a in abonelikler if a["durum"] != "aktif"]
bugun = now.day

# Yaklaşan yenilemeler
yaklasan = []
for a in abonelikler:
    fark = a["yenileme"] - bugun
    if fark < 0: fark += 30
    if fark <= 7:
        yaklasan.append({**a, "fark": fark})
yaklasan.sort(key=lambda x: x["fark"])

# Tabs
tab1, tab2, tab3 = st.tabs(["◐  GENEL", "☰  LİSTE", "◑  ANALİZ"])

# ===== TAB 1: GENEL =====
with tab1:
    # Metrikler
    cols = st.columns(4)
    metrics = [
        ("AYLIK TOPLAM", f"₺{toplam:,.0f}", "#5eead4", f"{len(abonelikler)} abonelik"),
        ("YILLIK TOPLAM", f"₺{toplam*12:,.0f}", "#38bdf8", "Projeksiyon"),
        ("AKTİF", f"{len(aktif)} servis", "#a78bfa", f"{len(bekleyen)} bekleyen"),
        ("BU HAFTA", f"₺{sum(a['tutar_tl'] for a in yaklasan):,.0f}", "#fb923c", f"{len(yaklasan)} yenileme"),
    ]
    for col, (label, value, color, sub) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="color:{color}">{value}</div>
                <div class="metric-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # İki kolon: Yaklaşan + Grafik
    col_left, col_right = st.columns(2)

    with col_left:
        renewals_html = ""
        if yaklasan:
            for a in yaklasan:
                renk = "#ef4444" if a["fark"] <= 1 else "#fb923c" if a["fark"] <= 3 else "#5eead4"
                gun_text = "BUGÜN" if a["fark"] == 0 else f"{a['fark']} gün sonra"
                renewals_html += f"""
                <div class="renewal-row" style="border-left: 3px solid {renk}">
                    <div style="display:flex;align-items:center;gap:12px">
                        {get_logo(a['servis'])}
                        <div>
                            <div class="renewal-name">{a['servis']}</div>
                            <div class="renewal-detail">{gun_text} · Her ayın {a['yenileme']}'i</div>
                        </div>
                    </div>
                    <div class="renewal-amount" style="color:{renk}">₺{a['tutar_tl']:,.0f}</div>
                </div>"""
        else:
            renewals_html = '<div style="text-align:center;padding:40px;color:rgba(148,163,184,0.3)"><div style="font-size:40px;margin-bottom:12px">✨</div><p>Bu hafta yenileme yok</p></div>'

        st.markdown(f"""
        <div class="glass-panel">
            <div class="section-title"><span class="section-icon">◔</span> Yaklaşan Yenilemeler</div>
            {renewals_html}
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        max_tutar = max((a["tutar_tl"] for a in abonelikler), default=1)
        bars_html = ""
        for a in sorted(abonelikler, key=lambda x: x["tutar_tl"], reverse=True):
            pct = (a["tutar_tl"] / max_tutar) * 100
            bars_html += f"""
            <div class="bar-container">
                <div class="bar-header">
                    <span class="bar-name">{a['servis']}</span>
                    <span class="bar-value">₺{a['tutar_tl']:,.0f}</span>
                </div>
                <div class="bar-track">
                    <div class="bar-fill" style="width:{pct}%;background:{bar_renk(a['tutar_tl'])}"></div>
                </div>
            </div>"""

        # Kaynak dağılımı
        kaynaklar = {}
        for a in abonelikler:
            kaynaklar[a["kaynak"]] = kaynaklar.get(a["kaynak"], 0) + a["tutar_tl"]

        source_html = ""
        for k, v in kaynaklar.items():
            source_html += f"""
            <div class="source-box">
                <div class="source-label">{k}</div>
                <div class="source-value">₺{v:,.0f}</div>
            </div>"""

        st.markdown(f"""
        <div class="glass-panel">
            <div class="section-title"><span class="section-icon">◑</span> Harcama Dağılımı</div>
            {bars_html}
            <div style="margin-top:20px;padding-top:16px;border-top:1px solid rgba(94,234,212,0.06);display:flex;gap:12px">
                {source_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===== TAB 2: LİSTE =====
with tab2:
    # Yeni abonelik ekleme
    with st.expander("➕ Yeni Abonelik Ekle"):
        c1, c2, c3, c4 = st.columns(4)
        with c1: yeni_servis = st.text_input("Servis Adı", placeholder="Netflix, Spotify...")
        with c2: yeni_tutar = st.number_input("Aylık Tutar (₺)", min_value=0, step=10)
        with c3: yeni_gun = st.number_input("Yenileme Günü", min_value=1, max_value=30, value=15)
        with c4: yeni_kaynak = st.selectbox("Kaynak", ["Gmail", "App Store", "Banka", "Manuel"])
        if st.button("✓ Kaydet", use_container_width=True):
            if yeni_servis and yeni_tutar > 0:
                abonelik_ekle(yeni_servis, yeni_tutar, yeni_gun, yeni_kaynak)
                st.rerun()

    # Liste
    subs_html = ""
    for a in abonelikler:
        renk = tutar_renk(a["tutar_tl"])
        durum_icon = "✅" if a["durum"] == "aktif" else "⚠️"
        subs_html += f"""
        <div class="sub-row">
            {get_logo(a['servis'])}
            <div class="sub-info">
                <div class="sub-name">{a['servis']}</div>
                <div class="sub-detail">Her ayın {a['yenileme']}'i · {a['kaynak']} · {durum_icon}</div>
            </div>
            <div class="sub-amount" style="color:{renk}">₺{a['tutar_tl']:,.0f}</div>
        </div>"""

    st.markdown(f"""
    <div class="glass-panel">
        <div class="section-title"><span class="section-icon">☰</span> Tüm Abonelikler</div>
        {subs_html}
    </div>
    """, unsafe_allow_html=True)

    # Silme butonu
    st.markdown("<br>", unsafe_allow_html=True)
    col_del1, col_del2 = st.columns([3, 1])
    with col_del1:
        sil_secim = st.selectbox("Silmek istediğin aboneliği seç:", [f"{a['servis']} (₺{a['tutar_tl']:,.0f})" for a in abonelikler])
    with col_del2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Sil", use_container_width=True):
            idx = [f"{a['servis']} (₺{a['tutar_tl']:,.0f})" for a in abonelikler].index(sil_secim)
            abonelik_sil(abonelikler[idx]["id"])
            st.rerun()

# ===== TAB 3: ANALİZ =====
with tab3:
    if abonelikler:
        sirali = sorted(abonelikler, key=lambda x: x["tutar_tl"], reverse=True)
        en_pahali = sirali[0]
        en_ucuz = sirali[-1]

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.markdown(f"""
            <div style="background:rgba(239,68,68,0.06);border-radius:14px;padding:20px;border:1px solid rgba(239,68,68,0.1);display:flex;align-items:center;gap:14px">
                {get_logo(en_pahali['servis'])}
                <div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:rgba(239,68,68,0.6);letter-spacing:2px">EN PAHALI</div>
                    <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:#ef4444;margin-top:4px">{en_pahali['servis']}</div>
                    <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:800;color:#ef4444">₺{en_pahali['tutar_tl']:,.0f}/ay</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_a2:
            st.markdown(f"""
            <div style="background:rgba(94,234,212,0.06);border-radius:14px;padding:20px;border:1px solid rgba(94,234,212,0.1);display:flex;align-items:center;gap:14px">
                {get_logo(en_ucuz['servis'])}
                <div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:rgba(94,234,212,0.6);letter-spacing:2px">EN UCUZ</div>
                    <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:#5eead4;margin-top:4px">{en_ucuz['servis']}</div>
                    <div style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:800;color:#5eead4">₺{en_ucuz['tutar_tl']:,.0f}/ay</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Yüzdelik dağılım
        pct_html = ""
        hue_colors = ['#5eead4','#38bdf8','#a78bfa','#fb923c','#f472b6','#fbbf24','#34d399','#60a5fa']
        for i, a in enumerate(sirali):
            pct = (a["tutar_tl"] / toplam * 100)
            c = hue_colors[i % len(hue_colors)]
            pct_html += f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
                {get_logo(a['servis'])}
                <div style="flex:1">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                        <span style="font-family:'DM Sans',sans-serif;font-size:0.8rem;color:#94a3b8">{a['servis']}</span>
                        <span style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#5eead4">%{pct:.1f}</span>
                    </div>
                    <div style="height:8px;background:rgba(255,255,255,0.03);border-radius:4px;overflow:hidden">
                        <div style="height:100%;border-radius:4px;width:{pct}%;background:{c}"></div>
                    </div>
                </div>
            </div>"""

        st.markdown(f"""
        <div class="glass-panel">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:rgba(148,163,184,0.4);letter-spacing:2px;margin-bottom:12px">HARCAMA ORANLARI</div>
            {pct_html}
        </div>
        """, unsafe_allow_html=True)

        # Tasarruf ipucu
        max_pct = (en_pahali["tutar_tl"] / toplam * 100) if toplam > 0 else 0
        bekleyen_text = f' Ayrıca <strong style="color:#fb923c">{len(bekleyen)} aboneliğin</strong> ödeme durumu belirsiz.' if bekleyen else ''
        st.markdown(f"""
        <div style="padding:16px;background:rgba(94,234,212,0.03);border-radius:12px;border:1px solid rgba(94,234,212,0.06);margin-top:12px">
            <div style="font-family:'DM Sans',sans-serif;font-size:0.8rem;color:#94a3b8;margin-bottom:8px">💡 Tasarruf İpucu</div>
            <div style="font-family:'DM Sans',sans-serif;font-size:0.85rem;color:#e2e8f0;line-height:1.6">
                En pahalı aboneliğin toplam harcamanın <strong style="color:#ef4444">%{max_pct:.0f}</strong>'ini oluşturuyor.{bekleyen_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-text">BATUHAN ŞEN © 2026</div>
</div>
""", unsafe_allow_html=True)
