import pandas as pd
import scipy.stats as st

from .probability_estimator import ProbabilityEstimator


class Uniform(ProbabilityEstimator):

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

            min_value = min(feature_value, min(df[feature_name]))
            max_value = max(feature_value, max(df[feature_name]))

            if self.direction == 'right-tailed':
                p_value = 1 - st.uniform.cdf(feature_value, min_value, max_value - min_value)

            elif self.direction == 'left-tailed':
                p_value = st.uniform.cdf(feature_value, min_value, max_value - min_value)

            else:
                p_value_right = 1 - st.uniform.cdf(feature_value, min_value, max_value - min_value)
                p_value_left = st.uniform.cdf(feature_value, min_value, max_value - min_value)

                p_value = 2 * min(p_value_right, p_value_left)

            # Add the calculated p_value to the list of p_values for this vertex
            p_values_list.append(p_value)

        # Return the completed list
        return p_values_list
