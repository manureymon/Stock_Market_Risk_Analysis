# Stock Market Risk Analysis


## Overview

This project aims to help users decide whether or not to lend money to a publicly traded company by analyzing its financial health using two well-known models: the **Altman Z-Score** and the **Merton Model**. The application provides a user-friendly interface built with *Streamlit*, where users can input a company's ticker, the risk-free rate, and the time horizon for the loan. Based on the analysis, the app will recommend whether lending money to the company is a good idea.

## Introduction

Lending money to a company can be risky, especially if the company is financially unstable. This project uses two financial models to assess the risk of lending money to a publicly traded company:

1. Altman Z-Score: A model that predicts the likelihood of a company going bankrupt.
2. Merton Model: A model that estimates the probability of a company defaulting on its debt.

By combining these models, the application provides a comprehensive risk analysis and helps users make informed decisions.

## Theoretical Background

### Altman Z-Score

What It Is: The Altman Z-Score is a formula developed by Edward Altman in 1968 to predict the likelihood of a company going bankrupt.

How It Works: It uses financial ratios (e.g., working capital/total assets, retained earnings/total assets) to calculate a score. A higher score indicates a lower risk of bankruptcy.

Good Things:
- Simple and easy to calculate.
- Widely used and well-tested.

Bad Things:
- Less effective for non-manufacturing companies.
- Relies on historical data, which may not predict future performance.

### Merton Model

What It Is: The Merton Model, developed by Robert C. Merton in 1974, estimates the probability of a company defaulting on its debt by modeling the company's assets as a call option.

How It Works: It calculates the Distance to Default (DD) and uses it to estimate the Probability of Default (PD).

Good Things:
- Incorporates market data (e.g., stock prices) for a forward-looking analysis.
- Provides a probabilistic measure of default risk.
  
Bad Things:
- Requires accurate estimates of asset volatility.
- Assumes markets are efficient, which may not always be true.

## How It Works

User Inputs:
- Ticker: The stock symbol of the company (e.g., AAPL for Apple).
- Risk-Free Rate: The return on a risk-free investment (e.g., U.S. Treasury bonds).
- Time Horizon (T): The period over which the loan will be made (in years).

Analysis:
- The app calculates the Z-Score and the Probability of Default (PD) using the Merton Model.
- Based on the results, it decides whether to recommend lending money to the company.

Decision Rules:
- Z-Score > 3: Indicates a strong financial position.
- Probability of Default (PD) < 35%: Indicates a low risk of default.

If both conditions are met, the app recommends lending money. Otherwise, it advises against it.

*Additional Information*: The app also provides historical price charts, annual returns, and the company's balance sheet for further analysis.


## How to Run the Project

Prerequisites

1. Install Python (version 3.11 or higher).
2. Install the required libraries:

`pip install streamlit yfinance matplotlib numpy scipy`

3. Clone the repository or download the project files.
4. Open a terminal and navigate to the project directory.
5. Run the Streamlit app:
`streamlit run main.py`
This will open a page on your browser

6. Enter the company's ticker, risk-free rate, and time horizon, then click "Analyze."

## Limitations and Improvements

**Limitations**

- Data Quality: The analysis relies on accurate and up-to-date financial data from yfinance.
- Model Assumptions: Both models make simplifying assumptions that may not hold in all cases.
- Single Ticker: The app currently analyzes one company at a time.

**Improvements**

- Multiple Tickers: Allow users to analyze multiple companies simultaneously.
- More Models: Incorporate additional financial models for a more robust analysis.
- Custom Parameters: Let users adjust the decision thresholds (e.g., Z-Score > 2.5 instead of 3).

#### Author

This project was developed by **manureymon**. If you have any questions or suggestions, feel free to reach out!
