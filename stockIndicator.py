import yfinance
import yahoo_fin.stock_info as si

#Return dividend yield on previous market close

def yield_on_close (ticker):
	stock = yfinance.Ticker(ticker)
	df = stock.history(period = '1d', start = '2020-1-1', end = '2020-12-31')
	try:
		return df['Dividends'].sum() / stock.info['previousClose'] * 100
	except:
		return None

def yield_on_custom_price (ticker, custom_price):
	stock = yfinance.Ticker(ticker)
	df = stock.history(period = '1d', start = '2020-1-1', end = '2020-12-31')
	try:
		return df['Dividends'].sum() / custom_price * 100
	except:
		return None

def trailing_pe (ticker):
	try:
		return yfinance.Ticker(ticker).info['trailingPe']
	except KeyError:
		return None

def actual_pe(ticker):
	stock = yfinance.Ticker(ticker)
	try:
		return float(stock.info['previousClose'] / stock.info['trailingEps'])
	except KeyError:
		return None

def trailing_eps(ticker):
	try:
		return yfinance.Ticker(ticker).info['trailingEps']
	except KeyError:
		return None

def market_value(ticker, qt):
	try:
		return yfinance.Ticker(ticker).info['previousClose'] * qt
	except KeyError:
		return None

def last_year_dividends (ticker):
	t = yfinance.Ticker(ticker)
	df = t.history(period = '1d', start = '2020-1-1', end = '2020-12-31')
	# Return last year dividends excluding taxes
	try:
		last_year_dividend = round(df[df['Dividends']>0]['Dividends'].sum() ,2)
	except KeyError:
		last_year_dividend = None
	return last_year_dividend

def last_year_dividends_df (ticker):
	t = yfinance.Ticker(ticker)
	#TODO: Set last year
	df = t.history(period = '1d', start = '2020-1-1', end = '2020-12-31')
	# return last year dividends excluding taxes
	try:
		last_year_dividend = df[df['Dividends']>0]['Dividends']
	except KeyError:
		last_year_dividend = None
	return last_year_dividend

def pe_ratio(ticker):
	try:
		return yfinance.Ticker(ticker).info['trailingPE']
	except KeyError:
		return None

def debt_on_asset(ticker):
	maxdate = '1900-1-1 00:00:00'

	df = si.get_balance_sheet(ticker)
	for d in df.columns:
		if str(d) > maxdate:
			maxdate = str(d)
	try:
		return df.loc['totalLiab', maxdate] / df.loc['totalAssets', maxdate] * 100
	except KeyError:
		return None


def analyze_stock(ticker):
	stock = {}
	stock["ticker"] = ticker
	stock["dividends"] = last_year_dividends(ticker)
	stock["yield"] = yield_on_close(ticker)
	stock["pe"] = actual_pe(ticker)
	stock["price"] = market_value(ticker, 1)
	stock["debtOnAssets"] = debt_on_asset(ticker)
	return stock
