# ============================================================
#  fuzzy_engine.py
#  Implementasi Sistem Fuzzy Mamdani — BuyWise
#  Metode  : Mamdani
#  Defuzz  : Centroid (Weighted Average)
# ============================================================


class FuzzyEngine:
    """Mesin inferensi fuzzy Mamdani untuk kelayakan pembelian barang."""

    # ----------------------------------------------------------
    # FUNGSI KEANGGOTAAN
    # ----------------------------------------------------------

    def _trap(self, x: float, a: float, b: float, c: float, d: float) -> float:
        """Fungsi keanggotaan trapesium."""
        if x <= a or x >= d:
            return 0.0
        if b <= x <= c:
            return 1.0
        if x < b:
            return (x - a) / (b - a)
        return (d - x) / (d - c)

    def _tri(self, x: float, a: float, b: float, c: float) -> float:
        """Fungsi keanggotaan segitiga."""
        if x <= a or x >= c:
            return 0.0
        if x == b:
            return 1.0
        if x < b:
            return (x - a) / (b - a)
        return (c - x) / (c - b)

    # ----------------------------------------------------------
    # FUZZIFIKASI — INPUT 1: Rasio Harga/Saldo (0–100)
    # ----------------------------------------------------------

    def _mf_harga(self, x: float) -> dict:
        return {
            "rendah": self._trap(x, 0,  0,  20, 40),
            "sedang": self._tri( x, 20, 50, 80),
            "tinggi": self._trap(x, 60, 80, 100, 100),
        }

    # ----------------------------------------------------------
    # FUZZIFIKASI — INPUT 2: Frekuensi Pemakaian (0–7)
    # ----------------------------------------------------------

    def _mf_frekuensi(self, x: float) -> dict:
        return {
            "jarang": self._trap(x, 0,   0,   1, 3),
            "kadang": self._tri( x, 1,   3.5, 6),
            "sering": self._trap(x, 4,   6,   7, 7),
        }

    # ----------------------------------------------------------
    # FUZZIFIKASI — INPUT 3: Urgensi Kebutuhan (1–10)
    # ----------------------------------------------------------

    def _mf_urgensi(self, x: float) -> dict:
        return {
            "rendah": self._trap(x, 1, 1, 3,  5),
            "sedang": self._tri( x, 3, 5.5, 8),
            "tinggi": self._trap(x, 6, 8, 10, 10),
        }

    # ----------------------------------------------------------
    # INFERENSI — Rule Base (14 rules)
    # ----------------------------------------------------------

    def _inference(self, h: dict, f: dict, u: dict) -> dict:
        """
        Evaluasi rule base Mamdani.
        Output himpunan: jangan (0–30) | pertimbangkan (20–60) | layak (60–100)
        """
        ro = {"jangan": 0.0, "pertimbangkan": 0.0, "layak": 0.0}

        def fire(output: str, *inputs: float):
            alpha = min(inputs)
            ro[output] = max(ro[output], alpha)

        # --- Harga TINGGI ---
        fire("jangan",          h["tinggi"], f["jarang"], u["rendah"])
        fire("jangan",          h["tinggi"], f["jarang"], u["sedang"])
        fire("pertimbangkan",   h["tinggi"], f["kadang"], u["sedang"])
        fire("pertimbangkan",   h["tinggi"], f["sering"], u["sedang"])
        fire("layak",           h["tinggi"], f["sering"], u["tinggi"])

        # --- Harga SEDANG ---
        fire("jangan",          h["sedang"], f["jarang"], u["rendah"])
        fire("pertimbangkan",   h["sedang"], f["jarang"], u["sedang"])
        fire("pertimbangkan",   h["sedang"], f["kadang"], u["sedang"])
        fire("layak",           h["sedang"], f["sering"], u["tinggi"])
        fire("layak",           h["sedang"], f["kadang"], u["tinggi"])

        # --- Harga RENDAH ---
        fire("pertimbangkan",   h["rendah"], f["jarang"], u["rendah"])
        fire("layak",           h["rendah"], f["kadang"], u["sedang"])
        fire("layak",           h["rendah"], f["sering"], u["tinggi"])
        fire("layak",           h["rendah"], f["sering"], u["sedang"])

        return ro

    # ----------------------------------------------------------
    # DEFUZZIFIKASI — Centroid (Weighted Average)
    # ----------------------------------------------------------

    def _defuzzify(self, ro: dict) -> float:
        centroids = {"jangan": 15.0, "pertimbangkan": 40.0, "layak": 80.0}
        num = sum(w * centroids[k] for k, w in ro.items())
        den = sum(ro.values())
        return round(num / den, 2) if den > 0 else 50.0

    # ----------------------------------------------------------
    # INTERPRETASI OUTPUT
    # ----------------------------------------------------------

    def _interpret(self, score: float) -> dict:
        if score < 33:
            return {
                "verdict":  "Jangan Beli!",
                "emoji":    "🚫",
                "color":    "#e05070",
                "kategori": "jangan",
                "deskripsi": (
                    f"Skor kelayakan kamu adalah <strong>{score}/100</strong> — cukup rendah. "
                    "Harga barang ini relatif besar dibanding saldo dan frekuensi pemakaiannya rendah. "
                    "Lebih baik tahan dulu!"
                ),
                "tips": [
                    "Tunggu minimal 48 jam sebelum memutuskan beli — teknik anti-impulsif yang efektif.",
                    "Simpan uangnya dulu, beli setelah kamu benar-benar membutuhkan.",
                    "Cari alternatif yang lebih terjangkau atau pinjam dari teman dulu.",
                ],
            }
        elif score < 65:
            return {
                "verdict":  "Pertimbangkan Dulu",
                "emoji":    "🤔",
                "color":    "#d4891a",
                "kategori": "pertimbangkan",
                "deskripsi": (
                    f"Skor kelayakan kamu adalah <strong>{score}/100</strong> — berada di zona abu-abu. "
                    "Ada faktor yang mendukung, tapi ada juga yang perlu dipikirkan lebih matang."
                ),
                "tips": [
                    "Tanyakan pada diri: 'Apakah aku akan menyesal jika tidak beli ini bulan depan?'",
                    "Cek apakah ada promo atau cicilan yang lebih ringan.",
                    "Prioritaskan kebutuhan lain yang mungkin lebih mendesak saat ini.",
                ],
            }
        else:
            return {
                "verdict":  "Layak Dibeli!",
                "emoji":    "✨",
                "color":    "#2d9e6b",
                "kategori": "layak",
                "deskripsi": (
                    f"Skor kelayakan kamu adalah <strong>{score}/100</strong> — cukup tinggi! "
                    "Barang ini sering dipakai, harganya proporsional, dan urgensinya ada. Go ahead!"
                ),
                "tips": [
                    "Pastikan masih ada dana darurat tersisa setelah membeli barang ini.",
                    "Beli dari toko terpercaya dan cek review produknya dulu.",
                    "Catat pengeluaran ini supaya keuangan tetap terpantau.",
                ],
            }

    # ----------------------------------------------------------
    # PUBLIC — Evaluasi lengkap
    # ----------------------------------------------------------

    def evaluate(self, rasio: float, frekuensi: float, urgensi: float) -> dict:
        """
        Jalankan pipeline fuzzy Mamdani secara lengkap.

        Parameters
        ----------
        rasio      : Rasio harga/saldo (0–100)
        frekuensi  : Frekuensi pemakaian per minggu (0–7)
        urgensi    : Tingkat urgensi kebutuhan (1–10)

        Returns
        -------
        dict berisi skor, nilai keanggotaan, output rule, dan interpretasi.
        """
        h = self._mf_harga(rasio)
        f = self._mf_frekuensi(frekuensi)
        u = self._mf_urgensi(urgensi)

        rule_outputs = self._inference(h, f, u)
        score        = self._defuzzify(rule_outputs)
        interpretation = self._interpret(score)

        return {
            "score":        score,
            "rule_outputs": {k: round(v, 3) for k, v in rule_outputs.items()},
            "membership": {
                "harga":     {k: round(v, 3) for k, v in h.items()},
                "frekuensi": {k: round(v, 3) for k, v in f.items()},
                "urgensi":   {k: round(v, 3) for k, v in u.items()},
            },
            **interpretation,
        }
