import math
import pandas as pd
import numpy as np
import scipy.stats as st

from .probability_estimator import ProbabilityEstimator


class Exponential(ProbabilityEstimator):

    def __init__(self, direction='right-tailed'):

        if direction not in ['right-tailed', 'left-tailed', 'two-tailed']:
            raise ValueError("The given direction for probability calculation is not known! "
                             "Possible directions are: 'right-tailed', 'left-tailed' & 'two-tailed'.")

        self.direction = direction

    def estimate(self, features_values, reference_features_values, weights):
        """
        Takes a vertex and a reference to the database.
        Returns a list of p_values with a p_value for each given feature value in features_values. These p_values are
        calculated based on the given reference_features_values.
        :param features_values: (1 x n) dataframe with a value for each feature. Each column refers to a feature, so n
        is the number of features (no 'name'-column).
        :param reference_features_values: (m x n+1) dataframe of tuples of windows and the corresponding feature values.
        :param weights: (m x 2) dataframe with weights for the different windows.
        :return: List of p_values.
        """

        # Add the weights to a combined dataframe of reference_values and weights
        df = pd.merge(reference_features_values, weights, on="time_window")

        # Get a list of all the features for building an easy iterable
        features_list = features_values.columns.values.tolist()
        features_list.remove('name')

        p_values_list = []

        for feature_name in features_list:

            # This is the feature value for the current feature of the vertex in question
            feature_value = features_values.iloc[0][feature_name]

            mean, _ = self.weighted_mean_and_sd(df[feature_name], df['weight'])

            if self.direction == 'right-tailed':
                p_value = 1 - st.expon.cdf(feature_value, 0, 1 / mean)

            elif self.direction == 'left-tailed':
                p_value = st.expon.cdf(feature_value, 0, 1 / mean)

            else:
                p_value_right = 1 - st.expon.cdf(feature_value, 0, 1 / mean)
                p_value_left = st.expon.cdf(feature_value, 0, 1 / mean)

                p_value = 2 * min(p_value_right, p_value_left)

            # Add the calculated p_value to the list of p_values for this vertex
            p_values_list.append(p_value)

        # Return the completed list
        return p_values_list

    def weighted_mean_and_sd(self, values, weights):
        """
        Returns the weighted mean and standard deviation of the given values weighted by the given weights.
        :param values: the given feature values.
        :param weights: the weights for the values.
        :return: Weighted mean and standard deviation.
        """
        isnan = np.isnan(values)

        mean = np.average(values[~isnan], weights=weights[~isnan])
        variance = np.average((values[~isnan] - mean) ** 2, weights=weights[~isnan])

        return mean, math.sqrt(variance)
