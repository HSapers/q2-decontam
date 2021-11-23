#   Copyright 2021 Haley Sapers
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import unittest

import qiime2
from qiime2.plugin.testing import TestPluginBase
from qiime2 import Metadata, Artifact
import numpy as np
import pandas as pd
import biom
import yaml

import pandas.testing as pdt

from ..format_types import YamlDirectoryFormat


# testing functionality for a single function unit test - every line of code
# or logical branch works a test that looks at the if case and a test that
# look at the else case write a failing test first, know test is running and
# failing when it should setup runs before every test setup testclass runs
# before every class set up - set up context needed in tests set up data in
# the test it self eg - in order to test a method that needs a database,
# set up the connections to the database
# import module to test # from ..module import mytest
# class SomeTests(unitte

# test

# help get data path - set package as class variable, data folder inside test directory
#one class for all decontam or one for each function
# test view api - object itself, or python api - hand artifacts
#smoke test through q2 api - python code may not talk to q2 - this will catch this

#q2:https://dev.qiime2.org/latest/architecture/ artifact api written in framework but is an interface, writting towards an api - an abstract programming interface that the framework defines. The framework does the work to translate from registration to the interface - plug in should not be interface specific
#two ways of testing - try both - possible to get slightly different results

#use the tool that q2 provides to get action from framework vs importing the function
#python snake case
#cli underscore
#q2 replaces underscore with hyphens for cli
# set up is a method of testpluginbase - I want to run the setup method from the porent class
# super().setUp() creates 'plugin'
class TestsPreprocessing(TestPluginBase):

    package = 'q2_decontam.tests'

    def setUp(self):
        super().setUp()
        table = self.get_data_path('feature_table_test.biom')
        self.table = Artifact.import_data('FeatureTable[Frequency]',table)

        self.split_batches = self.plugin.actions['split_batches']
        self.split_samples = self.plugin.actions['split_samples']

    def test_smoke(self):
    # will only fail if setup doesn't work
        self.assertTrue(True)

    def test_split_batches_batch_types_categorical(self):
        # data must be categorical, only str
        data = qiime2.Metadata(pd.DataFrame(
           {'extraction': ['1', '1', np.nan, '2', '2', np.nan],
            'amplification': ['1', '1', '1', '2', '2', '2']},
           index=pd.Index(['sample1', 'sample2', 'sample3', 'sample4',
                           'sample5', 'sample6'], name='sampleid')))
        # returns a result that contains an artifact the ',' returns the
        # first thing in the result, the artifact itself
        actual, = self.split_batches(data, ['extraction', 'amplification'])
        print(actual.view(dict))
        # expected computed by hand
        expected = {'amplification_1': ['sample1', 'sample2', 'sample3'],
                    'amplification_2': ['sample4', 'sample5', 'sample6'],
                    'extraction_1': ['sample1', 'sample2'],
                    'extraction_2': ['sample4', 'sample5'],
                    'extraction_nan': []}

        self.assertDictEqual(actual.view(dict), expected)
        # TODO check semantic type of actual

    def test_split_batches_no_batch_types_categorical(self):
        # function only operated over index, no data cols supplied
        data = qiime2.Metadata(pd.DataFrame(index=pd.Index(
            ['sample1', 'sample2'], name='sampleid')))
        actual, = self.split_batches(data)
        expected = {'single_batch': ['sample1', 'sample2']}
        self.assertDictEqual(actual.view(dict), expected)

    def test_split_batches_batch_types_numerical(self):
        # data must be categorical, only str
        data = qiime2.Metadata(pd.DataFrame(
           {'extraction': [1, 1, np.nan, 2, 2, np.nan],
            'amplification': [1, 1, 1, 2, 2, 2]},
           index=pd.Index(['sample1', 'sample2', 'sample3', 'sample4',
                           'sample5', 'sample6'], name='sampleid')))
        # returns a result that contains an artifact the ',' returns the
        # first thing in the result, the artifact itself
        actual, = self.split_batches(data, ['extraction', 'amplification'])
        #print(actual.view(dict))
        # expected computed by hand
        expected = {'amplification_1.0': ['sample1', 'sample2', 'sample3'],
                    'amplification_2.0': ['sample4', 'sample5', 'sample6'],
                    'extraction_1.0': ['sample1', 'sample2'],
                    'extraction_2.0': ['sample4', 'sample5'],
                    'extraction_nan': []}

        self.assertDictEqual(actual.view(dict), expected)
        # TODO check semantic type of actual

    def test_split_samples_single(self):

        data = qiime2.Metadata(pd.DataFrame(
            {'extraction': ['1', '1', '1', np.nan, np.nan, np.nan],
             'amplification': ['1', '1', '1', '2', '2', '2']},
            index=pd.Index(['sample1', 'sample2', 'sample3', 'sample4',
                            'sample5', 'sample6'], name='sampleid')))

        actual = self.split_samples(self.table, data,
                                    ['extraction'])

        e_table = self.get_data_path('amplification_1.biom')
        expected = Artifact.import_data('FeatureTable[Frequency]',e_table)
        #TODO write out biom table see https://github.com/qiime2/q2-feature-table/blob/master/q2_feature_table/tests/test_core_features.py

        self.assertEqual(actual.view(biom.Table), expected.view(biom.Table))


    # def test_split_samples_single(self):
    #     #dict = {'amplification_1': ['sample1', 'sample2', 'sample3']}
    #     #yaml_d = yaml.safe_dump(dict, default_flow_style=False)
    #     batch_set_test = self.get_data_path('amp_1_test.yml')
    #     actual = self.split_samples(self.table, batch_set_test)
    #
    #     e_table = self.get_data_path('amplification_1.biom')
    #     expected = Artifact.import_data('FeatureTable[Frequency]',e_table)
    #
    #     self.assertEqual(actual.view(biom.Table), expected.view(biom.Table))




 # emtpy metadata - should be handled by q2
 # test empty batch type will evaluate to colname_nan
 # assert raises - when I do this things after
 #   with assert raises regex - check message  - correct value error for #2



# d = {'sampleid':['sample1', 'sample2', 'sample3', 'sample4'],
#      'sample_type':['control', 'experimental', 'experimental', 'experimental']}
# sample_metadata = pd.DataFrame(data=d)
#
#
# class TestPrepareControlBatches(unittest.TestCase):
#     def test_sample_type_col_in_control_cols(self):
#         self.assertTrue(False)
#
#     def test_meta_col(self):
#         actual = set(sample_metadata.columns)
#         expected = {'sampleid', 'sample_type'}
#         self.assertSetEqual(actual, expected)
#
#     def test_sample_type_col_in_meta_cols(self):
#         meta_cols = {'sampleid', 'sample_type'}
#         self.assertIn('sample_type', meta_cols)
#
#     def test_sample_type_col_notin_meta_cols(self):
#         meta_cols = {'sampleid', 'sample_type'}
#         self.assertNotIn('sample_type', meta_cols,
#                          'sample type column is not in metadata')

