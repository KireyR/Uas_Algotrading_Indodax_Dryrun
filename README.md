# UAS Algoritma Trading — Bot Dry Run Indodax di Vercel
Ursulla Ningtyas Kirey Ruu · NIM 25110200023

## Status jujur
- Freeze strategi: 04 Nov 2026 12.00 WIB (buktikan lewat commit: ISI hash + waktu).
- Pengerjaan bot dimulai 09 Nov 2026, dilanjutkan 11 Nov malam dan 12 Nov.
- Forward test live: dimulai ISI (tanggal/jam tick pertama), BUKAN 4 Nov. Jendela resmi 4–14 Nov 12.00 WIB tidak tercakup penuh.
- Tidak ada angka forward yang diisi manual; semua dari log di folder `logs/`.

## Strategi (samakan dengan kode!)
RSI Cross Level + SMA(200), 1D, long-only, spot IDR. Parameter beku: RSI 21, entry 60, exit 40, SMA 200.
Universe: BTC/IDR, ETH/IDR, DOGE/IDR. Maks. 3 posisi, batas rugi harian 3% (hari WIB), kill switch.
Eksekusi: fill di bid/ask live dengan rata-rata kedalaman order book; hanya candle tertutup; min order Rp25.000.
Fee taker: ISI nilai, URL sumber resmi, tanggal akses (pakai yang lebih mahal vs /api/pairs).

## Perubahan UTS → UAS
ISI sesuai kenyataan (aset, eksekusi, biaya, risiko, infrastruktur). Parameter tidak diubah setelah freeze.

## Struktur pengumpulan
- `dashboard.html` — dashboard offline (self-contained)
- `hitung_ulang.py` — hitung ulang semua angka dashboard: `python3 hitung_ulang.py dashboard.html`
- `.env.example` — tanpa secret
- `.git/` — riwayat commit utuh (tanpa force-push)
- `logs/` — log mentah forward: panggilan, order, equity harian, error, snapshot order book (ISI dari export bot)
- source bot + backtest (ISI)

## Link
Dashboard Vercel: ISI · Repo: ISI

## Refleksi
ISI setelah forward selesai: penyebab selisih backtest vs forward dengan angka (spread bps, slippage, candle terlewat).
