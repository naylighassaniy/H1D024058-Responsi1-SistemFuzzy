// ============================================================
//  main.js — BuyWise · Frontend Logic
//  Mengirim input ke Flask API dan menampilkan hasil
// ============================================================

// ── Update tampilan nilai slider ──────────────────────────────
document.getElementById("s1").addEventListener("input", function () {
  document.getElementById("val1").textContent = this.value + "%";
});
document.getElementById("s2").addEventListener("input", function () {
  document.getElementById("val2").textContent = this.value + "×";
});
document.getElementById("s3").addEventListener("input", function () {
  document.getElementById("val3").textContent = this.value;
});

// ── Fungsi utama: kirim ke API & tampilkan hasil ──────────────
async function hitung() {
  const btn = document.getElementById("btnCheck");
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Menganalisis...';

  const payload = {
    rasio:     parseFloat(document.getElementById("s1").value),
    frekuensi: parseFloat(document.getElementById("s2").value),
    urgensi:   parseFloat(document.getElementById("s3").value),
  };

  try {
    const res  = await fetch("/api/check", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(payload),
    });

    if (!res.ok) throw new Error("Server error: " + res.status);

    const data = await res.json();
    renderResult(data);

  } catch (err) {
    alert("Terjadi kesalahan: " + err.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = "✦ Cek Sekarang ✦";
  }
}

// ── Render hasil ke DOM ───────────────────────────────────────
function renderResult(data) {
  // --- Verdict ---
  const rc = document.getElementById("resultCard");
  rc.classList.add("visible");

  document.getElementById("resultVerdict").textContent = data.emoji + " " + data.verdict;
  document.getElementById("resultVerdict").style.color = data.color;
  document.getElementById("scoreNum").textContent      = data.score;
  document.getElementById("resultDesc").innerHTML      = data.deskripsi;

  // --- Score bar (animasi) ---
  setTimeout(() => {
    document.getElementById("scoreBar").style.width = data.score + "%";
  }, 100);

  // --- Tips ---
  const tipsList = data.tips.map(t => `<li>${t}</li>`).join("");
  document.getElementById("resultTips").innerHTML =
    `<div class="result-tips-title">💌 Saran untukmu</div><ul>${tipsList}</ul>`;

  // --- Membership values ---
  const mf = data.membership;
  const varDefs = [
    { label: "Rasio Harga", sets: [["Rendah", mf.harga.rendah], ["Sedang", mf.harga.sedang], ["Tinggi", mf.harga.tinggi]] },
    { label: "Frekuensi",   sets: [["Jarang", mf.frekuensi.jarang], ["Kadang", mf.frekuensi.kadang], ["Sering", mf.frekuensi.sering]] },
    { label: "Urgensi",     sets: [["Rendah", mf.urgensi.rendah],  ["Sedang", mf.urgensi.sedang],  ["Tinggi", mf.urgensi.tinggi]] },
  ];

  document.getElementById("mfGrid").innerHTML = varDefs.map(v => `
    <div class="mf-var">
      <div class="mf-var-name">${v.label}</div>
      ${v.sets.map(([name, val]) => `
        <div class="mf-row">
          <span class="mf-set">${name}</span>
          <span class="mf-val">${val.toFixed(3)}</span>
        </div>
        <div class="mf-bar-wrap">
          <div class="mf-bar" style="width:${(val * 100).toFixed(1)}%"></div>
        </div>
      `).join("")}
    </div>
  `).join("");

  const mfSection = document.getElementById("mfSection");
  mfSection.classList.add("visible");

  // --- Scroll ke hasil ---
  rc.scrollIntoView({ behavior: "smooth", block: "nearest" });
}
