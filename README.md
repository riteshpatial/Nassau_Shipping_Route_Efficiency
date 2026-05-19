# Nassau Shipping Route Efficiency

An interactive logistics intelligence dashboard that analyzes **factory-to-customer shipping routes** for Nassau Candy Distributor. Built with Python and Streamlit, it identifies efficient routes, delay-prone lanes, and regional logistics bottlenecks — all in real time.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Factory & Product Mapping](#factory--product-mapping)
- [Key Metrics & Logic](#key-metrics--logic)
- [Dashboard Features](#dashboard-features)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [Deliverables](#deliverables)

---

## Project Overview

Nassau Candy Distributor ships Wonka-brand candy products from **5 factories** across the United States to customers nationwide. This project answers:

- Which factory-to-state routes are fastest?
- Which routes are consistently delayed?
- Which ship modes perform best?
- Where are the regional bottlenecks?

The system builds a full **logistics KPI dashboard** with filters, charts, and a route efficiency leaderboard.

---

## Project Structure

```
Nassau_Shipping_Route_Efficiency/
│
├── app.py                                        # Streamlit dashboard
├── factories.py                                  # Factory & product mapping data
├── analysis.ipynb                                # EDA & analysis notebook
├── requirements.txt                              # Python dependencies
│
├── data/
│   └── Nassau Candy Distributor.csv              # Raw shipping dataset
│
├── DPR/
│   └── Nassau_Shipping_Route_Efficiency_DPR.pdf  # Detailed Project Report
│
└── demo video/
    └── demo.mp4                                  # App walkthrough video
```

---

## Dataset

**File:** `data/Nassau Candy Distributor.csv`

| Column | Description |
|--------|-------------|
| `Order ID` | Unique order identifier |
| `Order Date` | Date order was placed |
| `Ship Date` | Date order was shipped |
| `Ship Mode` | Shipping method (Standard Class, etc.) |
| `Customer ID` | Customer identifier |
| `Country/Region` | Country of delivery |
| `City` | Delivery city |
| `State/Province` | Delivery state |
| `Postal Code` | ZIP code |
| `Division` | Product division (Chocolate, Candy, etc.) |
| `Region` | US region (Interior, etc.) |
| `Product ID` | SKU identifier |
| `Product Name` | Candy product name |
| `Sales` | Sale value (USD) |
| `Units` | Number of units ordered |
| `Gross Profit` | Profit after cost |
| `Cost` | Product cost |

**Engineered columns (added at runtime):**

| Column | Logic | Purpose |
|--------|-------|---------|
| `Shipping Lead Time` | `(Ship Date - Order Date).days % 15` → min 3 | Days taken to ship |
| `Delayed` | `1 if Lead Time > delay threshold (default: 7 days)` | Binary delay flag |
| `Factory` | Mapped from Product Name | Which factory produced the item |
| `Route` | `Factory → State/Province` | Full factory-to-destination lane |

---

## Factory & Product Mapping

Each product is mapped to one of **5 factories** across the US:

| Factory | Location | Products |
|---------|----------|---------|
| **Lot's O' Nuts** | Arizona (32.88°N, 111.77°W) | Wonka Bar Nutty Crunch, Fudge Mallows, Scrumdiddlyumptious |
| **Wicked Choccy's** | Georgia (32.08°N, 81.09°W) | Wonka Bar Milk Chocolate, Triple Dazzle Caramel |
| **Sugar Shack** | Minnesota (48.12°N, 96.18°W) | Laffy Taffy, SweeTARTS, Nerds, Fun Dip, Fizzy Lifting Drinks |
| **Secret Factory** | Illinois (41.45°N, 90.57°W) | Everlasting Gobstopper, Lickable Wallpaper, Wonka Gum |
| **The Other Factory** | Tennessee (35.12°N, 89.97°W) | Hair Toffee, Kazookles |

---

## Key Metrics & Logic

**Shipping Lead Time:**
```
Lead Time = (Ship Date - Order Date).days % 15
Minimum capped at 3 days
```

**Delay Flag:**
```
Delayed = 1  →  if Lead Time > threshold (adjustable, default: 7 days)
Delayed = 0  →  on-time
```

**Route:**
```
Route = Factory Name → Destination State
Example: "Sugar Shack → Texas"
```

**KPIs tracked:**
- Total Shipments
- Average Lead Time (days)
- Delayed % across all shipments
- Unique Routes count

---

## Dashboard Features

The Streamlit app has **4 sidebar filters** and **5 analysis sections**:

### Sidebar Filters

| Filter | Options |
|--------|---------|
| Order Date Range | Date picker — filter by order period |
| Region | Multi-select — filter by US region |
| Ship Mode | Multi-select — Standard Class, etc. |
| Delay Threshold | Slider (1–20 days) — what counts as "delayed" |

### Dashboard Sections

| Section | Chart Type | What It Shows |
|---------|-----------|---------------|
| **KPI Cards** | Metric tiles | Total shipments, avg lead time, delay %, unique routes |
| **Route Efficiency Leaderboard** | Sortable table | Every route ranked by avg lead time + delay rate |
| **Average Lead Time by Route** | Bar chart (Top 15) | Fastest vs slowest factory-to-state lanes |
| **Ship Mode Comparison** | Box plot | Lead time distribution per shipping method |
| **Regional Bottleneck View** | Scatter plot | Region vs lead time, bubble size = Sales value |

---

## Tech Stack

| Library | Purpose |
|---------|---------|
| `streamlit` | Interactive web dashboard |
| `pandas` | Data loading, cleaning, aggregation |
| `numpy` | Lead time calculation, delay flagging |
| `plotly` | Interactive bar, box, and scatter charts |
| `scikit-learn` | Available for ML extensions |

---

## Setup & Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/riteshpatial/Nassau_Shipping_Route_Efficiency.git
cd Nassau_Shipping_Route_Efficiency
```

### Step 2 — Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run

```bash
streamlit run app.py
```

Dashboard opens at: **http://localhost:8501**

Use the sample dataset already included at `data/Nassau Candy Distributor.csv` — no setup needed.

---

## Deliverables

| Deliverable | Location |
|------------|----------|
| Interactive Streamlit Dashboard | `app.py` |
| EDA & Analysis Notebook | `analysis.ipynb` |
| Detailed Project Report (DPR) | `DPR/Nassau_Shipping_Route_Efficiency_DPR.pdf` |
| Demo Video | `demo video/demo.mp4` |
| Raw Dataset | `data/Nassau Candy Distributor.csv` |

---

## Author

**Ritesh Patial** — Data Analyst

GitHub: [github.com/riteshpatial](https://github.com/riteshpatial)
