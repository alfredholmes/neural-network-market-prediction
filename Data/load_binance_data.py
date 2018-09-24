""" Script to pull data from the binance API of the previous years trades
	Writes to ../data/Symbol_Data.csv The binance API data

	as well as ./input.csv traning data for the Neural Network


"""


import time, datetime, csv, json, requests, numpy as np

import matplotlib.pyplot as plt

def main():
	symbols = ['BTCUSDT', 'ETHBTC', 'EOSBTC', 'LTCBTC', 'BCCBTC', 'XRPBTC', 'XLMBTC']
	data = get_binance_data(symbols)

	for k, v in data.items():
		print(k, len(v))

	#Write the raw data to disk
	for s in symbols:
		with open('data/' + s + '_previous_year_data.csv', 'w') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume'])
			for line in data[s]:
				writer.writerow(line[:-1])

	#generate data for NN
	""" Data vector: [ts, weekday, hour number, (open, close, log return, volume) for each currency]
	"""
	timestamps = None

	for k, v in data.items():
		current_timestamps = set()
		for hour in v:
			current_timestamps.add(hour[0])
		if timestamps is None:
			timestamps = current_timestamps
		else:
			timestamps = timestamps.intersection(current_timestamps)

	print(len(timestamps))
	log_returns = []

	for k, v in data.items():
		data[k] = [hour for hour in v if hour[0] in timestamps]	


	with open('input.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		header = ['timestamp', 'day', 'hour']
		currency_titles = ['log_return', 'open', 'close', 'volume']
		for symbol in symbols:
			header += [symbol + '_' + title for title in currency_titles]
		writer.writerow(header)
		for i in range(len(data[symbols[0]])):
			ts = data[symbols[0]][i][0]
			
			#only record the timestamp if all data is available
			if ts not in timestamps:
				continue
			
			row = [int(ts), datetime.datetime.fromtimestamp(int(ts / 1000)).strftime('%w'), int(datetime.datetime.fromtimestamp(int(ts / 1000)).strftime('%H'))]
			for symbol, d in data.items():
				row += [np.log(d[i][4] / d[i][1]), d[i][1], d[i][4] , d[i][3]]
				log_returns.append(np.log(d[i][4] / d[i][1]))
			writer.writerow(row)


	plt.hist(log_returns, 50)
	plt.show()

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

	for i in range(9, 0, -1):
		print(i)
		start = today * 1000 - (i + 1) * 1000 * 1000 * 60 * 60 
		end = today * 1000 - i * 1000 * 1000 * 60 * 60
				
		for symbol in symbols:
			r = requests.get('https://api.binance.com/api/v1/klines', params={'symbol': symbol, 'interval': '1h', 'startTime': int(start), 'endTime': int(end), 'limit': 1000})
			if r.status_code != 200:
				print(r, '\n' , r.text)
			else:
				data[symbol] += [[float(x) for x in hour] for hour in json.loads(r.text)]


	return data

if __name__ == '__main__':
	main()