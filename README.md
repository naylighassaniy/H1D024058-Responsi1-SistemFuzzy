# BuyWise — Sistem Fuzzy Mamdani
> Penentu Kelayakan Pembelian Barang berbasis Logika Fuzzy Mamdani

---

## 📁 Struktur Project

```
buywise/
├── app.py              ← Entry point Flask
├── fuzzy_engine.py     ← Logika fuzzy Mamdani (murni Python)
├── requirements.txt    ← Dependencies
├── vercel.json         ← Konfigurasi deploy Vercel
├── templates/
│   └── index.html      ← Tampilan utama (Jinja2)
└── static/
    ├── css/
    │   └── style.css   ← Semua styling
    └── js/
        └── main.js     ← Frontend logic (fetch API)
```

---

## 🚀 Cara Menjalankan Lokal (VS Code)

### 1. Buka project di VS Code
```bash
cd buywise
```

### 2. Buat virtual environment
```bash
python -m venv venv
```

### 3. Aktifkan virtual environment
```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Jalankan Flask
```bash
python app.py
```

### 6. Buka di browser
```
http://127.0.0.1:5000
```

---

## ☁️ Cara Deploy ke Vercel

### Prasyarat
- Akun [Vercel](https://vercel.com) (gratis)
- Akun [GitHub](https://github.com)
- [Vercel CLI](https://vercel.com/docs/cli) (opsional)

---

### Langkah 1 — Upload project ke GitHub

1. Buka [github.com](https://github.com) → **New repository**
2. Beri nama repo, misal: `buywise-fuzzy`
3. Klik **Create repository**
4. Di terminal VS Code, jalankan:

```bash
git init
git add .
git commit -m "first commit: BuyWise Fuzzy Mamdani"
git branch -M main
git remote add origin https://github.com/USERNAME/buywise-fuzzy.git
git push -u origin main
```

> Ganti `USERNAME` dengan username GitHub kamu.

---

### Langkah 2 — Import ke Vercel

1. Buka [vercel.com](https://vercel.com) → Login
2. Klik **Add New → Project**
3. Pilih repository `buywise-fuzzy` dari GitHub
4. Klik **Import**
5. Pada bagian **Framework Preset** → pilih **Other**
6. Klik **Deploy**

Vercel akan otomatis mendeteksi `vercel.json` dan mendeploy Flask app kamu.

---

### Langkah 3 — Selesai! 🎉

Setelah deploy berhasil, kamu akan mendapatkan URL seperti:
```
https://buywise-fuzzy.vercel.app
```

URL ini bisa langsung dikumpulkan ke form responsi!

---

## 🔁 Update Setelah Deploy

Setiap kali kamu push ke GitHub, Vercel akan otomatis redeploy:
```bash
git add .
git commit -m "update: ..."
git push
```

---

## 🧠 Tentang Sistem

| Komponen     | Detail                              |
|--------------|-------------------------------------|
| Metode       | Fuzzy Mamdani                       |
| Input 1      | Rasio Harga/Saldo (0–100%)          |
| Input 2      | Frekuensi Pemakaian (0–7 kali/minggu)|
| Input 3      | Urgensi Kebutuhan (1–10)            |
| Fungsi MF    | Segitiga & Trapesium                |
| Rule Base    | 14 aturan IF-THEN                   |
| Defuzzifikasi| Centroid (Weighted Average)         |
| Output       | Jangan Beli / Pertimbangkan / Layak |
