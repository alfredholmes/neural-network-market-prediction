""" Python module for controlling the MLP NN used to make portfolio decisions
"""

import tensorflow as tf

class RNN:
	def __init__(self, n_entities, n_features, n_steps, hidden_layers=2, learning_rate=0.01):
		"""
			Arguments
			-------------

				n_entities: the number of currencies given
				n_features: the number of attributes per currency per time step
				n_steps: the number of time steps given in the inputs
				inputs: the input data for the network. Should be a 1 dimensional array of the price data
				price: an array of the vectors of close prices to be used in training
		"""

		#configuration
		self.hidden_layers = hidden_layers
		self.learning_rate = learning_rate

		#input tensor is an array of datasets for the network to evaluate.
		self.input_tensor = tf.placeholder(tf.float32, [None, n_steps, n_entities * n_features + 2])
		#vector of prices to use as the  is an array of portfolio weights
		self.prices = tf.placeholder(tf.float32, [None, n_entities])
		#RNN parameters
		self.weights =tf.Variable(tf.random_normal([hidden_layers, n_entities]))
		self.bias = tf.Variable(tf.random_normal([n_entities]))

		#initialize tensorflow
		self.prediction = self.rnn_eval()

		#calculate the portfolio value
		self.portfolio_value = tf.reduce_sum(tf.multiply(self.prediction,self.prices))
		# TODO: Perhaps add trading costs
		#optimize function
		self.to_minimize = - self.portfolio_value

		self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.to_minimize)

		self.session = tf.Session()
		self.session.run(tf.global_variables_initializer())


	def rnn_eval(self):
		x = tf.unstack(self.input_tensor, axis=1)
		cell = tf.contrib.rnn.BasicLSTMCell(self.hidden_layers)
		output, states = tf.contrib.rnn.static_rnn(cell, x, dtype=tf.float32)
		return tf.nn.softmax(tf.matmul(output[-1], self.weights) + self.bias)

	def basic_train(self, input, prices, testing_input, testing_prices):
		self.session.run(self.optimizer, feed_dict={self.input_tensor: input, self.prices: prices})
		return self.session.run(self.portfolio_value, feed_dict={self.input_tensor: testing_input, self.prices: testing_prices})

	
