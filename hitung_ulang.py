#!/usr/bin/env python3
"""hitung_ulang: hitung ulang metrik dashboard dari data mentah (equity, trades, live).
Pakai: python3 hitung_ulang.py [dashboard.html]
Membaca DRY_RUN_DATA dari dashboard, menghitung ulang semua metrik, dan membandingkannya
dengan nilai yang tampil. Exit code 1 bila ada selisih > toleransi."""
import re, json, sys, math
path = sys.argv[1] if len(sys.argv) > 1 else "dashboard.html"
src = open(path, encoding="utf-8").read()
outer = json.loads(re.search(r'<script id="DASHBOARD_DATA" type="application/json">(.*?)</script>', src, re.S).group(1))
d = json.loads(re.search(r'<script id="DRY_RUN_DATA" type="application/json">(.*?)</script>', outer["uas"], re.S).group(1))
bt, live = d["backtest"], d["live"]; M = bt["metrics"]
eq = [p["equity"] for p in bt["equity"]]; tr = bt["trades"]
res = {}
res["initial_cash"] = eq[0]; res["final_equity"] = eq[-1]
res["total_return"] = eq[-1] / eq[0] - 1
days = (bt["equity"][-1]["time"] - bt["equity"][0]["time"]) / 86400
res["cagr"] = (eq[-1] / eq[0]) ** (365.25 / days) - 1
pk, mdd = 0, 0
for v in eq: pk = max(pk, v); mdd = min(mdd, v / pk - 1)
res["max_drawdown"] = mdd
wins = [t["pnl_idr"] for t in tr if t["pnl_idr"] > 0]; loss = [t["pnl_idr"] for t in tr if t["pnl_idr"] <= 0]
res["trade_count"] = len(tr); res["win_rate"] = len(wins) / len(tr) if tr else None
res["profit_factor"] = sum(wins) / abs(sum(loss)) if loss else None
res["average_win_idr"] = sum(wins) / len(wins) if wins else None
res["average_loss_idr"] = sum(loss) / len(loss) if loss else None
fee = sum(t["fee_idr"] for t in tr); spr = sum(t["spread_cost_idr"] for t in tr)
net = sum(t["pnl_idr"] for t in tr)
res["cost_share_of_gross_profit"] = (fee + spr) / (net + fee + spr)
res["btc_buy_hold_return"] = M["benchmark_buy_hold_idr"]["btcidr"] / M["initial_cash"] - 1
print(f"{'metrik':32}{'dihitung ulang':>20}{'di dashboard':>20}  status"); bad = 0
for k, v in res.items():
    ref = M.get(k)
    if ref is None: print(f"{k:32}{v:>20.6f}{'(turunan)':>20}"); continue
    ok = abs(v - ref) <= 1e-6 * max(1, abs(ref)); bad += not ok
    print(f"{k:32}{v:>20.6f}{ref:>20.6f}  {'OK' if ok else 'BEDA'}")
# catatan: total_fees_idr di dashboard mencakup posisi terbuka; jumlah per-trade tertutup:
print(f"fee trade tertutup={fee:.2f}; total_fees_idr dashboard={M['total_fees_idr']:.2f} (selisih = fee posisi terbuka)")
# benchmark equal-weight: konsistensi
bh = M["benchmark_buy_hold_idr"]; ew = sum(bh.values()) / len(bh) / M["initial_cash"] - 1
print(f"equal-weight dari B&H per aset = {ew:.4f}; di dashboard = {M['benchmark_equal_weight_return']:.4f}",
      "OK" if abs(ew - M['benchmark_equal_weight_return']) < 1e-3 else "<< TIDAK KONSISTEN, periksa")
# forward
f = live.get("forward", {}); rows = f.get("equity", [])
print("forward: observasi =", len(rows), "| trade =", len(live.get("trades", [])), "| panggilan", live.get("calls"))
if len(rows) > 1:
    s = f.get("start_equity") or rows[0]["equity"]; pk = s; m = 0
    for r in rows: pk = max(pk, r["equity"]); m = min(m, r["equity"] / pk - 1)
    print(f"forward return={rows[-1]['equity']/s-1:.6f}  forward MDD={m:.6f}")
else:
    print("forward: belum ada data (jangan diisi manual)")
sys.exit(1 if bad else 0)
