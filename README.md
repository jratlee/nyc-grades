# 🍔 nyc-grades

**In plain English:** Want to check if your favorite pizza spot passed its last health inspection? This free dashboard lets any New Yorker look up restaurant grades, violations, and inspection dates across all five boroughs.

---

A simple web dashboard for looking up New York City restaurant inspection results
and the violations they were cited for. It's built with
[Streamlit](https://streamlit.io/).

The app pulls data straight from [NYC Open Data](https://opendata.cityofnewyork.us/)
using the Socrata Open Data API, so it always shows recent inspections and doesn't
keep any data of its own.

This is a clone of
[`eigenfoo/nyc-restaurant-violations`](https://github.com/eigenfoo/nyc-restaurant-violations)
by George Ho. See [Attribution and license](#attribution-and-license) below for details.

## Features

- Search for restaurants by name (the DBA, or "Doing Business As" name).
- Filter by borough and cuisine type.
- See quick stats: the top violation descriptions and how grades are distributed.
- Download the results you're looking at as a CSV file.
- Cached data (24 hours) so reloads stay fast.

## Where the data comes from

The data is the DOHMH New York City Restaurant Inspection Results dataset on
NYC Open Data:

- Dataset page: <https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j>
- API endpoint (Socrata): `https://data.cityofnewyork.us/resource/43nn-pn8j.json`

The app loads the 50,000 most recent records, ordered by inspection date. That's a
recent sample rather than the full history, and since it's compiled from NYC
administrative systems it can have errors or missing values.

## Getting started

You'll need Python 3.9 or newer.

```bash
git clone https://github.com/jratlee/nyc-grades.git
cd nyc-grades
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Then run the app:

```bash
streamlit run app.py
```

Streamlit starts a local server (usually at <http://localhost:8501>) and opens the
dashboard in your browser.

## Project structure

```
nyc-grades/
├── app.py             # Streamlit dashboard application
├── requirements.txt   # Python dependencies
├── LICENSE            # MIT license (with attribution)
└── README.md
```

## How it works

When you load the page, `app.py`:

1. Requests the latest inspection records from the Socrata API, with a request
   timeout and HTTP error handling so a bad response doesn't crash the app.
2. Loads them into a pandas `DataFrame` and cleans up the `inspection_date` column.
3. Builds the search and filter controls in the sidebar.
4. Shows the matching records in a table, lets you download them, and charts a
   couple of summary stats.

The data is cached for 24 hours with `@st.cache_data`, so clicking around doesn't
re-fetch from the API every time.

## Contributing

Issues and pull requests are welcome. If you add a dependency, please update
`requirements.txt`.

## Attribution and license

This project is licensed under the [MIT License](LICENSE).

It's based on
[`eigenfoo/nyc-restaurant-violations`](https://github.com/eigenfoo/nyc-restaurant-violations),
which is also MIT licensed and copyright 2021 George Ho. As the MIT License
requires, the original copyright notice is kept in the [`LICENSE`](LICENSE) file
alongside the copyright for this version, which is held by False Dawn Industries.

The restaurant inspection data comes from the City of New York through
[NYC Open Data](https://opendata.cityofnewyork.us/) and is subject to its
[terms of use](https://www.nyc.gov/home/terms-of-use.page). This project is not
affiliated with or endorsed by the City of New York.
