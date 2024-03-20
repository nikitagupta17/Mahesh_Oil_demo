import streamlit as st
import pandas as pd
from datetime import datetime

# Load the dataset
@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv("sales_data2.csv")
    df["Expected Order Date"] = pd.to_datetime(df["Expected Order Date"])  # Convert to datetime
    return df

df = load_data()

# Get today's date
today = datetime.today().date()

# Filter the data for today's date
df_today = df[df["Expected Order Date"].dt.date == today]

# Sort the data by Expected Order Value
sorted_df_today = df_today.sort_values(by="Expected Order Value", ascending=False)

# Display the list of customers to be visited today
st.title("List of Customers to be Visited Today")
st.write(sorted_df_today[["Customer", "Location", "Segment", "Expected Order Date", "Expected Order Value", "Recommended Action", "Priority", "Assigned to"]])

# Sidebar filters
st.sidebar.title("Filters")

# Filter by Salesperson
selected_salesperson = st.sidebar.selectbox("Select Salesperson", df["Assigned to"].unique())

# Filter by Location
selected_location = st.sidebar.selectbox("Select Location", df["Location"].unique())

# Apply filters for location and salesperson
filtered_df = df[(df["Location"] == selected_location) & (df["Assigned to"] == selected_salesperson)]

# Filter the data for today's date after applying salesperson and location filters
filtered_df_today = filtered_df[filtered_df["Expected Order Date"].dt.date == today]

# Sort the filtered dataframe by Expected Order Value
sorted_filtered_df_today = filtered_df_today.sort_values(by="Expected Order Value", ascending=False)

# Display the sorted list of customers based on location and salesperson for today
st.title("Filtered List based on Location and Salesperson for Today")
st.write(sorted_filtered_df_today[["Customer", "Location", "Segment", "Expected Order Date", "Expected Order Value", "Recommended Action", "Priority", "Assigned to"]])
