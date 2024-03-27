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
    
    # Display IBM logo on the left
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
    min_date = datetime(2024, 4, 5).date()  # Minimum selectable date
    max_date = today  # Maximum selectable date
    selected_date = st.sidebar.date_input("Expected Order Date", min_date, min_value=min_date, max_value=max_date)

    # Filter the data
    df_filtered = df.copy()
    if selected_salesperson != "All":
        df_filtered = df_filtered[df_filtered["Assigned to"] == selected_salesperson]
    if selected_location != "All":
        df_filtered = df_filtered[df_filtered["Location"] == selected_location]
    df_filtered = df_filtered[df_filtered["Expected Order Date"] == selected_date]

    st.title("Sales Dashboard")
    st.write("### List of Customers to be Visited Today")

    if not df_filtered.empty:
        # Replace "Rs" with the rupee symbol in the "Expected Order Value" column
        df_filtered["Expected Order Value(Rs)"] = df_filtered["Expected Order Value(Rs)"].astype(str).str.replace("Rs", "₹")
        st.dataframe(df_filtered.set_index("Customer").style.set_properties(subset=["Expected Order Value(Rs)"], **{'text-align': 'left'}))
    else:
        st.write("No records found for the selected filters.")

if __name__ == "__main__":
    main()
