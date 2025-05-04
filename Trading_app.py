import streamlit as st
st.set_page_config(
    page_title="Trading page",
    page_icon="chart_with_downwards_trend:",
    layout="wide"
)

# Title and header
st.title("Trading Guide App 📊")
st.header("We Provide  information for stock Analysis")

st.image("app.jpg")
# Services section
st.markdown("## We Provide the Following Services:")
st.markdown("### :one: Stock Information")
st.write("Through this page, you can get information about stocks.")
st.markdown("### :two: Stock Prediction")
st.write("Through this page, you can predict the price of stocks.")
