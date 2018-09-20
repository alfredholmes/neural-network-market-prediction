# Neural Network Market Prediction
Neural network and data acquisition tools to model correlated financial markets.

Models are being developed for crypto currency trading due to ease of data and automating trades.

Project written in python 3 using Tensorflow.


Data:

	Using hourly price data for the previous year (8670 hours) 
	Currently USDBTC, ETHBTC, EOSBTC, XRPBTC, LTCBTC, XMRBTC, BCHBTC, XLMBTC markets are being tracked
	Model tries to predict the next day from the previous two weeks

	Training set is the whole set with out the randomly selected 3 weeks of testing data.