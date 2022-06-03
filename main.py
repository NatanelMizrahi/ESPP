import pandas as pd
from matplotlib import pyplot as plt


def compare_espp_vs_index_investment(
		expected_avg_index_annual_return_percent: float = 8,
		expected_avg_espp_annual_return_percent: float = 8,
		monthly_desposit: float = 1,
		espp_purchase_interval_months: int = 3,
		tax_tier: float = 0.47,
		espp_discount_rate_percent: float = 10,
		n_investment_years: int = 10
	) -> pd.DataFrame:
	avg_index_annual_return = expected_avg_index_annual_return_percent / 100
	avg_stock_annual_return = expected_avg_espp_annual_return_percent / 100
	espp_discount_rate = espp_discount_rate_percent / 100

	# init iterative comparison
	index_portfolio_value = 0
	espp_portfolio_value = 0
	avg_index_monthly_return = ((1 + avg_index_annual_return) ** (1 / 12)) - 1
	avg_espp_monthly_return = ((1 + avg_stock_annual_return) ** (1 / 12)) - 1

	espp_interval_deposit_sum = monthly_desposit * espp_purchase_interval_months
	espp_purchase_value = espp_interval_deposit_sum / (1 - espp_discount_rate)
	espp_period_tax_deduction = espp_discount_rate * tax_tier * monthly_desposit * espp_purchase_interval_months

	df = pd.DataFrame(columns=['ESPP', 'Index', 'Ratio'])

	for month in range(n_investment_years * 12):
		index_portfolio_value *= 1 + avg_index_monthly_return
		index_portfolio_value += monthly_desposit

		espp_portfolio_value *= 1 + avg_espp_monthly_return
		if (month != 0) and (month % espp_purchase_interval_months == 0):
			espp_portfolio_value += espp_purchase_value
			# we can treat the deducted tax as an addition to the alternative investment to ESPP
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
