from unittest import TestCase

import pandas as pd
from pandas.util.testing import assert_frame_equal, assert_series_equal

from sfgad.modules.features.two_hop_reach import TwoHopReach


class TestTwoHopReach(TestCase):
    def setUp(self):
        # 1. time step
        self.df_1 = pd.DataFrame({'TIMESTAMP': ['2018-01-01 00:00:00', '2018-01-01 00:00:01', '2018-01-01 00:00:04'],
                                  'SRC_NAME': ['A', 'C', 'A'],
                                  'SRC_TYPE': ['NODE', 'NODE', 'NODE'],
                                  'DST_NAME': ['B', 'D', 'E'],
                                  'DST_TYPE': ['NODE', 'NODE', 'NODE']})
        self.df_1['TIMESTAMP'] = pd.to_datetime(self.df_1['TIMESTAMP'])

        # 2. time step
        self.df_2 = pd.DataFrame({'TIMESTAMP': ['2018-01-01 00:00:11', '2018-01-01 00:00:14', '2018-01-01 00:00:16'],
                                  'SRC_NAME': ['A', 'A', 'D'],
                                  'SRC_TYPE': ['NODE', 'NODE', 'NODE'],
                                  'DST_NAME': ['B', 'C', 'B'],
                                  'DST_TYPE': ['NODE', 'NODE', 'NODE']})
        self.df_2['TIMESTAMP'] = pd.to_datetime(self.df_2['TIMESTAMP'])

        # the target output of the feature after 1. (2.) time step
        self.target_df_1 = pd.DataFrame(data={'name': ['A', 'B', 'C', 'D', 'E'], 'TwoHopReach': [2, 2, 1, 1, 2]},
                                        columns=['name', 'TwoHopReach'])
        self.target_df_2 = pd.DataFrame(data={'name': ['A', 'B', 'C', 'D'], 'TwoHopReach': [3, 3, 2, 2]},
                                        columns=['name', 'TwoHopReach'])

        self.feature = TwoHopReach()

    def test_init(self):
        self.assertEqual(self.feature.names, ['TwoHopReach'])
        self.assertEqual(self.feature.neighbors, {})

    def test_reset_after_processing(self):
        # process a time step
        self.feature.process_vertices(self.df_1, 1)

        # test resetting of the dictionaries
        self.assertEqual(self.feature.neighbors, {})

    def test_result_df_shape(self):
        result_df_1 = self.feature.process_vertices(self.df_1, 1)

        self.assertEqual(result_df_1.shape, self.target_df_1.shape)

    def test_result_df_columns(self):
        result_df_1 = self.feature.process_vertices(self.df_1, 1)

        self.assertEqual(result_df_1.columns.tolist(), ['name', 'TwoHopReach'])

    def test_result_df_dtypes(self):
        result_df_1 = self.feature.process_vertices(self.df_1, 1)

        assert_series_equal(result_df_1.dtypes, self.target_df_1.dtypes)

    def test_result_df_values(self):
        result_df_1 = self.feature.process_vertices(self.df_1, 1)

        assert_series_equal(result_df_1['name'], self.target_df_1['name'])
        assert_series_equal(result_df_1['TwoHopReach'], self.target_df_1['TwoHopReach'])

    def test_overall_processing_all_nodes(self):
        # test the calculation of two-hop reach in the 1. time step ('df_1')
        assert_frame_equal(self.feature.process_vertices(self.df_1, 1), self.target_df_1)

        # test the calculation of two-hop reach in the 2. time step ('df_2')
        assert_frame_equal(self.feature.process_vertices(self.df_2, 1), self.target_df_2)

    def test_interpret_edge(self):
        # add a new edge and verify the changes in neighbors-dictionary
        self.feature.interpret_edge("B", "A")

        self.assertEqual(self.feature.neighbors["A"], ["B"])
        self.assertEqual(self.feature.neighbors["B"], ["A"])

    def test_update_neighbor(self):
        self.feature.neighbors["A"] = ["B", "C"]

        # try to add an existing neighbor
        self.feature.update_neighbor("A", "B")
        self.assertEqual(self.feature.neighbors["A"], ["B", "C"])

        # add a new neighbor
        self.feature.update_neighbor("A", "D")
        self.assertEqual(self.feature.neighbors["A"], ["B", "C", "D"])
