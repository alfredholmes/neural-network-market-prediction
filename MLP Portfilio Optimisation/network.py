""" Python module for controlling the MLP NN used to make portfolio decisions
"""

import tensorflow as tf

class MLP_NN:
	def __init__(n_entities, n_features, n_steps, inputs, price):
		"""
			Arguments
			-------------

				n_entities: the number of currencies given
				n_features: the number of attributes per currency per time step
				n_steps: the number of time steps given in the inputs
				inputs: the input data for the network. Should be a 1 dimensional array of the price data
				price: an array of the vectors of close prices to be used in training
		"""



		