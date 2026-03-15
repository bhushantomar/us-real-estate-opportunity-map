from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'data' / 'markets.json'
SITE = ROOT / 'site'
DOCS = ROOT / 'docs'

weights = {
    'balanced': {'trend_1y': 0.24, 'gross_yield': 0.18, 'job_growth': 0.16, 'pop_growth': 0.12, 'median_price_inv': 0.14, 'inventory_tight': 0.10, 'trend_5y': 0.06},
    'appreciation': {'trend_1y': 0.36, 'trend_5y': 0.22, 'job_growth': 0.16, 'pop_growth': 0.10, 'inventory_tight': 0.10, 'median_price_inv': 0.06},
    'cashflow': {'gross_yield': 0.34, 'median_price_inv': 0.24, 'inventory_loose': 0.14, 'job_growth': 0.12, 'trend_1y': 0.10, 'pop_growth': 0.06},
}


def normalize(value: float, values: list[float], invert: bool = False) -> float:
    lo, hi = min(values), max(values)
    if hi == lo:
        return 0.5
    scaled = (value - lo) / (hi - lo)
    return 1 - scaled if invert else scaled


def price_tier(price: int) -> str:
    if price < 325000:
        return 'Affordable'
    if price < 475000:
        return 'Mid-market'
    return 'Premium'


def drivers_for(m: dict) -> list[str]:
    drivers = []
    if m['trend_1y'] >= 7:
        drivers.append('fast price momentum')
    if m['gross_yield'] >= 6.2:
        drivers.append('strong gross yield')
    if m['job_growth'] >= 2.7:
        drivers.append('strong job growth')
    if m['pop_growth'] >= 1.3:
        drivers.append('population inflow')
    if m['median_price'] <= 300000:
        drivers.append('lower entry price')
    if m['inventory_delta'] >= 7:
        drivers.append('more negotiating room')
    if m['inventory_delta'] <= -2:
        drivers.append('tight supply support')
    if not drivers:
        drivers.append('steady fundamentals')
    return drivers[:4]


def summary_for(m: dict) -> str:
    if m['trend_1y'] >= 7 and m['gross_yield'] >= 5.5:
        return 'Momentum plus usable income. Strong all-around candidate for a watch list.'
    if m['trend_1y'] < 0 and m['inventory_delta'] >= 10:
        return 'Cooling values with much looser supply. Better for patient buyers than momentum chasers.'
    if m['gross_yield'] >= 6.4 and m['median_price'] <= 300000:
        return 'Lower-cost market with stronger gross yield. More operator-friendly than prestige-oriented.'
    if m['trend_5y'] >= 50:
        return 'Long-run strength is already visible, so entry timing matters more than the headline trend.'
    return 'Balanced fundamentals without one single metric dominating the story.'


def rebuild() -> None:
    markets = json.loads(SOURCE.read_text(encoding='utf-8'))
    trend_values = [m['trend_1y'] for m in markets]
    trend5_values = [m['trend_5y'] for m in markets]
    yield_values = [m['gross_yield'] for m in markets]
    job_values = [m['job_growth'] for m in markets]
    pop_values = [m['pop_growth'] for m in markets]
    price_values = [m['median_price'] for m in markets]
    inv_values = [m['inventory_delta'] for m in markets]

    for m in markets:
        norms = {
            'trend_1y': normalize(m['trend_1y'], trend_values),
            'trend_5y': normalize(m['trend_5y'], trend5_values),
            'gross_yield': normalize(m['gross_yield'], yield_values),
            'job_growth': normalize(m['job_growth'], job_values),
            'pop_growth': normalize(m['pop_growth'], pop_values),
            'median_price_inv': normalize(m['median_price'], price_values, invert=True),
            'inventory_tight': normalize(m['inventory_delta'], inv_values, invert=True),
            'inventory_loose': normalize(m['inventory_delta'], inv_values, invert=False),
        }
        m['price_tier'] = price_tier(m['median_price'])
        m['drivers'] = drivers_for(m)
        m['summary'] = summary_for(m)
        m['rationale'] = f"Signals that stand out here: {', '.join(m['drivers'][:3])}. This is demo data meant for product exploration, not live investment advice."
        m['scores'] = {mode: round(sum(norms[key] * weight for key, weight in mode_weights.items()) * 10, 2) for mode, mode_weights in weights.items()}

    payload = {
        'title': 'U.S. Real Estate Opportunity Map',
        'subtitle': 'Assumed demo data for the best U.S. cities to buy residential real estate.',
        'modes': {
            'balanced': {'label': 'Balanced', 'summary': 'Balances price momentum, yield, job growth, population growth, affordability, and supply tightness.'},
            'appreciation': {'label': 'Appreciation', 'summary': 'Leans harder into recent trend, 5Y strength, and tighter supply.'},
            'cashflow': {'label': 'Cash flow', 'summary': 'Favors yield, cheaper entry price, and more negotiable supply.'},
        },
        'markets': markets,
    }

    for path in [SITE / 'data.json', DOCS / 'data.json']:
        path.write_text(json.dumps(payload, indent=2), encoding='utf-8')

    if (SITE / 'index.html').exists():
        shutil.copy2(SITE / 'index.html', DOCS / 'index.html')


if __name__ == '__main__':
    rebuild()
    print('[OK] rebuilt site/data.json and docs/data.json')
