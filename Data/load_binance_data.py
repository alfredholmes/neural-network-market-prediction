import time, datetime, csv, json, requests




def main():
	symbols = ['BTCUSDT', 'ETHBTC']
	data = get_binance_data(symbols)

	for s in symbols:
		with open(s + '_previous_year_data.csv', 'w') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_by_base_asset_volume', 'taker_buy_quote_asset_volume'])
			for line in data[s]:
				writer.writerow(line[:-1])




def get_binance_data(symbols):
	""" Queries the API to get the previous year of trades

	Arguments:
	--------------
		symbols: list of symbols traded on the binance exchange

	Returns:
	-------------
		dict of arrays with the previous years' data (9000 hours) in chronological order
	example response
		[
		  [
		    1499040000000,      // Open time
		    "0.01634790",       // Open
		    "0.80000000",       // High
		    "0.01575800",       // Low
		    "0.01577100",       // Close
		    "148976.11427815",  // Volume
		    1499644799999,      // Close time
		    "2434.19055334",    // Quote asset volume
		    308,                // Number of trades
		    "1756.87402397",    // Taker buy base asset volume
		    "28.46694368",      // Taker buy quote asset volume
		    "17928899.62484339" // Ignore.
		  ]
		]
	"""	

	today = time.mktime(datetime.date.today().timetuple())
	#365 * 24 = 8760, so look for the previous 9000 candles
	data = {s: [] for s in symbols}

	for i in range(8, 0, -1):

		start = today * 1000 - (i + 1) * 1000 * 60 * 60 * 1000
		end = today * 1000 - i * 1000 * 60 * 60 * 1000

		print(start, end)
		for symbol in symbols:
			r = requests.get('https://api.binance.com/api/v1/klines', params={'symbol': symbol, 'interval': '1h', 'startTime': int(start), 'endTime': int(end), 'limit': 1000})
			if r.status_code != 200:
				print(r, '\n' , r.text)
			data[symbol] += json.loads(r.text)


	return data

if __name__ == '__main__':
	main()