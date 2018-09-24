import network, csv, random, numpy as np

def main():
	n_entities, headings, raw_data =  currency_data()

	random.seed(0)
	testing_weeks = int(0.75 * len(raw_data) / (24 * 7))
	training_set, training_prices, test_set, test_prices = fix_data(headings, raw_data, testing_weeks)
	rnn = network.RNN(n_entities, int((len(raw_data[0]) - 2) / n_entities), 7 * 24)
	for _ in range(100):
		print(rnn.basic_train(training_set, training_prices, test_set, test_prices) / testing_weeks)


def currency_data():
	""" Loads data from the file /Data/input.csv which is binance candle data which can be accessed from the API using /Data/load_binance_data.py
	the heading from the file should be of the form BTCUSDT_xxx where xxx is the measurement apart from the hour and minute integer headings
	"""
	with open('../Data/input.csv', 'r') as csvfile:
		data = []
		currencies = set()
		currency_keys = set()
		reader = csv.DictReader(csvfile)
		headings = []
		btc_row = []
		for line in reader:
			if len(currencies) == 0:
				for key in line.keys():
					if '_' in key:
						currencies.add(key.split('_')[0])
						currency_keys.add(key.split('_')[1])

				btc_row = [0, 0] + [1] * (len(currency_keys) - 2)
				btc_row_headers = ['BTCBTC_log_return', 'BTCBTC_volume'] + [k for k in currency_keys if 'volume' != k and 'log' != k]

			if len(headings) == 0:
				#sorted such that if the script is run twice, then the headings will be in the same order
				headings = sorted([k for k in line.keys()])

			data.append([float(line[h]) for h in headings] + btc_row)
	return len(currencies) + 1, headings + btc_row_headers, data


def fix_data(headings, raw_data, n_testing_weeks):
	#for hour in the dataset step, append an array of the precious weeks' data
	weekly_input = []
	#the close price for the hour after the weekly close
	next_close = []
	for i in range(len(raw_data) - 8 * 24):
		weekly_data = []

		for hour in raw_data[i:i + 7 * 24]:
			hour_nn_input = []

			for j, h in enumerate(headings):
				if h == 'BTCUSDT_log_return':
					hour_nn_input.append(-hour[j])
					continue
				if h == 'BTCUSDT_open' or h == 'BTCUSDT_close':
					hour_nn_input.append(1 / hour[j])
					continue
				if h == 'timestamp':
					continue
				if h == 'hour':
					hour_nn_input.append(hour[j] / 24)
					continue
				if h == 'day':
					hour_nn_input.append(hour[j] / 6)
					continue
				hour_nn_input.append(hour[j])


			weekly_data.append(hour_nn_input)
		next_close_data = []
		next_open_data = []
		for j, h in enumerate(headings):
			if '_close' in h:
				if 'BTCUSDT' in h:

					next_close_data.append((1 / raw_data[i + 7 * 24 + 1][j]) / (1 / raw_data[i + 7 * 24][j]))
				else:
					next_close_data.append((raw_data[i + 7 * 24 + 1][j] / raw_data[i + 7 * 24][j]))
		next_close.append(next_close_data + [1])
		# TODO: find a better way of doing this
		weekly_input.append(weekly_data)

	testing_input = []
	testing_prices = []
	for _ in range(n_testing_weeks):
		#pick a random number from the available weeks
		n = random.randint(0, len(weekly_data) - 1)
		testing_input.append(weekly_input[n])
		testing_prices.append(next_close[n])
		#delete the next week from the training data to prevent over fitting
		del weekly_input[n: n + 7 * 24]
		del next_close[n: n + 7 * 24]

	return weekly_input, next_close, testing_input, testing_prices




if __name__ == '__main__':
	main()
