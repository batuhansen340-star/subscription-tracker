# abonelikler.py
# Gerçek abonelik verilerini yönet

from datetime import datetime

abonelikler = [
    {
        "servis": "Claude Max 5x",
        "tutar_usd": 87.93,
        "tutar_tl": 3150,
        "periyot": "aylik",
        "yenileme": "05",
        "durum": "aktif"
    },
    {
        "servis": "Eleven Labs",
        "tutar_usd": 6.00,
        "tutar_tl": 215,
        "periyot": "aylik",
        "yenileme": "07",
        "durum": "aktif"
    },
    {
        "servis": "ZeroGPT",
        "tutar_usd": 9.99,
        "tutar_tl": 360,
        "periyot": "aylik",
        "yenileme": "18",
        "durum": "aktif"
    },
    {
        "servis": "Canva Pro",
        "tutar_usd": 12.99,
        "tutar_tl": 470,
        "periyot": "aylik",
        "yenileme": "12",
        "durum": "odeme_bekliyor"
    },
    {
        "servis": "YouTube Premium Lite",
        "tutar_usd": None,
        "tutar_tl": 57,
        "periyot": "aylik",
        "yenileme": "30",
        "durum": "aktif"
    },
]

# Hesaplamalar
toplam_tl = sum(a["tutar_tl"] for a in abonelikler)
aktif = [a for a in abonelikler if a["durum"] == "aktif"]
bekleyen = [a for a in abonelikler if a["durum"] == "odeme_bekliyor"]

print("=" * 50)
print("📊 ABONELİK ÖZETİ")
print("=" * 50)

for a in abonelikler:
    status = "✅" if a["durum"] == "aktif" else "⚠️"
    print(f"{status} {a['servis']}: ₺{a['tutar_tl']}/ay (her ayın {a['yenileme']}'i)")

print("=" * 50)
print(f"💰 AYLIK TOPLAM: ₺{toplam_tl}")
print(f"📅 YILLIK: ₺{toplam_tl * 12:,}")
print(f"✅ Aktif: {len(aktif)} | ⚠️ Bekleyen: {len(bekleyen)}")
print("=" * 50)

# Yaklaşan yenilemeler
print("\n📅 YAKLASAN YENİLEMELER (7 gün)")
print("-" * 50)

bugun = datetime.now().day
yaklasan = []

for a in abonelikler:
    yenileme_gunu = int(a["yenileme"])
    fark = yenileme_gunu - bugun
    
    if 0 <= fark <= 7:
        yaklasan.append((a, fark))
    elif fark < 0 and (fark + 30) <= 7:
        yaklasan.append((a, fark + 30))

if yaklasan:
    for a, gun in sorted(yaklasan, key=lambda x: x[1]):
        if gun == 0:
            print(f"🔴 BUGÜN: {a['servis']} - ₺{a['tutar_tl']}")
        else:
            print(f"🟡 {gun} gün sonra: {a['servis']} - ₺{a['tutar_tl']}")
else:
    print("✅ Bu hafta yenilenecek abonelik yok.")