import pandas as pd
from matplotlib import pyplot as plt

"""
HOW TO USE:
Change the parameters above and run the script.

NOTES:
The following far-fetched assumptions have been made to simplify the analysis:
* Both the stock and index have a fixed, evenly-distributed average monthly return. For example, if the average annual return is set to 8%, the monthly return needs to be 0.643% to compound to 8% annually.
* The tax otherwise deducted in the ESPP option is used as an addition to the alternative investment in the index.
* The stock's return is greater or equal to the index's return. why? 
	(a) Simplification. This way, neglecting fees, using a quick-sell upon purchase and reinvesting the profits in an index is worse than or identical to keeping the stock.
	(b) If you don't believe this is the case, you should seriously consider quitting your job 😛

DISCLAIMER:
I am not a financial advisor. Do not take anything in this script as financial advice.
"""
BUY_WITH_LOWEST_STOCK_PRICE_IN_PERIOD = True
EXPECTED_AVERAGE_INDEX_ANNUAL_RETURN_PERCENT = 8
EXPECTED_AVERAGE_ESPP_ANNUAL_RETURN_PERCENT = 8
ESPP_PURCHASE_INTERVAL_MONTHS = 3
TAX_TIER_PERCENT = 47
ESPP_DISCOUNT_RATE_PERCENT = 10
N_INVESTMENT_YEARS = 10
MONTHLY_DEPOSIT = 1000


def compare_espp_vs_index_investment(
		buy_with_lowest_stock_price_in_period: bool = BUY_WITH_LOWEST_STOCK_PRICE_IN_PERIOD,
		expected_avg_index_annual_return_percent: float = EXPECTED_AVERAGE_INDEX_ANNUAL_RETURN_PERCENT,
		expected_avg_espp_annual_return_percent: float = EXPECTED_AVERAGE_ESPP_ANNUAL_RETURN_PERCENT,
		monthly_desposit: float = MONTHLY_DEPOSIT,
		espp_purchase_interval_months: int = ESPP_PURCHASE_INTERVAL_MONTHS,
		tax_tier_percent: float = TAX_TIER_PERCENT,
		espp_discount_rate_percent: float = ESPP_DISCOUNT_RATE_PERCENT,
		n_investment_years: int = N_INVESTMENT_YEARS,
	) -> pd.DataFrame:

	avg_index_annual_return = expected_avg_index_annual_return_percent / 100
	avg_stock_annual_return = expected_avg_espp_annual_return_percent / 100
	espp_fixed_discount_rate = espp_discount_rate_percent / 100
	tax_tier = tax_tier_percent / 100

	# init iterative comparison
	index_portfolio_value = 0
	espp_portfolio_value = 0
	avg_index_monthly_return = ((1 + avg_index_annual_return) ** (1 / 12)) - 1
	avg_espp_monthly_return = ((1 + avg_stock_annual_return) ** (1 / 12)) - 1

	espp_compound_return_discount_rate = 0
	if buy_with_lowest_stock_price_in_period:
		# When the stock is bought with the lowest price in the period, assuming an evenly-distibuted average monthly return, the additional discount will be equivalent to the compund return in this period
		# For example: if a stock is up 50% in 3 months, we can add those 50% to the discount
		espp_compound_return_discount_rate = ((1 + avg_espp_monthly_return) ** ESPP_PURCHASE_INTERVAL_MONTHS) - 1

	espp_interval_deposit_sum = monthly_desposit * espp_purchase_interval_months

	total_discount_rate = espp_fixed_discount_rate + espp_compound_return_discount_rate
	# the value of the purchased stocks is inverse to (1 - total discount).
	# For example, if the total discount is 50% we get twice as many stocks: (1 / (1 - 0.5)) = 2.
	espp_purchase_value = espp_interval_deposit_sum / (1 - total_discount_rate)

	total_discount = espp_purchase_value - espp_interval_deposit_sum
	espp_period_tax_deduction = total_discount * tax_tier

	df = pd.DataFrame(columns=['ESPP', 'Index', 'Ratio'])

	for month in range(n_investment_years * 12):
		index_portfolio_value *= 1 + avg_index_monthly_return
		index_portfolio_value += monthly_desposit

		espp_portfolio_value *= 1 + avg_espp_monthly_return
		if (month != 0) and (month % espp_purchase_interval_months == 0):
			espp_portfolio_value += espp_purchase_value
			# NOTE: we can treat the deducted tax as an addition to the alternative investment to ESPP
			index_portfolio_value += espp_period_tax_deduction

		df = df.append({
			'ESPP': espp_portfolio_value,
			'Index': index_portfolio_value,
			'Ratio': espp_portfolio_value / index_portfolio_value
		},
			ignore_index=True)

	return df


def plot_espp_vs_index_investment(df: pd.DataFrame):
	pd.options.display.max_rows = None
	pd.options.display.float_format = "{:,.2f}".format
	print(df)

	df['Ratio'].plot()
	plt.locator_params(nbins=30)
	plt.title('ESPP vs Index Investment')
	plt.xlabel('Month')
	plt.ylabel('ESPP / Index projected profit ratio')
	plt.show()


if __name__ == '__main__':
	df = compare_espp_vs_index_investment()
	plot_espp_vs_index_investment(df)
