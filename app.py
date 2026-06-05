import streamlit as st
import pandas as pd
import requests

# Socrata Open Data API endpoint for the DOHMH NYC Restaurant Inspection Results dataset.
DATA_URL = "https://data.cityofnewyork.us/resource/43nn-pn8j.json"
DATASET_PAGE = (
    "https://data.cityofnewyork.us/Health/"
    "DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j"
)
DEFAULT_LIMIT = 50000
REQUEST_TIMEOUT = 30  # seconds

# Project links and attribution
REPO_URL = "https://github.com/jratlee/nyc-grades"
README_URL = "https://github.com/jratlee/nyc-grades/blob/main/README.md"
ORIGINAL_PROJECT_URL = "https://github.com/eigenfoo/nyc-restaurant-violations"

# Set page configuration
st.set_page_config(page_title="NYC Restaurant Violations", page_icon="🍔", layout="wide")

st.title("🍔 NYC Restaurant Violations Dashboard")
st.markdown(
    "A web-based clone of the [`eigenfoo/nyc-restaurant-violations`]"
    "(https://github.com/eigenfoo/nyc-restaurant-violations) dashboard. "
    "It pulls the latest data from NYC Open Data so you can look up restaurant "
    "inspection results and the violations they were cited for."
)


@st.cache_data(ttl=86400)  # Cache the data for 24 hours to prevent slow reloads
def load_data(limit: int = DEFAULT_LIMIT) -> pd.DataFrame:
    """Fetch a sample of the latest inspections via the Socrata Open Data API."""
    params = {"$limit": limit, "$order": "inspection_date DESC"}
    try:
        response = requests.get(DATA_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        st.error(f"Failed to fetch data from NYC Open Data: {exc}")
        return pd.DataFrame()

    df = pd.DataFrame(response.json())

    # Normalize the date column; invalid/missing values become NaT instead of raising.
    if "inspection_date" in df.columns:
        df["inspection_date"] = pd.to_datetime(
            df["inspection_date"], errors="coerce"
        ).dt.date

    return df


with st.spinner("Pulling latest dataset from NYC Open Data..."):
    df = load_data()

if not df.empty:
    st.sidebar.header("Search & Filter")

    # Search by Restaurant Name (DBA - Doing Business As)
    restaurant_name = st.sidebar.text_input("Search Restaurant Name (DBA)", "")

    # Filter by Borough
    if "boro" in df.columns:
        boroughs = sorted(df["boro"].dropna().unique().tolist())
        selected_boro = st.sidebar.selectbox("Select Borough", ["All"] + boroughs)
    else:
        selected_boro = "All"

    # Filter by Cuisine
    if "cuisine_description" in df.columns:
        cuisines = sorted(df["cuisine_description"].dropna().unique().tolist())
        selected_cuisine = st.sidebar.selectbox("Select Cuisine", ["All"] + cuisines)
    else:
        selected_cuisine = "All"

    # Apply filters dynamically
    filtered_df = df.copy()
    if restaurant_name and "dba" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["dba"].str.contains(restaurant_name, case=False, na=False)
        ]
    if selected_boro != "All":
        filtered_df = filtered_df[filtered_df["boro"] == selected_boro]
    if selected_cuisine != "All":
        filtered_df = filtered_df[filtered_df["cuisine_description"] == selected_cuisine]

    st.write(f"### Showing {len(filtered_df):,} inspection-violation records")
    st.caption(
        f"Loaded the {len(df):,} most recent records from NYC Open Data. "
        "Each row represents a single violation cited during an inspection."
    )

    # Display the data in a clean table
    display_cols = [
        "dba",
        "boro",
        "cuisine_description",
        "inspection_date",
        "violation_description",
        "critical_flag",
        "grade",
    ]
    available_cols = [col for col in display_cols if col in filtered_df.columns]

    sort_col = "inspection_date" if "inspection_date" in available_cols else available_cols[0]
    table_df = filtered_df[available_cols].sort_values(by=sort_col, ascending=False)

    st.dataframe(table_df, use_container_width=True, hide_index=True)

    st.download_button(
        label="⬇️ Download these results as CSV",
        data=table_df.to_csv(index=False).encode("utf-8"),
        file_name="nyc_restaurant_violations.csv",
        mime="text/csv",
    )

    # Show statistics if data is present
    if not filtered_df.empty:
        st.write("### Dashboard Statistics")
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Top 5 Violation Descriptions**")
            if "violation_description" in filtered_df.columns:
                violation_counts = (
                    filtered_df["violation_description"].value_counts().head(5)
                )
                st.bar_chart(violation_counts)

        with col2:
            st.write("**Grade Distribution**")
            if "grade" in filtered_df.columns:
                grade_counts = filtered_df["grade"].dropna().value_counts()
                st.bar_chart(grade_counts)

else:
    st.warning("No data available. Please try reloading the page in a moment.")

st.markdown("---")
st.markdown(
    f"""
**A few things to keep in mind:**
- This dashboard loads only the **{DEFAULT_LIMIT:,} most recent** inspection records, not the full history.
- The source data is compiled from NYC administrative systems, so it can contain errors or gaps.
- Grades and critical flags reflect the inspection they were recorded on, which may not match a restaurant's current status.
- Data comes from [NYC Open Data: DOHMH New York City Restaurant Inspection Results]({DATASET_PAGE}).
"""
)

st.markdown("---")
st.markdown(
    f"""
**About this project**

📖 [Documentation & README]({README_URL}) &nbsp;•&nbsp; 💻 [Source code]({REPO_URL})

This dashboard is an open-source clone of
[`eigenfoo/nyc-restaurant-violations`]({ORIGINAL_PROJECT_URL}) by George Ho.
It is released under the [MIT License](https://github.com/jratlee/nyc-grades/blob/main/LICENSE). The original work is copyright 2021 George Ho,
and this version is copyright 2026 False Dawn Industries. This project is not
affiliated with or endorsed by the City of New York.
"""
)
