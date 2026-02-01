# veritabani.py
# SQLite veritabanı yönetimi

import sqlite3

def baglanti_kur():
    """Veritabanına bağlan, tablo yoksa oluştur"""
    conn = sqlite3.connect("abonelikler.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS abonelikler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servis TEXT NOT NULL,
            tutar_tl REAL NOT NULL,
            yenileme INTEGER NOT NULL,
            durum TEXT DEFAULT 'aktif',
            kaynak TEXT DEFAULT 'Manuel',
            eklenme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def abonelik_ekle(servis, tutar_tl, yenileme, kaynak="Manuel"):
    conn = baglanti_kur()
    conn.execute(
        "INSERT INTO abonelikler (servis, tutar_tl, yenileme, kaynak) VALUES (?, ?, ?, ?)",
        (servis, tutar_tl, yenileme, kaynak)
    )
    conn.commit()
    conn.close()

def abonelik_sil(id):
    conn = baglanti_kur()
    conn.execute("DELETE FROM abonelikler WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def abonelikleri_getir():
    conn = baglanti_kur()
    cursor = conn.execute("SELECT id, servis, tutar_tl, yenileme, durum, kaynak FROM abonelikler")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {"id": r[0], "servis": r[1], "tutar_tl": r[2], "yenileme": r[3], "durum": r[4], "kaynak": r[5]}
        for r in rows
    ]

def baslangic_verisi_yukle():
    """İlk çalıştırmada mevcut abonelikleri ekle"""
    conn = baglanti_kur()
    cursor = conn.execute("SELECT COUNT(*) FROM abonelikler")
    
    if cursor.fetchone()[0] == 0:
        veriler = [
            ("Claude Max 5x", 3150, 5, "Gmail"),
            ("Eleven Labs", 215, 7, "Gmail"),
            ("ZeroGPT", 360, 18, "Gmail"),
            ("Canva Pro", 470, 12, "Gmail"),
            ("YouTube Premium", 65, 28, "App Store"),
            ("Teuida Languages", 50, 7, "App Store"),
            ("Zero Fasting", 80, 16, "App Store"),
        ]
        conn.executemany(
            "INSERT INTO abonelikler (servis, tutar_tl, yenileme, kaynak) VALUES (?, ?, ?, ?)",
            veriler
        )
        conn.commit()
        print("✅ Başlangıç verileri yüklendi!")
    
    conn.close()

# Test
if __name__ == "__main__":
    baslangic_verisi_yukle()
    for a in abonelikleri_getir():
        print(f"{a['servis']}: ₺{a['tutar_tl']}/ay")
