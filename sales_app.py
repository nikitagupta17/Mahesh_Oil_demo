import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Load the dataset
@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv("trans_sales_v3.csv")
    df["Expected on"] = pd.to_datetime(df["Expected on"], format='%d.%m.%Y').dt.date  # Adjust date format
    return df

@st.cache(allow_output_mutation=True)
def load_customer_data():
    return pd.read_csv("customer.csv")

def fetch_customer_details(customer_name, customer_data):
    customer_details = customer_data[customer_data["Customer"] == customer_name]
    customer_details["Last Transaction On"] = pd.to_datetime(customer_details["Last Transaction On"], format='%d.%m.%Y').dt.date  
    customer_details["Expected order date"] = pd.to_datetime(customer_details["Expected order date"], format='%d.%m.%Y').dt.date  
    return customer_details

def main():
    st.set_page_config(page_title="Sales Dashboard", page_icon=":chart_with_upwards_trend:")
    
    # Display Mahesh Oil logo on the left in the sidebar
    st.sidebar.image("ibm_logo.png", width=150, use_column_width=False)
    
    df = load_data()
    customer_data = load_customer_data()

    # Sidebar navigation
    selected_page = st.sidebar.radio("Navigate to", ["Dashboard", "Salesperson", "Customer Details"], index=0)
    
    if selected_page == "Dashboard":
        st.title("Sales Dashboard")
        st.write("### List of Customers to be Visited")
        # Set up date range for the date input
        today = datetime.today().date()
        min_date = datetime(2024, 4, 5).date()
        max_date = (min_date + timedelta(days=365))  # 1 year from April 5th, 2024
        selected_date = st.sidebar.date_input("Expected on", min_value=min_date, max_value=max_date, value=min_date)
        df_filtered = df[df["Expected on"] == selected_date].copy() 
        df_filtered.rename(columns={"Expected Value(Rs)": "Expected Value(₹)"}, inplace=True)
        df_filtered = df_filtered.sort_values(by=["Expected Value(₹)"], ascending=False)
        instructions = "Here are your upcoming visits for today, sorted by expected order value:\n"
        for index, row in df_filtered.reset_index().iterrows():
            instructions += f"Visit {row['Customer']} in {row['Location']} ({row['Segment']}) as we are expecting order value of ₹{row['Expected Value(₹)']:,}.\n"
        
        # Render the DataFrame without horizontal scrolling and without index column
        df_filtered_reset_index = df_filtered.reset_index(drop=True)  # Reset index and drop the original index column
        centered_table_html = f"<div style='text-align: center; font-size: large;'>{df_filtered_reset_index.to_html(index=False)}</div>"
        st.markdown(centered_table_html, unsafe_allow_html=True)
        
        st.write("### Instructions")
        for line in instructions.split('\n'):
            st.write(line)
        
    elif selected_page == "Salesperson":
        st.title("Salesperson Details")
        # Set up date range for the date input
        today = datetime.today().date()
        min_date = datetime(2024, 4, 5).date()
        max_date = (min_date + timedelta(days=365))  # 1 year from April 5th, 2024
        selected_date = st.sidebar.date_input("Expected on", min_value=min_date, max_value=max_date, value=min_date)
        
        salespeople = ["All"] + list(df["Assigned to"].unique())
        selected_salesperson = st.selectbox("Salesperson", salespeople)

        df_filtered = df.copy()
        if selected_salesperson != "All":
            df_filtered = df_filtered[df_filtered["Assigned to"] == selected_salesperson]
        df_filtered = df_filtered[df_filtered["Expected on"] == selected_date].copy() 
        # Define mapping for priority
        df_filtered.rename(columns={"Expected Value(Rs)": "Expected Value(₹)"}, inplace=True)
        df_filtered = df_filtered.sort_values(by=["Expected Value(₹)"], ascending=False)
        # Drop the "Assigned to" column
        df_filtered = df_filtered.drop(columns=["Assigned to"])  # Assign the modified DataFrame back to df_filtered
        
        instructions = "Here are your upcoming visits for today, sorted by expected order value:\n"
        for index, row in df_filtered.reset_index().iterrows():
            instructions += f"Visit {row['Customer']} in {row['Location']} ({row['Segment']}) as we are expecting order value of ₹{row['Expected Value(₹)']:,}.\n"
        
        # Render the DataFrame without horizontal scrolling and without index column
        df_filtered_reset_index = df_filtered.reset_index(drop=True)  # Reset index and drop the original index column
        centered_table_html = f"<div style='text-align: center; font-size: large;'>{df_filtered_reset_index.to_html(index=False)}</div>"
        st.markdown(centered_table_html, unsafe_allow_html=True)
        
        st.write("### Instructions")
        for line in instructions.split('\n'):
            st.write(line)
        
    elif selected_page == "Customer Details":
        st.title("Customer Details")
        selected_customer = st.selectbox("Select a customer", df["Customer"].unique())
        
        customer_details = fetch_customer_details(selected_customer, customer_data)
        if not customer_details.empty:
            st.write(f"### Details for - {selected_customer}", unsafe_allow_html=True)
            # Display customer details in a structured manner using HTML table
            customer_html_table = "<table style='font-size: large;'>"
            for column_name, value in customer_details.iloc[0].items():
                customer_html_table += f"<tr><td><strong>{column_name}:</strong></td><td>{value}</td></tr>"
            customer_html_table += "</table>"
            st.markdown(customer_html_table, unsafe_allow_html=True)
        else:
            st.write("No details found for the selected customer.")

if __name__ == "__main__":
    main()
