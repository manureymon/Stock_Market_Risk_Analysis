import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from analysis import ZScore, MertonModel  # Import classes from analysis.py

# Page configuration
st.set_page_config(page_title="Stock Market Risk Analysis", layout="wide")

# Title and description
st.title("Stock Market Risk Analysis")
st.write("""
This page aims to facilitate the decision of whether or not to lend money to a publicly traded company. 
Enter the company's ticker, the risk-free rate, and the time horizon (T) for the loan.
""")

# User inputs
ticker = st.text_input("Enter the company's ticker (e.g., AAPL):", "AAPL").upper()
risk_free_rate = st.number_input("Enter the risk-free rate (e.g., 0.05 for 5%):", value=0.05, step=0.01)
T = st.number_input("Enter the time horizon (T) in years (e.g., 1.0):", value=1.0, step=0.1)

# Button to perform analysis
if st.button("Analyze"):
    # Calculate Z-Score
    z_score_calculator = ZScore(ticker)
    z_score = z_score_calculator.calculate_z_score()

    # Calculate Merton Model (Probability of Default and Distance to Default)
    merton_model = MertonModel(ticker, risk_free_rate, T)
    DD = merton_model.distance_to_default()
    PD = merton_model.probability_of_default()

    # Display results
    st.subheader("Analysis Results")
    st.write(f"Z-Score: {z_score:.2f}")
    st.write(f"Distance to Default (DD): {DD:.2f}")
    st.write(f"Probability of Default (PD): {PD * 100:.2f}%")

    # Decision logic
    if z_score > 3 and PD < 0.35:
        st.success("Go ahead, give them all your money! They will pay you ;)")
    else:
        st.error("Caution! Don't give them money!")

    # Explanation of parameters
    st.write("""
    This model uses the following parameters to make a decision:
    - **Z-Score > 3**: Indicates that the company has a strong financial position.
    - **Probability of Default (PD) < 35%**: Indicates a low risk of default.
    If either of these conditions is not met, it is suggested not to lend money.
    """)

    # Additional information for the user
    st.subheader("Additional Information for Your Analysis")

    # Historical price chart
    st.write("### Historical Price (Last Year)")
    historical_prices = yf.Ticker(ticker).history(period="1y")['Close']
    plt.figure(figsize=(10, 5))
    plt.plot(historical_prices, label="Closing Price")
    plt.title(f"Historical Price of {ticker} (Last Year)")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.legend()
    st.pyplot(plt)

    # Price table
    st.write("### Price Table (Last Year)")
    st.dataframe(historical_prices)

    # Annual return
    st.write("### Annual Return")
    returns = historical_prices.pct_change().dropna()
    st.write(f"Average daily return: {returns.mean() * 100:.2f}%")
    st.write(f"Cumulative return: {(historical_prices[-1] / historical_prices[0] - 1) * 100:.2f}%")

    # Balance Sheet
    st.write("### Balance Sheet (Last Quarter)")
    balance_sheet = yf.Ticker(ticker).quarterly_balance_sheet
    st.dataframe(balance_sheet)

# Additional note
st.write("""
**Note:** This analysis is a support tool and should not be considered financial advice. 
Conduct your own research before making investment decisions.
""")