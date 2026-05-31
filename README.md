# 🍔 nyc-grades

A web-based dashboard for exploring **New York City restaurant inspection results
and violation citations**, built with [Streamlit](https://streamlit.io/).

It pulls the latest data live from [NYC Open Data](https://opendata.cityofnewyork.us/)
via the Socrata Open Data API, so the dashboard always reflects recent inspections
without storing any data locally.

> This project is a clone / reimplementation of
> [`eigenfoo/nyc-restaurant-violations`](https://github.com/eigenfoo/nyc-restaurant-violations)
> by George Ho. See [Attribution & License](#attribution--license) below.

## Features

- 🔎 **Search** restaurants by name (DBA — "Doing Business As").
- 🗺️ **Filter** by borough and cuisine type.
- 📊 **Statistics**: top violation descriptions and inspection-grade distribution.
- ⬇️ **Download** the filtered results as a CSV file.
- ⚡ **Cached** data (24 hours) for fast reloads.

## Data source

Data comes from the **DOHMH New York City Restaurant Inspection Results** dataset
on NYC Open Data:

- Dataset page: <https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j>
- API endpoint (Socrata): `https://data.cityofnewyork.us/resource/43nn-pn8j.json`

The app loads the **50,000 most recent** records ordered by inspection date. This is
a recent sample, not the full historical dataset. Data is compiled from NYC
administrative systems and may contain errors or omissions.

## Getting started

### Prerequisites

- Python 3.9 or newer

### Installation

```bash
git clone https://github.com/jratlee/nyc-grades.git
cd nyc-grades
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

Streamlit will start a local server (by default at <http://localhost:8501>) and open
the dashboard in your browser.

## Project structure

```
nyc-grades/
├── app.py             # Streamlit dashboard application
├── requirements.txt   # Python dependencies
├── LICENSE            # MIT license (with attribution)
└── README.md
```

## How it works

`app.py`:

1. Requests the latest inspection records from the Socrata API (with a request
   timeout and HTTP error handling).
2. Loads them into a pandas `DataFrame` and normalizes the `inspection_date` column.
3. Renders interactive search/filter controls in the sidebar.
4. Displays the filtered records in a table, offers a CSV download, and charts
   summary statistics.

Data is cached for 24 hours via `@st.cache_data` so repeated interactions don't
re-fetch from the API.

## Contributing

Issues and pull requests are welcome. If you add a dependency, please update
`requirements.txt`.

## Attribution & License

This project is licensed under the [MIT License](LICENSE).

It is a derivative of
[`eigenfoo/nyc-restaurant-violations`](https://github.com/eigenfoo/nyc-restaurant-violations),
which is also MIT licensed and **Copyright (c) 2021 George Ho**. In accordance
with the MIT License, the original copyright notice is preserved in the [`LICENSE`](LICENSE)
file alongside the copyright for this derivative work.

Restaurant inspection data is provided by the City of New York via
[NYC Open Data](https://opendata.cityofnewyork.us/) and is subject to its
[terms of use](https://www.nyc.gov/home/terms-of-use.page). This project is not
affiliated with or endorsed by the City of New York.
