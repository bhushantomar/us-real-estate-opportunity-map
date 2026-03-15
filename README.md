# U.S. Real Estate Opportunity Map

Analyzing which U.S. cities look most interesting for buying residential real estate, using assumed demo data spanning home value trend, gross rent yield, job growth, population growth, and inventory conditions.

**Live demo:** `https://bhushantomar.github.io/us-real-estate-opportunity-map/` *(works if you create the repo with this exact name and enable GitHub Pages from `/docs`)*

![Treemap demo](assets/real-estate-heatmap-treemap.png)

## What's here

This repo mirrors the same overall pattern as the reference project: a lightweight data pipeline, a compact static dataset, and a single interactive site.

It ships with:

- a mock dataset for 40 U.S. housing markets
- three ranking modes: balanced, appreciation, and cash flow
- a static interactive site with a treemap and scatter view
- a prompt generator for LLM-assisted analysis
- a `/docs` folder so GitHub Pages can host the demo

## Data pipeline

1. **Source data** (`data/markets.json`) — assumed market metrics for 40 cities.
2. **Build site data** (`build_site_data.py`) — computes tiers, scores, and writes `site/data.json` plus `docs/data.json`.
3. **Prompt file** (`make_prompt.py`) — packages the current dataset and top-ranked markets into `prompt.md`.
4. **Website** (`site/index.html`) — interactive treemap/scatter visualization where area = annual home sales and color = 1Y home value trend.
5. **Pages publish target** (`docs/`) — duplicate of the static site so GitHub Pages can serve it directly.

## Key files

| File | Description |
|------|-------------|
| `data/markets.json` | Source dataset with assumed market metrics |
| `site/data.json` | Computed frontend data used by the local site |
| `docs/data.json` | Same dataset for GitHub Pages |
| `site/index.html` | Local static site |
| `docs/index.html` | GitHub Pages version of the site |
| `build_site_data.py` | Rebuilds `site/data.json` and `docs/data.json` from source data |
| `make_prompt.py` | Recreates `prompt.md` |
| `prompt.md` | Single-file summary for LLM analysis |
| `assets/` | README screenshots |
| `PUBLISH_TO_GITHUB.md` | Exact upload and publish steps |

## Opportunity scoring

Each market gets a 0–10 score in three different modes:

- **Balanced** — blends appreciation, yield, job growth, population growth, affordability, and supply tightness.
- **Appreciation** — leans into recent trend, 5Y strength, and constrained inventory.
- **Cash flow** — favors gross yield, lower entry price, and more negotiable supply.

The color scale is intentionally independent from the ranking mode:

- **Green** = positive 1Y home value trend
- **Red** = negative 1Y home value trend

## Visualization

The main visualization is an interactive view with two modes:

- **Treemap** — rectangle area is proportional to annual home sales.
- **Growth vs Yield** — bubble size is market size, x-axis is gross yield, y-axis is 1Y home value trend.

Hover any market to inspect the thesis. Click a market to pin it in the details panel.

## Setup

This project uses only the Python standard library.

```bash
python build_site_data.py
python make_prompt.py
```

Serve locally:

```bash
cd site
python -m http.server 8000
```

Then open `http://localhost:8000`.

## GitHub Pages

The repo is already prepared for GitHub Pages via `/docs`.

1. Create a new public repo named `us-real-estate-opportunity-map`.
2. Upload this bundle or push it with git.
3. In GitHub repo settings, enable **Pages** from the `main` branch and `/docs` folder.
4. Your demo URL should become `https://bhushantomar.github.io/us-real-estate-opportunity-map/`.

## Screenshots

### Treemap

![Treemap](assets/real-estate-heatmap-treemap.png)

### Growth vs Yield

![Scatter](assets/real-estate-heatmap-scatter.png)

## Notes

- All numbers in this starter are **assumed demo values**, not live market data.
- Replace `data/markets.json` with real exports from Zillow, Redfin, Census, BLS, or your own pipeline when you are ready.
- This is a design and repo starter, not investment advice.
