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

# Sidebar filters
st.sidebar.title("Filters")

# Filter by Salesperson
salespeople = ["All"] + list(df["Assigned to"].unique())
selected_salesperson = st.sidebar.selectbox("Select Salesperson", salespeople)

# Filter by Location
locations = ["All"] + list(df["Location"].unique())
selected_location = st.sidebar.selectbox("Select Location", locations)

# Filter the data for today's date
df_today = df[df["Expected Order Date"].dt.date == today]

# Apply filters for location and salesperson
if selected_salesperson != "All":
    df_today = df_today[df_today["Assigned to"] == selected_salesperson]
if selected_location != "All":
    df_today = df_today[df_today["Location"] == selected_location]

# Display the table
st.title("List of Customers to be Visited Today")
st.write(df_today[["Customer", "Location", "Segment", "Expected Order Date", "Expected Order Value", "Recommended Action", "Priority", "Assigned to"]])
