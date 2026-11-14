#!/usr/bin/env python3
"""
run_all.py - satu perintah: unduh data -> backtest + validasi -> bangun dashboard HTML mandiri.

  python run_all.py                       # unduh data Yahoo (jika belum ada cache), jalankan, bangun UTS_NIM_Nama.html
  python run_all.py --refresh             # paksa unduh ulang data
  python run_all.py --data-dir data       # pakai folder data lain (format CSV sama) - untuk uji ulang dosen
  python run_all.py --freeze 2026-09-15   # tetapkan tanggal pembekuan sebenarnya
  python run_all.py --params-file output/frozen_params.json   # pakai parameter beku (tanpa optimasi ulang)
  python run_all.py --synthetic           # UJI PROGRAM dengan data simulasi (hasil: DEMO_*.html, BUKAN untuk dikumpulkan)
"""
import argparse, json, os, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "src"))
import pandas as pd
import config as cfg, data, pipeline, build_dashboard

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=os.path.join(HERE, "data")); ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--universe", default=os.path.join(HERE, "universe.csv")); ap.add_argument("--freeze", default=None)
    ap.add_argument("--params-file", default=None); ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--out-dir", default=os.path.join(HERE, "output"))
    ap.add_argument("--ohlc", default=os.path.join(HERE, "data", "kompas100_ohlc.csv"), help="CSV panjang hasil tools/ods_to_csv.py (jalur utama)")
    ap.add_argument("--yahoo", action="store_true", help="pakai jalur unduh Yahoo Finance (data/raw) alih-alih file OHLC")
    a = ap.parse_args(); os.makedirs(a.out_dir, exist_ok=True)
    if a.synthetic:
        print("MODE SINTETIS: data simulasi, hanya untuk menguji program."); panel = data.synthetic_panel()
    elif not a.yahoo and os.path.exists(a.ohlc):
        print(f"Memuat data OHLC dari {a.ohlc}")
        ihsg = os.path.join(HERE, cfg.IHSG_CSV)
        panel = data.load_ohlc_csv(a.ohlc, set(data.load_universe(a.universe)), ihsg_csv=ihsg)
        for n in panel.meta["data_notes"]: print("  -", n)
        print(f"Data termuat: {len(panel.tickers)} saham, {panel.dates[0].date()} .. {panel.dates[-1].date()}")
    else:
        raw = os.path.join(a.data_dir, "raw"); have = os.path.isdir(raw) and any(f.endswith(".JK.csv") for f in os.listdir(raw))
        if a.refresh or not have:
            uni = data.load_universe(a.universe); end = dt.date.today() + dt.timedelta(days=1)
            fd = pd.Timestamp(a.freeze or cfg.FREEZE_DATE) if (a.freeze or cfg.FREEZE_DATE) else pd.Timestamp(dt.date.today()) - pd.Timedelta(days=cfg.FORWARD_MIN_DAYS)
            start = (fd - pd.DateOffset(years=cfg.BACKTEST_YEARS) - pd.Timedelta(days=cfg.WARMUP_DAYS)).date()
            print(f"Mengunduh {len(uni)} saham dari Yahoo Finance ({start} .. {end}) ..."); os.makedirs(raw, exist_ok=True)
            meta = data.download(uni, start, end, a.data_dir)
            print(f"Berhasil {len(meta['tickers_ok'])} saham; gagal/tidak ada: {meta['tickers_missing']}")
        panel = data.load_panel(a.data_dir, set(data.load_universe(a.universe)))
        print(f"Data termuat: {len(panel.tickers)} saham, {panel.dates[0].date()} .. {panel.dates[-1].date()} (unduhan {panel.meta.get('download_date')})")
    R = pipeline.run_all(panel, params_file=a.params_file, freeze_date=a.freeze)
    for w in R["warnings"]: print("PERINGATAN:", w)
    fz = {"freeze_date": R["periods"]["freeze"], "params": R["params"], "created": dt.datetime.now().isoformat(timespec="seconds"),
          "note": "Parameter dipilih hanya dari data in-sample sebelum tanggal pembekuan."}
    json.dump(fz, open(os.path.join(a.out_dir, "frozen_params.json"), "w"), indent=1)
    synth = bool(panel.meta.get("synthetic"))
    name = "DEMO_DATA_SIMULASI_JANGAN_DIKUMPULKAN.html" if synth else f"UTS_{cfg.NIM}_{cfg.NAMA_FILE}.html"
    path, size = build_dashboard.build_html(R, panel, os.path.join(HERE, "src", "template.html"), os.path.join(a.out_dir, name))
    m = R["m_full"]
    print(f"\nParameter: {R['params']}\nCAGR {m['cagr']*100:.2f}% | MDD {m['mdd']*100:.2f}% | Sharpe {m['sharpe']:.2f} | trade {m['n_trades']}")
    print(f"HTML: {path} ({size/1024:.0f} KB; batas 15 MB)")
    if synth: print("INGAT: file DEMO memakai data simulasi dan TIDAK boleh dikumpulkan.")

if __name__ == "__main__": main()
