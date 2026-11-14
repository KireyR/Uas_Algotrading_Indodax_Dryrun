UAS Algoritma Trading — Bot Dry Run Indodax di Vercel

Ursulla Ningtyas Kirey Ruu · NIM 25110200023 · Algorithmic Trading

1. Status pengerjaan (jujur)
Forward test live TIDAK berjalan. Bot belum ter-deploy di Vercel selama jendela resmi 4 Nov 12.00 – 14 Nov 12.00 WIB 2026. Tidak ada log forward, order simulasi, equity harian, atau snapshot order book dari periode itu. Semua kolom forward di dashboard berstatus "menunggu data" dan sengaja tidak diisi.
Komponen kecocokan backtest–forward tidak dapat dinilai. Tidak ada angka forward yang dikarang, disimulasikan, atau diketik manual.
Freeze tidak dapat dibuktikan dari riwayat commit. Parameter (RSI 21 / entry 60 / exit 40 / SMA 200) berasal dari strategi UTS dan tidak diubah, tetapi commit pertama repo ini dibuat pada 14 Nov 2026, bukan 4 Nov 2026 12.00 WIB. Jadi klaim "beku pada 4 Nov" hanya pernyataan saya, bukan bukti commit.
Garis waktu: pengerjaan dimulai 9 Nov 2026, dilanjutkan 11 Nov malam dan 12 Nov 2026.
Link dashboard Vercel: tidak ada (belum ter-deploy). Dashboard offline: dashboard.html.
2. Strategi

RSI Cross Level + SMA(200), timeframe 1D, long-only, spot IDR, dry run. Parameter: RSI 21, entry 60, exit 40, SMA 200. Universe: BTC/IDR, ETH/IDR, DOGE/IDR. Risiko: maksimal 3 posisi, batas rugi harian 3% (hari WIB), kill switch. Eksekusi yang dirancang: fill di bid/ask dengan rata-rata kedalaman order book, hanya candle tertutup, order minimum Rp25.000.

3. Hasil backtest (data asli Indodax, 3 November 2023 – 3 November 2026, 1096 hari)
Metrik	Nilai
Modal awal / akhir	Rp100.000.000 / Rp117.551.829
Total return	17,55%
CAGR	5,54%
Max drawdown	−17,27%
Jumlah trade tertutup	15
Win rate	53,3%
Profit factor	2,09
Rata-rata menang / kalah	Rp3.785.276 / −Rp2.069.812
Biaya (fee + spread) ÷ laba kotor	4,87% (slippage tidak dimodelkan)
Buy & hold BTC/IDR, periode sama	−16,04%

Semua angka dihitung ulang dengan python3 hitung_ulang.py dashboard.html dan cocok dengan dashboard.

4. Perubahan UTS → UAS
Parameter dan aturan sinyal tidak diubah.
Aset: dari saham ke kripto Indodax IDR spot.
Eksekusi dan biaya: fill di bid/ask dengan kedalaman order book, fee taker, estimasi spread dari snapshot order book (3 snapshot), minimum order Rp25.000.
Risiko: batas rugi harian dan kill switch.
5. Isi repo
- `dashboard.html`: dashboard UAS offline mandiri (versi final UAS)
- `hitung_ulang.py`: menghitung ulang metrik dashboard dari data yang tertanam di dashboard
- `.env.example`: contoh variabel lingkungan, tanpa secret
- `vercel.json`: konfigurasi cron yang menunjuk ke /api/tick. Endpoint /api/tick TIDAK ada di repo ini, jadi bot Vercel tidak berjalan.
- `run_all.py`, `universe.csv`, `requirements.txt`: pipeline UTS (saham Kompas100, data Yahoo). BUKAN pipeline UAS Indodax.
- `UTS_*.html`, `UTS ... .html`: dashboard UTS (arsip).
- `UAS_Ursulla_NIngtyas...html`: versi awal dashboard UAS sebelum dilengkapi.

Belum ada di repo: kode yang mengunduh data Indodax dan menjalankan backtest UAS, source /api/tick, dan folder logs/. Angka backtest UAS di dashboard tertanam dari proses riset sebelumnya yang kodenya tidak disertakan di repo ini, sehingga tidak dapat direproduksi dari data mentah oleh pihak lain. hitung_ulang.py hanya memverifikasi konsistensi hitungan dari data tertanam itu.

Belum ada di repo: source code bot (/api/tick), folder logs/, dan source backtest. Seluruhnya belum disertakan.

6. Keterbatasan yang diketahui
Hanya 15 trade selama 3 tahun, sehingga profit factor dan win rate sangat sensitif terhadap satu-dua trade.
Spread diestimasi dari 3 snapshot saja (target soal: minimal 3 per hari). Slippage tidak dimodelkan.
Fee taker resmi Indodax dan tanggal aksesnya belum saya verifikasi dari sumber resmi.
Benchmark equal-weight tersimpan di dashboard (+73,5%) tidak konsisten dengan buy & hold per aset (BTC −16%, ETH −52%, DOGE −58%). Angka itu tidak boleh dianggap benar sebelum diperiksa ulang.
7. Refleksi

Pelajaran utama adalah bahwa saya baru mulai mengerjakan bot pada 9 Nov, lima hari setelah freeze, dan baru ke tahap hasil backtest saat jendela forward sudah berjalan. Akibatnya bot tidak sempat ter-deploy, sehingga selisih backtest vs forward tidak dapat diukur dan tidak akan saya perkirakan. Yang terukur hanya sisi backtest: biaya 4,87% dari laba kotor, hasil bergantung pada 15 trade, dan strategi (+17,55%) mengalahkan buy & hold BTC (−16,04%) pada periode yang sama, bukan hasil yang bisa dijamin berulang di forward. Kalau mengulang, saya akan men-deploy bot dan mulai mengumpulkan log sebelum tanggal freeze, bukan setelahnya.
