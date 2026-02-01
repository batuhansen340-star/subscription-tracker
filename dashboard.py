import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Abonelik Takipçi", page_icon="💰", layout="wide", initial_sidebar_state="collapsed")

# --- CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800;900&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

.stApp { background: linear-gradient(180deg, #020617 0%, #0a0f1e 50%, #020617 100%) !important; }
[data-testid="stSidebar"] { display: none; }
header[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 2rem !important; max-width: 1000px !important; }

@keyframes glow { 0%,100%{opacity:0.4} 50%{opacity:1} }
@keyframes slideUp { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }

.main-title { font-family:'Playfair Display',serif; font-size:2.2rem; font-weight:800; background:linear-gradient(90deg,#5eead4,#38bdf8); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:0; }
.subtitle { font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:rgba(148,163,184,0.4); margin-top:4px; }
.live-dot { display:inline-block; width:6px; height:6px; border-radius:50%; background:#5eead4; margin-right:4px; animation:glow 2s ease-in-out infinite; }

.metric-card { background:rgba(15,23,42,0.6); backdrop-filter:blur(16px); border:1px solid rgba(94,234,212,0.08); border-radius:16px; padding:20px 24px; position:relative; overflow:hidden; }
.metric-card::before { content:''; position:absolute; top:0;left:0;right:0; height:1px; background:linear-gradient(90deg,transparent,rgba(94,234,212,0.3),transparent); }
.metric-label { font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:rgba(148,163,184,0.5); letter-spacing:2px; margin-bottom:8px; }
.metric-value { font-family:'Playfair Display',serif; font-size:1.8rem; font-weight:800; line-height:1; }
.metric-sub { font-family:'DM Sans',sans-serif; font-size:0.7rem; color:rgba(148,163,184,0.4); margin-top:6px; }

.glass-panel { background:rgba(15,23,42,0.6); backdrop-filter:blur(20px); border:1px solid rgba(94,234,212,0.08); border-radius:20px; padding:24px; margin-bottom:16px; }
.section-title { font-family:'DM Sans',sans-serif; font-size:1rem; font-weight:600; color:#e2e8f0; margin-bottom:16px; }

.brand-logo { width:36px; height:36px; border-radius:10px; display:inline-flex; align-items:center; justify-content:center; font-weight:800; font-size:16px; color:white; flex-shrink:0; }

.renewal-row { display:flex; justify-content:space-between; align-items:center; padding:12px 16px; margin-bottom:8px; background:rgba(255,255,255,0.02); border-radius:0 12px 12px 0; }
.renewal-name { font-family:'DM Sans',sans-serif; font-weight:600; color:#e2e8f0; font-size:0.9rem; }
.renewal-detail { font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:rgba(148,163,184,0.5); margin-top:2px; }
.renewal-amount { font-family:'Playfair Display',serif; font-weight:700; font-size:1.1rem; }

.sub-row { display:flex; align-items:center; gap:14px; padding:14px 18px; margin-bottom:6px; background:rgba(15,23,42,0.3); border:1px solid rgba(94,234,212,0.04); border-radius:14px; }
.sub-name { font-family:'DM Sans',sans-serif; font-weight:600; color:#e2e8f0; font-size:0.95rem; }
.sub-detail { font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:rgba(148,163,184,0.4); margin-top:1px; }
.sub-amount { font-family:'Playfair Display',serif; font-weight:700; font-size:1.15rem; min-width:80px; text-align:right; }

.bar-container { margin-bottom:14px; }
.bar-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:5px; }
.bar-name { font-family:'DM Sans',sans-serif; font-size:0.8rem; color:#94a3b8; }
.bar-value { font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#5eead4; }
.bar-track { height:6px; background:rgba(255,255,255,0.03); border-radius:3px; overflow:hidden; }
.bar-fill { height:100%; border-radius:3px; }

.source-box { background:rgba(94,234,212,0.04); border:1px solid rgba(94,234,212,0.06); border-radius:10px; padding:10px 14px; flex:1; }
.source-label { font-family:'DM Sans',sans-serif; font-size:0.7rem; color:rgba(148,163,184,0.5); }
.source-value { font-family:'Playfair Display',serif; font-weight:700; font-size:1.1rem; color:#5eead4; margin-top:2px; }

.footer-text { font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:rgba(148,163,184,0.2); letter-spacing:1px; text-align:right; margin-top:32px; padding-top:20px; border-top:1px solid rgba(94,234,212,0.04); }

.stTabs [data-baseweb="tab-list"] { background:rgba(15,23,42,0.4); border-radius:12px; padding:4px; border:1px solid rgba(94,234,212,0.06); gap:4px; }
.stTabs [data-baseweb="tab"] { font-family:'DM Sans',sans-serif !important; font-size:0.8rem !important; font-weight:500 !important; color:rgba(148,163,184,0.7) !important; border-radius:10px !important; padding:8px 20px !important; }
.stTabs [aria-selected="true"] { background:rgba(94,234,212,0.08) !important; color:#5eead4 !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display:none; }

.stButton > button { background:rgba(94,234,212,0.08) !important; border:1px solid rgba(94,234,212,0.15) !important; border-radius:10px !important; color:#5eead4 !important; font-family:'DM Sans',sans-serif !important; }
.stButton > button:hover { background:rgba(94,234,212,0.15) !important; }
.streamlit-expanderHeader { background:rgba(15,23,42,0.4) !important; border:1px solid rgba(94,234,212,0.08) !important; border-radius:12px !important; color:#5eead4 !important; }
div[data-testid="stStatusWidget"] { display:none; }
::-webkit-scrollbar { width:4px; } ::-webkit-scrollbar-thumb { background:rgba(94,234,212,0.2); border-radius:4px; }
</style>
""", unsafe_allow_html=True)

# --- CSS Logo sistemi (SVG yerine) ---
BRAND_COLORS = {
    "Claude Max 5x": ("#D97757", "C"),
    "Eleven Labs": ("#1a1a2e", "II"),
    "ZeroGPT": ("#6C3CE1", "Z"),
    "Canva Pro": ("#00C4CC", "C"),
    "YouTube Premium": ("#FF0000", "▶"),
    "Teuida Languages": ("#FF6B35", "T"),
    "Zero Fasting": ("#FF4757", "⏱"),
    "Spotify": ("#1DB954", "♫"),
    "Netflix": ("#E50914", "N"),
    "ChatGPT": ("#10A37F", "G"),
}

def get_logo_html(name, size=36):
    if name in BRAND_COLORS:
        bg, letter = BRAND_COLORS[name]
    else:
        colors = ['#5eead4','#38bdf8','#a78bfa','#fb923c','#f472b6','#34d399']
        bg = colors[sum(ord(c) for c in name) % len(colors)]
        letter = name[0].upper()
    return f'<div class="brand-logo" style="width:{size}px;height:{size}px;background:{bg};font-size:{int(size*0.4)}px">{letter}</div>'

def tutar_renk(t):
    return "#ef4444" if t > 1000 else "#fb923c" if t > 300 else "#5eead4"

def bar_renk(t):
    return "#ef4444" if t > 1000 else "#fb923c" if t > 300 else "#5eead4"

# --- Veritabanı ---
DB_PATH = "abonelikler.db"

def baglanti_kur():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def tablo_olustur():
    conn = baglanti_kur()
    conn.execute("""CREATE TABLE IF NOT EXISTS abonelikler (
        id INTEGER PRIMARY KEY AUTOINCREMENT, servis TEXT NOT NULL,
        tutar_tl REAL NOT NULL, yenileme INTEGER NOT NULL,
        durum TEXT DEFAULT 'aktif', kaynak TEXT DEFAULT 'Manuel',
        eklenme_tarihi TEXT DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    if conn.execute("SELECT COUNT(*) FROM abonelikler").fetchone()[0] == 0:
        for v in [("Claude Max 5x",3150,5,"aktif","Gmail"),("Eleven Labs",215,7,"aktif","Gmail"),
                   ("ZeroGPT",360,18,"aktif","Gmail"),("Canva Pro",470,12,"bekliyor","Gmail"),
                   ("YouTube Premium",65,28,"aktif","App Store"),("Teuida Languages",50,7,"aktif","App Store"),
                   ("Zero Fasting",80,16,"aktif","App Store"),("Spotify",60,30,"aktif","App Store")]:
            conn.execute("INSERT INTO abonelikler (servis,tutar_tl,yenileme,durum,kaynak) VALUES (?,?,?,?,?)", v)
        conn.commit()
    conn.close()

def abonelikleri_getir():
    conn = baglanti_kur()
    rows = conn.execute("SELECT * FROM abonelikler ORDER BY tutar_tl DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def abonelik_ekle(servis, tutar, yenileme, kaynak):
    conn = baglanti_kur()
    conn.execute("INSERT INTO abonelikler (servis,tutar_tl,yenileme,kaynak) VALUES (?,?,?,?)", (servis,tutar,yenileme,kaynak))
    conn.commit(); conn.close()

def abonelik_sil(id):
    conn = baglanti_kur()
    conn.execute("DELETE FROM abonelikler WHERE id=?", (id,))
    conn.commit(); conn.close()

tablo_olustur()

# --- Header ---
now = datetime.now()
st.markdown(f"""
<div style="margin-bottom:28px">
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
max_tutar = max((a["tutar_tl"] for a in abonelikler), default=1)

yaklasan = []
for a in abonelikler:
    fark = a["yenileme"] - bugun
    if fark < 0: fark += 30
    if fark <= 7: yaklasan.append({**a, "fark": fark})
yaklasan.sort(key=lambda x: x["fark"])

tab1, tab2, tab3 = st.tabs(["◐  GENEL", "☰  LİSTE", "◑  ANALİZ"])

# ===== GENEL =====
with tab1:
    cols = st.columns(4)
    for col, (label, value, color, sub) in zip(cols, [
        ("AYLIK TOPLAM", f"₺{toplam:,.0f}", "#5eead4", f"{len(abonelikler)} abonelik"),
        ("YILLIK TOPLAM", f"₺{toplam*12:,.0f}", "#38bdf8", "Projeksiyon"),
        ("AKTİF", f"{len(aktif)} servis", "#a78bfa", f"{len(bekleyen)} bekleyen"),
        ("BU HAFTA", f"₺{sum(a['tutar_tl'] for a in yaklasan):,.0f}", "#fb923c", f"{len(yaklasan)} yenileme"),
    ]):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value" style="color:{color}">{value}</div><div class="metric-sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        html = ""
        if yaklasan:
            for a in yaklasan:
                c = "#ef4444" if a["fark"]<=1 else "#fb923c" if a["fark"]<=3 else "#5eead4"
                gt = "BUGÜN" if a["fark"]==0 else f"{a['fark']} gün sonra"
                html += f'<div class="renewal-row" style="border-left:3px solid {c}"><div style="display:flex;align-items:center;gap:12px">{get_logo_html(a["servis"])}<div><div class="renewal-name">{a["servis"]}</div><div class="renewal-detail">{gt} · Ayın {a["yenileme"]}\'i</div></div></div><div class="renewal-amount" style="color:{c}">₺{a["tutar_tl"]:,.0f}</div></div>'
        else:
            html = '<div style="text-align:center;padding:40px;color:rgba(148,163,184,0.3)"><div style="font-size:40px;margin-bottom:12px">✨</div><p>Bu hafta yenileme yok</p></div>'
        st.markdown(f'<div class="glass-panel"><div class="section-title">◔ Yaklaşan Yenilemeler</div>{html}</div>', unsafe_allow_html=True)

    with col_r:
        bars = ""
        for a in sorted(abonelikler, key=lambda x: x["tutar_tl"], reverse=True):
            pct = (a["tutar_tl"]/max_tutar)*100
            bars += f'<div class="bar-container"><div class="bar-header"><span class="bar-name">{a["servis"]}</span><span class="bar-value">₺{a["tutar_tl"]:,.0f}</span></div><div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:{bar_renk(a["tutar_tl"])}"></div></div></div>'

        kaynaklar = {}
        for a in abonelikler: kaynaklar[a["kaynak"]] = kaynaklar.get(a["kaynak"], 0) + a["tutar_tl"]
        src = "".join(f'<div class="source-box"><div class="source-label">{k}</div><div class="source-value">₺{v:,.0f}</div></div>' for k,v in kaynaklar.items())

        st.markdown(f'<div class="glass-panel"><div class="section-title">◑ Harcama Dağılımı</div>{bars}<div style="margin-top:20px;padding-top:16px;border-top:1px solid rgba(94,234,212,0.06);display:flex;gap:12px">{src}</div></div>', unsafe_allow_html=True)

# ===== LİSTE =====
with tab2:
    with st.expander("➕ Yeni Abonelik Ekle"):
        c1,c2,c3,c4 = st.columns(4)
        with c1: yeni_servis = st.text_input("Servis Adı", placeholder="Netflix...")
        with c2: yeni_tutar = st.number_input("Aylık ₺", min_value=0, step=10)
        with c3: yeni_gun = st.number_input("Yenileme Günü", min_value=1, max_value=30, value=15)
        with c4: yeni_kaynak = st.selectbox("Kaynak", ["Gmail","App Store","Banka","Manuel"])
        if st.button("✓ Kaydet", use_container_width=True):
            if yeni_servis and yeni_tutar > 0:
                abonelik_ekle(yeni_servis, yeni_tutar, yeni_gun, yeni_kaynak)
                st.rerun()

    subs_html = ""
    for a in abonelikler:
        c = tutar_renk(a["tutar_tl"])
        d = "✅" if a["durum"]=="aktif" else "⚠️"
        subs_html += f'<div class="sub-row">{get_logo_html(a["servis"])}<div style="flex:1"><div class="sub-name">{a["servis"]}</div><div class="sub-detail">Ayın {a["yenileme"]}\'i · {a["kaynak"]} · {d}</div></div><div class="sub-amount" style="color:{c}">₺{a["tutar_tl"]:,.0f}</div></div>'
    st.markdown(f'<div class="glass-panel"><div class="section-title">☰ Tüm Abonelikler</div>{subs_html}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([3,1])
    with c1: sil_secim = st.selectbox("Silmek istediğin:", [f"{a['servis']} (₺{a['tutar_tl']:,.0f})" for a in abonelikler])
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Sil", use_container_width=True):
            idx = [f"{a['servis']} (₺{a['tutar_tl']:,.0f})" for a in abonelikler].index(sil_secim)
            abonelik_sil(abonelikler[idx]["id"])
            st.rerun()

# ===== ANALİZ =====
with tab3:
    if abonelikler:
        sirali = sorted(abonelikler, key=lambda x: x["tutar_tl"], reverse=True)
        ep, eu = sirali[0], sirali[-1]

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div style="background:rgba(239,68,68,0.06);border-radius:14px;padding:20px;border:1px solid rgba(239,68,68,0.1);display:flex;align-items:center;gap:14px">{get_logo_html(ep["servis"],48)}<div><div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;color:rgba(239,68,68,0.6);letter-spacing:2px">EN PAHALI</div><div style="font-family:\'Playfair Display\',serif;font-size:1.1rem;font-weight:700;color:#ef4444;margin-top:4px">{ep["servis"]}</div><div style="font-family:\'Playfair Display\',serif;font-size:1.5rem;font-weight:800;color:#ef4444">₺{ep["tutar_tl"]:,.0f}/ay</div></div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div style="background:rgba(94,234,212,0.06);border-radius:14px;padding:20px;border:1px solid rgba(94,234,212,0.1);display:flex;align-items:center;gap:14px">{get_logo_html(eu["servis"],48)}<div><div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;color:rgba(94,234,212,0.6);letter-spacing:2px">EN UCUZ</div><div style="font-family:\'Playfair Display\',serif;font-size:1.1rem;font-weight:700;color:#5eead4;margin-top:4px">{eu["servis"]}</div><div style="font-family:\'Playfair Display\',serif;font-size:1.5rem;font-weight:800;color:#5eead4">₺{eu["tutar_tl"]:,.0f}/ay</div></div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        hue = ['#5eead4','#38bdf8','#a78bfa','#fb923c','#f472b6','#fbbf24','#34d399','#60a5fa']
        pct_html = ""
        for i, a in enumerate(sirali):
            p = a["tutar_tl"]/toplam*100
            c = hue[i%len(hue)]
            pct_html += f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">{get_logo_html(a["servis"],28)}<div style="flex:1"><div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="font-family:\'DM Sans\',sans-serif;font-size:0.8rem;color:#94a3b8">{a["servis"]}</span><span style="font-family:\'JetBrains Mono\',monospace;font-size:0.75rem;color:#5eead4">%{p:.1f}</span></div><div style="height:8px;background:rgba(255,255,255,0.03);border-radius:4px;overflow:hidden"><div style="height:100%;border-radius:4px;width:{p}%;background:{c}"></div></div></div></div>'

        st.markdown(f'<div class="glass-panel"><div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;color:rgba(148,163,184,0.4);letter-spacing:2px;margin-bottom:12px">HARCAMA ORANLARI</div>{pct_html}</div>', unsafe_allow_html=True)

        mp = ep["tutar_tl"]/toplam*100 if toplam>0 else 0
        bt = f' Ayrıca <strong style="color:#fb923c">{len(bekleyen)} aboneliğin</strong> ödeme durumu belirsiz.' if bekleyen else ''
        st.markdown(f'<div style="padding:16px;background:rgba(94,234,212,0.03);border-radius:12px;border:1px solid rgba(94,234,212,0.06)"><div style="font-family:\'DM Sans\',sans-serif;font-size:0.8rem;color:#94a3b8;margin-bottom:8px">💡 Tasarruf İpucu</div><div style="font-family:\'DM Sans\',sans-serif;font-size:0.85rem;color:#e2e8f0;line-height:1.6">En pahalı aboneliğin toplam harcamanın <strong style="color:#ef4444">%{mp:.0f}</strong>\'ini oluşturuyor.{bt}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="footer-text">BATUHAN ŞEN © 2026</div>', unsafe_allow_html=True)
