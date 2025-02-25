import yfinance as yf
import numpy as np
from scipy.stats import norm

class ZScore:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.data = self.get_data()

    def get_data(self):
        try:
            stock = yf.Ticker(self.ticker)
            balance_sheet = stock.quarterly_balance_sheet
            income_statement = stock.quarterly_financials

            # Extraer los valores necesarios
            total_assets = balance_sheet.loc['Total Assets'].iloc[0]
            working_capital = balance_sheet.loc['Working Capital'].iloc[0]
            retained_earnings = balance_sheet.loc['Retained Earnings'].iloc[0]
            total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[0]
            market_value_equity = stock.info['marketCap']

            # Para EBIT (Operating Income) y Sales (Total Revenue)
            # Nota: yfinance no siempre tiene una fila llamada "EBIT", pero puede tener "Operating Income"
            ebit = income_statement.loc['Operating Income'].iloc[0]  # Usar "Operating Income" como aproximación de EBIT
            sales = income_statement.loc['Total Revenue'].iloc[0]  # Usar "Total Revenue" como Sales

            data = {
                'total_assets': total_assets,
                'working_capital': working_capital,
                'retained_earnings': retained_earnings,
                'ebit': ebit,
                'total_liabilities': total_liabilities,
                'market_value_equity': market_value_equity,
                'sales': sales
            }
            return data
        except Exception as e:
            print(f'Error retrieving data: {e}')
            return None

    def calculate_z_score(self) -> float:
        if not self.data:
            return None

        # Calcular las variables X1, X2, X3, X4, X5
        x1 = self.data['working_capital'] / self.data['total_assets']
        x2 = self.data['retained_earnings'] / self.data['total_assets']
        x3 = self.data['ebit'] / self.data['total_assets']
        x4 = self.data['market_value_equity'] / self.data['total_liabilities']
        x5 = self.data['sales'] / self.data['total_assets']

        # Calcular el Z-Score
        z_score = (0.717 * x1) + (0.847 * x2) + (3.107 * x3) + (0.420 * x4) + (0.998 * x5)
        return z_score


class MertonModel:
    def __init__(self, ticker: str, risk_free_rate: float, T: float):
        self.ticker = ticker.upper()
        self.risk_free_rate = risk_free_rate  # Tasa libre de riesgo (anualizada)
        self.T = T  # Horizonte temporal (en años)
        self.data = self.get_data()
        self.asset_volatility = self.calculate_asset_volatility()

    def get_data(self):
        try:
            stock = yf.Ticker(self.ticker)
            balance_sheet = stock.quarterly_balance_sheet
            market_cap = stock.info['marketCap']  # Valor de mercado del equity (E)
            historical_prices = stock.history(period="1y")['Close']  # Precios históricos para calcular la volatilidad

            # Extraer los valores necesarios
            total_assets = balance_sheet.loc['Total Assets'].iloc[0]  # Valor de los activos (V)
            total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[0]  # Valor de la deuda (D)

            data = {
                'market_cap': market_cap,
                'total_assets': total_assets,
                'total_liabilities': total_liabilities,
                'historical_prices': historical_prices
            }
            return data
        except Exception as e:
            print(f'Error retrieving data for {self.ticker}: {e}')
            return None

    def calculate_asset_volatility(self):
        if not self.data:
            return None

        # Calcular los rendimientos diarios de los precios históricos
        returns = self.data['historical_prices'].pct_change().dropna()

        # Calcular la volatilidad anualizada de los rendimientos
        volatility = returns.std() * np.sqrt(252)  # 252 días de trading en un año
        return volatility

    def distance_to_default(self):
        if not self.data or not self.asset_volatility:
            return None

        V = self.data['total_assets']  # Valor de los activos
        D = self.data['total_liabilities']  # Valor de la deuda
        r = self.risk_free_rate  # Tasa libre de riesgo
        sigma = self.asset_volatility  # Volatilidad de los activos
        T = self.T  # Horizonte temporal

        # Calcular la distancia al incumplimiento (DD)
        numerator = np.log(V / D) + (r + (sigma ** 2) / 2) * T
        denominator = sigma * np.sqrt(T)
        DD = numerator / denominator

        return DD

    def probability_of_default(self):
        if not self.data or not self.asset_volatility:
            return None

        DD = self.distance_to_default()
        if DD is None:
            return None

        # Calcular la probabilidad de incumplimiento (PD)
        PD = 1 - norm.cdf(DD)
        return PD
