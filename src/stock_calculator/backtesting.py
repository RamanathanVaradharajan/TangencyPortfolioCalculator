import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.attributes import excel_input_names as ein

class BackTest:

    def back_test(self, frame, stocks, allocation):

        invested_amt = allocation.sum()
        total = invested_amt + ein.cash
        allocation = allocation/total
        allocation = np.array(allocation)
        cash_percentage = ein.cash/total
        

        dfs = frame["Close"]
        fig, axs = plt.subplots(4,3, figsize=(7, 5)) 
        axs = axs.flatten()

        for i, year in enumerate(range(2013, 2025)):
            year_df = dfs[dfs.index.year == year]
            prev_df = dfs[(dfs.index.year == (year - 1)) & (dfs.index.month == 12)]
            df = pd.concat([prev_df,year_df])

            monthly_df = df.resample('ME').last()
            monthly_returns = monthly_df[stocks].pct_change().dropna()
            
            portfolio_returns = []
            portfolio_dollar_value = []

            for date in monthly_returns.index:
                weighted_return = monthly_returns.loc[date].dot(allocation)
                portfolio_returns.append(weighted_return)

                invested_amt = (1+weighted_return)*invested_amt + ein.monthly_investment
                portfolio_dollar_value.append(invested_amt+ein.cash)
                
                portfolio_values = (1+monthly_returns.loc[date])*allocation
                portfolio_total_value = portfolio_values.sum() + cash_percentage
                allocation = portfolio_values/portfolio_total_value

            portfolio_returns = pd.Series(portfolio_returns, index=monthly_returns.index)
            portfolio_dollar_value = pd.Series(portfolio_dollar_value, index=monthly_returns.index)

            yearly_returns = (1+portfolio_returns).prod()-1
            portfolio_returns = portfolio_returns*100

            colors = ['green' if x >= 0 else 'red' for x in portfolio_returns]

            ax2 = axs[i].twinx()

            axs[i].bar(portfolio_returns.index.strftime('%b'), portfolio_returns, color=colors, width=0.95)
            ax2.plot(portfolio_dollar_value.index.strftime('%b'), portfolio_dollar_value, marker='o', color='blue', linestyle='-', label='Portfolio Value')  
            axs[i].set_title(f'{year}') 
            axs[i].set_ylabel('Return (%)')
            ax2.set_ylabel('Value ($)')
            axs[i].text(0.95, 0.1, f'Yearly Return: {yearly_returns:.2%}', transform=axs[i].transAxes, fontsize=8, verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        return "Done"