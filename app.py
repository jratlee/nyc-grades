import streamlit as st
import pandas as pd
import requests

# Set page configuration
st.set_page_config(page_title="NYC Restaurant Violations", page_icon="🍔", layout="wide")

st.title("🍔 NYC Restaurant Violations Dashboard")
st.markdown("""
This is a web-based clone of the `eigenfoo/nyc-restaurant-violations` dashboard. 
It pulls the latest dataset from the NYC Open Data website to display restaurant inspection results and violation citations.
""")

@st.cache_data(ttl=86400) # Cache the data for 24 hours to prevent slow reloads
def load_data(limit=50000):
    # Fetch a large sample of the latest inspections via the Socrata Open Data API
    url = f"https://data.cityofnewyork.us/resource/43nn-pn8j.json?$limit={limit}&$order=inspection_date DESC"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        # Clean up the date format
        if 'inspection_date' in df.columns:
            df['inspection_date'] = pd.to_datetime(df['inspection_date']).dt.date
        return df
    else:
        st.error("Failed to fetch data from NYC Open Data.")
        return pd.DataFrame()

with st.spinner("Pulling latest dataset from NYC Open Data..."):
    df = load_data()

if not df.empty:
    st.sidebar.header("Search & Filter")
    
    # Search by Restaurant Name (DBA - Doing Business As)
    restaurant_name = st.sidebar.text_input("Search Restaurant Name (DBA)", "")
    
    # Filter by Borough
    boroughs = sorted(df['boro'].dropna().unique().tolist())
    selected_boro = st.sidebar.selectbox("Select Borough", ["All"] + boroughs)
    
    # Filter by Cuisine
    cuisines = sorted(df['cuisine_description'].dropna().unique().tolist())
    selected_cuisine = st.sidebar.selectbox("Select Cuisine", ["All"] + cuisines)
    
    # Apply filters dynamically
    filtered_df = df.copy()
    if restaurant_name:
        filtered_df = filtered_df[filtered_df['dba'].str.contains(restaurant_name, case=False, na=False)]
    if selected_boro != "All":
        filtered_df = filtered_df[filtered_df['boro'] == selected_boro]
    if selected_cuisine != "All":
        filtered_df = filtered_df[filtered_df['cuisine_description'] == selected_cuisine]
    
    st.write(f"### Showing {len(filtered_df)} violation records")
    
    # Display the data in a clean table
    display_cols =['dba', 'boro', 'cuisine_description', 'inspection_date', 'violation_description', 'critical_flag', 'grade']
    available_cols =[col for col in display_cols if col in filtered_df.columns]
    
    st.dataframe(filtered_df[available_cols].sort_values(by='inspection_date', ascending=False), use_container_width=True)
    
    # Show statistics if data is present
    if not filtered_df.empty:
        st.write("### Dashboard Statistics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top 5 Violation Descriptions**")
            if 'violation_description' in filtered_df.columns:
                violation_counts = filtered_df['violation_description'].value_counts().head(5)
                st.bar_chart(violation_counts)
                
        with col2:
            st.write("**Grades Distribution**")
            if 'grade' in filtered_df.columns:
                grade_counts = filtered_df['grade'].dropna().value_counts()
                st.bar_chart(grade_counts)

else:
    st.warning("No data available.")

st.markdown("---")
st.markdown("""
**Caveats & Notes:** 
- Only restaurants in active status are shown.
- There may be data errors or missing data as compiled from NYC administrative systems.
- Data provided by [NYC Open Data - DOHMH New York City Restaurant Inspection Results](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j).
""")
