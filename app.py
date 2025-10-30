import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="E-Commerce Profit Dashboard", layout="wide")

# --- TITLE ---
st.title("🛍 E-Commerce Profit Dashboard")
st.write("Analyze your sales and find out which products bring the most profit 💹")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("📂 Upload your sales_data.csv file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV
    df = pd.read_csv(uploaded_file)

    # --- PROFIT CALCULATION ---
    df["Revenue"] = df["Price"] * df["Quantity"]
    df["Total_Cost"] = df["Cost"] * df["Quantity"]
    df["Profit"] = df["Revenue"] - df["Total_Cost"]
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

    # --- SUMMARY METRICS ---
    total_profit = df["Profit"].sum()
    total_revenue = df["Revenue"].sum()
    avg_profit_margin = (total_profit / total_revenue) * 100 if total_revenue else 0

    top_products = df.groupby("Product")["Profit"].sum().sort_values(ascending=False).head(3)

    st.divider()
    st.subheader("💰 Business Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue (₹)", f"{total_revenue:,.0f}")
    col2.metric("Total Profit (₹)", f"{total_profit:,.0f}")
    col3.metric("Avg Profit Margin (%)", f"{avg_profit_margin:.2f}")

    # --- TOP PRODUCTS ---
    st.subheader("🏆 Top Profitable Products")
    for product, profit in top_products.items():
        st.write(f"• *{product}* — ₹{profit:,.0f}")

    # --- CHARTS ---
    st.divider()
    st.subheader("📊 Visual Insights")

    col1, col2 = st.columns(2)

    # Profit by Product
    with col1:
        profit_by_product = df.groupby("Product")["Profit"].sum().reset_index()
        fig1 = px.bar(
            profit_by_product, x="Product", y="Profit",
            title="Profit by Product", color="Product", text_auto=".2s"
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Profit by Category
    with col2:
        profit_by_category = df.groupby("Category")["Profit"].sum().reset_index()
        fig2 = px.pie(
            profit_by_category, values="Profit", names="Category",
            title="Profit by Category", hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Monthly Trend
    st.subheader("📈 Profit Trend Over Time")
    monthly_profit = df.groupby(df["Date"].dt.to_period("M"))["Profit"].sum().reset_index()
    monthly_profit["Date"] = monthly_profit["Date"].astype(str)

    fig3 = px.line(
        monthly_profit, x="Date", y="Profit",
        markers=True, title="Monthly Profit Trend"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.success("✅ Dashboard generated successfully!")

else:
    st.info("👆 Please upload your sales_data.csv file to view insights.")
