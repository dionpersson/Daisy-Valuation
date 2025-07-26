import streamlit as st
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt

# Daisy Branding (replace with real logo if available)
st.image("https://via.placeholder.com/200x80?text=Daisy+Logo", width=200)

st.title("🚀 Business Valuation Calculator")

# Intro Text
st.header("📊 Business Information")
st.markdown(
    "Please provide the following information. "
    "If you do not have any of this information or prefer not to disclose it, please leave it blank."
)

# Inputs
revenue = st.number_input("1. Total Annual Revenue ($)", min_value=0, value=1000000, step=1, format="%d")
num_employees = st.number_input("2. Number of Employees", min_value=0, step=1)
profit_margin = st.slider("3. Profit Margin (%)", 0, 100, 15)
recurring_pct = st.slider("4. Recurring Revenue (% of revenue)", 0, 100, 10)
growth_pct_input = st.slider("5. Average Growth Rate (%)", 0, 100, 10)
growth_pct = min(growth_pct_input, 25)  # Cap at 25%

# Valuation Functions
def base_valuation(revenue, margin, recurring, growth):
    m = margin / 100
    r = recurring / 100
    g = growth / 100
    Z = 10 * m
    A = 4 * r
    B = 8 * g
    X = 2.5 + Z + A + B
    return revenue * m * X

def daisy_valuation(revenue):
    return revenue * 1.45 * 0.2 * 12.5  # Daisy = revenue × 3.625

# Handle Calculate button
if "calc_done" not in st.session_state:
    st.session_state.calc_done = False

if st.button("💰 Calculate Valuations"):
    with st.spinner("Crunching the numbers..."):
        time.sleep(1)

    st.session_state.base_val = base_valuation(revenue, profit_margin, recurring_pct, growth_pct)
    st.session_state.daisy_val = daisy_valuation(revenue)
    st.session_state.pm = profit_margin
    st.session_state.gr = growth_pct
    st.session_state.rr = recurring_pct
    st.session_state.calc_done = True

# If calculation has been run, show results
if st.session_state.calc_done:
    val_base = st.session_state.base_val
    val_daisy = st.session_state.daisy_val

    df = pd.DataFrame({
        "Scenario": ["Without Daisy", "With Daisy’s Help"],
        "Valuation": [val_base, val_daisy]
    })

    fig, ax = plt.subplots()
    bars = ax.bar(df["Scenario"], df["Valuation"], color=["#2E86AB", "#F6B352"])
    ax.set_ylabel("Valuation ($)")
    ax.set_title("Business Valuation Comparison")
    ax.ticklabel_format(axis='y', style='plain')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, height * 1.01, f"${height:,.0f}", ha='center')

    st.pyplot(fig)

    st.markdown(f"**📉 Current Valuation (Without Daisy):** ${val_base:,.2f}")
    st.markdown(f"**🚀 In three years, based on Daisy’s expectations:** ${val_daisy:,.2f}")
    st.balloons()

    # Show tips if checkbox selected
    st.markdown("---")
    if st.checkbox("📈 Show 4 Ways to Improve Your Business Value"):
        pm = st.session_state.pm
        gr = st.session_state.gr
        rr = st.session_state.rr

        if pm < 10 and gr < 10 and rr < 30:
            tips = [
                "1. Improve profit margin to ~20%",
                "2. Improve recurring revenue to 30%",
                "3. Improve growth rate to over 10%",
                "4. Institute a tech stack for the business"
            ]
        elif pm < 10 and gr >= 10 and rr < 30:
            tips = [
                "1. Improve profit margin to ~20%",
                "2. Improve recurring revenue to 30%",
                "3. Institute a tech stack for the business",
                f"4. Improve growth rate to {gr + 5:.0f}%"
            ]
        else:
            tips = [
                "1. Improve recurring revenue to 30%",
                "2. Institute a tech stack for the business",
                "3. Maintain profit margins at 20% or higher",
                "4. Improve growth rate to 15% or higher"
            ]

        st.subheader("📌 Top 4 Ways to Improve Your Business Value")
        for tip in tips:
            st.markdown(f"- {tip}")
