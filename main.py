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

    # Explanation of Z-Score components
    st.subheader("Z-Score Components")
    st.write("""
    The Z-Score is calculated using the following formula en componentes:
    """)

    st.latex(r"""
        ZScore = (0.717 x_1)+ (0.847 x_2) + (3.107 x_3) + (0.42 x_4) + (0.998 x_5)
        """)

    # Calculate and display each component
    if z_score_calculator.data:
        x1 = z_score_calculator.data['working_capital'] / z_score_calculator.data['total_assets']
        x2 = z_score_calculator.data['retained_earnings'] / z_score_calculator.data['total_assets']
        x3 = z_score_calculator.data['ebit'] / z_score_calculator.data['total_assets']
        x4 = z_score_calculator.data['market_value_equity'] / z_score_calculator.data['total_liabilities']
        x5 = z_score_calculator.data['sales'] / z_score_calculator.data['total_assets']

        st.write("""
        - **X1**: Measures the company's liquidity.
          - Formula: Working Capital / Total Assets
          - Value: {:.2f}
        """.format(x1))

        st.write("""
        - **X2**: Measures the company's profitability.
          - Formula: Retained Earnings / Total Assets
          - Value: {:.2f}
        """.format(x2))

        st.write("""
        - **X3**: Measures the company's operating efficiency.
          - Formula: EBIT / Total Assets
          - Value: {:.2f}
        """.format(x3))

        st.write("""
        - **X4**: Measures the company's leverage.
          - Formula: Market Value of Equity / Total Liabilities
          - Value: {:.2f}
        """.format(x4))

        st.write("""
        - **X5**: Measures the company's asset turnover.
          - Formula: Sales / Total Assets
          - Value: {:.2f}
        """.format(x5))

    st.subheader("Distance to Default and Probability of Default")
    st.write("""
    The **Distance to Default (DD)** and **Probability of Default (PD)** are calculated using the Merton Model. 
    Here are the formulas:
    """)

    st.write("""
    ### Distance to Default (DD)
    The Distance to Default measures how far a company is from defaulting on its debt. It is calculated as:
    """)
    st.latex(r"""
    DD = \frac{\ln(V / D) + (r + \sigma^2 / 2) \cdot T}{\sigma \cdot \sqrt{T}}
    """)
    st.write("""
    Where:
    - **V**: Market value of the company's assets.
    - **D**: Market value of the company's debt.
    - **r**: Risk-free interest rate.
    - **σ**: Volatility of the company's asset value.
    - **T**: Time horizon for the loan.
    """)

    st.write("""
    ### Probability of Default (PD)
    The Probability of Default estimates the likelihood that the company will default on its debt. It is calculated as:
    """)
    st.latex(r"""
    PD = 1 - N(DD)
    """)
    st.write("""
    Where:
    - **N**: Cumulative standard normal distribution.
    - **DD**: Distance to Default.
    """)

    st.subheader("Model Parameters")

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