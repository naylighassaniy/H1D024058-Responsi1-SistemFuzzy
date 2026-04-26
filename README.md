# BuyWise — Sistem Fuzzy Mamdani
### Penentu Kelayakan Pembelian Barang

> Dibuat sebagai bagian dari Responsi Kecerdasan Buatan — Semester 4

---

## 🌸 Tentang Aplikasi

**BuyWise** adalah sistem berbasis logika fuzzy yang membantu kamu mengevaluasi apakah sebuah pembelian layak dilakukan atau hanya sekadar keinginan sesaat. Cukup masukkan tiga informasi sederhana, dan sistem akan memberikan rekomendasi berdasarkan analisis fuzzy secara otomatis.

Aplikasi ini dibangun dengan pendekatan **Fuzzy Mamdani** — salah satu metode inferensi fuzzy paling populer yang meniru cara manusia berpikir dalam kondisi yang tidak pasti.

---

## 🧠 Penjelasan Sistem

### Apa itu Logika Fuzzy?

Logika fuzzy adalah cabang kecerdasan buatan yang memungkinkan komputer berpikir dalam kondisi **tidak pasti atau abu-abu** — seperti manusia. Tidak semua keputusan bisa dijawab "ya" atau "tidak"; logika fuzzy menjembatani kondisi di antaranya.

Contoh: apakah harga Rp150.000 itu "murah" atau "mahal"? Jawabannya tergantung konteks. Logika fuzzy menangani ketidakpastian ini dengan **derajat keanggotaan** (nilai 0 hingga 1).

---

### Metode: Mamdani

Sistem ini menggunakan **Metode Inferensi Mamdani**, yang terdiri dari empat tahap utama:

```
Input Numerik → Fuzzifikasi → Inferensi Rule → Defuzzifikasi → Output Numerik
```

**1. Fuzzifikasi**
Nilai input numerik diubah menjadi derajat keanggotaan dalam himpunan fuzzy menggunakan fungsi keanggotaan **segitiga** dan **trapesium**.

**2. Inferensi Rule (Rule Base)**
Sistem memiliki **14 aturan IF-THEN** yang meniru penalaran pakar. Setiap rule dievaluasi menggunakan operator MIN (AND), dan hasilnya digabungkan dengan operator MAX.

**3. Defuzzifikasi**
Output fuzzy diubah kembali menjadi nilai numerik menggunakan metode **Centroid (Weighted Average)**:

```
z* = Σ(wi × ci) / Σ(wi)
```

di mana `wi` adalah bobot rule yang aktif dan `ci` adalah centroid himpunan output.

---

### Variabel Input

| Variabel | Rentang | Himpunan Fuzzy |
|---|---|---|
| Rasio Harga / Saldo | 0 – 100% | Rendah, Sedang, Tinggi |
| Frekuensi Pemakaian | 0 – 7 kali/minggu | Jarang, Kadang, Sering |
| Urgensi Kebutuhan | 1 – 10 | Rendah, Sedang, Tinggi |

### Variabel Output

| Kategori | Rentang Skor | Centroid |
|---|---|---|
| Jangan Beli | 0 – 30 | 15 |
| Pertimbangkan | 20 – 60 | 40 |
| Layak Dibeli | 60 – 100 | 80 |

---

### Fungsi Keanggotaan

**Fungsi Trapesium** — digunakan untuk himpunan di tepi (Rendah & Tinggi):
```
         _______
        /       \
_______/         \_______
   a   b         c   d
```

**Fungsi Segitiga** — digunakan untuk himpunan di tengah (Sedang):
```
           /\
          /  \
_________/    \_________
     a    b    c
```

---

### Contoh Rule

```
R1 : IF harga TINGGI AND frekuensi JARANG AND urgensi RENDAH  → JANGAN BELI
R5 : IF harga TINGGI AND frekuensi SERING AND urgensi TINGGI  → LAYAK DIBELI
R9 : IF harga SEDANG AND frekuensi KADANG AND urgensi TINGGI  → LAYAK DIBELI
R11: IF harga RENDAH AND frekuensi KADANG AND urgensi SEDANG  → LAYAK DIBELI
```

Total: **14 aturan IF-THEN**

---

## 🛠️ Teknologi yang Digunakan

| Komponen | Teknologi |
|---|---|
| Backend | Python + Flask |
| Frontend | HTML, CSS, JavaScript |
| Template Engine | Jinja2 |
| Hosting | Vercel |
| Logika Fuzzy | Implementasi manual (tanpa library eksternal) |

---

## 📁 Struktur Project

```
buywise/
├── app.py              ← Entry point Flask & routing API
├── fuzzy_engine.py     ← Implementasi logika Fuzzy Mamdani
├── requirements.txt    ← Daftar dependencies Python
├── vercel.json         ← Konfigurasi hosting Vercel
├── templates/
│   └── index.html      ← Halaman utama (Jinja2)
└── static/
    ├── css/style.css   ← Styling antarmuka
    └── js/main.js      ← Logika frontend & komunikasi API
```

---

## 🔗 Cara Menggunakan Aplikasi

1. Buka aplikasi melalui link yang tersedia
2. Atur **slider Rasio Harga** — seberapa besar harga barang dibanding saldo kamu
3. Atur **slider Frekuensi Pemakaian** — seberapa sering kamu akan memakai barang ini
4. Atur **slider Urgensi** — seberapa mendesak kebutuhan kamu terhadap barang ini
5. Klik tombol **"Cek Sekarang"**
6. Sistem akan menampilkan:
   - Rekomendasi keputusan (Jangan Beli / Pertimbangkan / Layak Dibeli)
   - Skor kelayakan 0–100
   - Nilai keanggotaan fuzzy tiap variabel
   - Saran yang relevan
Link: buywise-fuzzy.vercel.app

*Responsi Kecerdasan Buatan 2026*
