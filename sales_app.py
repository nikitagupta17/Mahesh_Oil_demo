import streamlit as st
import pandas as pd
from datetime import datetime

# Load the dataset
@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv("sales_data_v6.csv")
    df["Expected Order Date"] = pd.to_datetime(df["Expected Order Date"]).dt.date  # Convert to date only
    return df

def main():
    st.set_page_config(page_title="Sales Dashboard", page_icon=":chart_with_upwards_trend:")
    st.image("ibm_logo.png", width=80, use_column_width=False)

    st.sidebar.image("mahesh_oil_logo.png", width=200, use_column_width=False)
    
    df = load_data()

    # Sidebar filters
    salespeople = ["All"] + list(df["Assigned to"].unique())
    selected_salesperson = st.sidebar.selectbox("Salesperson", salespeople)

    locations = ["All"] + list(df["Location"].unique())
    selected_location = st.sidebar.selectbox("Location", locations)

    today = datetime.today().date()
    selected_date = st.sidebar.date_input("Expected Order Date", today)

    # Filter the data
    df_filtered = df.copy()
    if selected_salesperson != "All":
        df_filtered = df_filtered[df_filtered["Assigned to"] == selected_salesperson]
    if selected_location != "All":
        df_filtered = df_filtered[df_filtered["Location"] == selected_location]
    df_filtered = df_filtered[df_filtered["Expected Order Date"] == selected_date]

    # Sort by "Expected Order Value" column in decreasing order
    df_filtered = df_filtered.sort_values(by="Expected Order Value(Rs)", ascending=False)

    st.title("Sales Dashboard")
    st.write("### List of Customers to be Visited Today")

    if not df_filtered.empty:
        st.write(
            df_filtered.set_index("Customer")
            .style
            .set_properties(**{'text-align': 'center'})
            .set_table_styles([
                dict(selector="th", props=[("text-align", "center")]),
                dict(selector="td", props=[("text-align", "center")]),
                dict(selector=".col2", props=[("text-align", "left")])  # Left-align Expected Order Value column
            ])
        )
    else:
        st.write("No records found for the selected filters.")

if __name__ == "__main__":
    main()
