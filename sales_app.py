import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Load the dataset
@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv("sales_data_v7.csv")
    df["Expected Order Date"] = pd.to_datetime(df["Expected Order Date"], format='%d.%m.%Y').dt.date  # Adjust date format
    return df

def main():
    st.set_page_config(page_title="Sales Dashboard", page_icon=":chart_with_upwards_trend:")
    
    # Display IBM logo on the right using columns
    col1, col2 = st.columns([3, 1])  # Adjust the ratio as needed
    with col1:
        st.image("ibm_logo.png", width=80, use_column_width=False)
    
    st.sidebar.image("mahesh_oil_logo.png", width=200, use_column_width=False)
    
    df = load_data()

    # Sidebar filters
    salespeople = ["All"] + list(df["Assigned to"].unique())
    selected_salesperson = st.sidebar.selectbox("Salesperson", salespeople)

    locations = ["All"] + list(df["Location"].unique())
    selected_location = st.sidebar.selectbox("Location", locations)

    # Set up date range for the date input
    today = datetime.today().date()
    min_date = datetime(2024, 4, 5).date()
    max_date = (min_date + timedelta(days=365))  # 1 year from April 5th, 2024
    selected_date = st.sidebar.date_input("Expected Order Date", min_value=min_date, max_value=max_date, value=min_date)

    # Filter the data
    df_filtered = df.copy()
    if selected_salesperson != "All":
        df_filtered = df_filtered[df_filtered["Assigned to"] == selected_salesperson]
    if selected_location != "All":
        df_filtered = df_filtered[df_filtered["Location"] == selected_location]
    df_filtered = df_filtered[df_filtered["Expected Order Date"] == selected_date]

    st.title("Sales Dashboard")
    st.write("### List of Customers to be Visited")

    if not df_filtered.empty:
        # Replace "Expected Order Value(Rs)" with "Expected Order Value(₹)"
        df_filtered.rename(columns={"Expected Order Value(Rs)": "Expected Order Value(₹)"}, inplace=True)
        st.dataframe(df_filtered.set_index("Customer").style.set_properties(subset=["Expected Order Value(₹)"], **{'text-align': 'left'}))
    else:
        st.write("No records found for the selected filters.")

if __name__ == "__main__":
    main()
