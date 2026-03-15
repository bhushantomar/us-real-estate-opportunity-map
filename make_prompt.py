from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'site' / 'data.json'
OUT = ROOT / 'prompt.md'


def pct(v: float) -> str:
    sign = '+' if v > 0 else ''
    return f"{sign}{v:.1f}%"


def money(v: int) -> str:
    return '${:,.0f}'.format(v)


def main() -> None:
    payload = json.loads(DATA.read_text(encoding='utf-8'))
    markets = payload['markets']
    ranked = sorted(markets, key=lambda m: m['scores']['balanced'], reverse=True)
    total_sales = sum(m['annual_sales'] for m in markets)
    avg_trend = sum(m['trend_1y'] * m['annual_sales'] for m in markets) / total_sales

    lines = []
    lines.append('# U.S. Real Estate Opportunity Map prompt pack')
    lines.append('')
    lines.append('Use this file as a compact context window for discussing the demo dataset in this repository.')
    lines.append('')
    lines.append('## Dataset summary')
    lines.append(f"- Markets: {len(markets)}")
    lines.append(f"- Sales-weighted 1Y home value trend: {pct(avg_trend)}")
    lines.append(f"- Median market price: {money(sorted(m['median_price'] for m in markets)[len(markets)//2])}")
    lines.append('')
    lines.append('## Top balanced picks')
    for idx, market in enumerate(ranked[:10], start=1):
        lines.append(f"{idx}. {market['city']}, {market['state']} — score {market['scores']['balanced']:.2f} | price {money(market['median_price'])} | 1Y trend {pct(market['trend_1y'])} | yield {pct(market['gross_yield'])} | drivers: {', '.join(market['drivers'])}")
    lines.append('')
    lines.append('## Full market table')
    lines.append('')
    lines.append('| Market | Region | Price | 1Y trend | 5Y trend | Yield | Job growth | Pop growth | Inventory | Balanced | Appreciation | Cash flow |')
    lines.append('|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for market in ranked:
        lines.append(
            f"| {market['city']}, {market['state']} | {market['region']} | {money(market['median_price'])} | {pct(market['trend_1y'])} | {pct(market['trend_5y'])} | {pct(market['gross_yield'])} | {pct(market['job_growth'])} | {pct(market['pop_growth'])} | {pct(market['inventory_delta'])} | {market['scores']['balanced']:.2f} | {market['scores']['appreciation']:.2f} | {market['scores']['cashflow']:.2f} |"
        )

    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('[OK] wrote prompt.md')


if __name__ == '__main__':
    main()
