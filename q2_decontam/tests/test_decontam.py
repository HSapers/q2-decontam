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
from qiime2 import Metadata
import numpy as np
import pandas as pd
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
class TestsSplitBatches(TestPluginBase):

    package = 'q2_decontam.tests'

    def setUp(self):
        super().setUp()
        data = self.get_data_path('q2-decontam_test_data_metadata.tsv')
        self.data = Metadata.load(data)

        self.split_batches = self.plugin.actions['split_batches']

    def test_smoke(self):
    # will only fail if setup doesn't work
        self.assertTrue(True)

    def test_split_batches_batch_types(self):
       actual, = self.split_batches (self.data, ['extraction', 'amp_batch'])
       # returns a result that contains an artifact the ',' returns the
       # first thing in the result, the artifact itself
       # expected computed by hond
       expected = {'amp_batch_1.0': ['HMS-poorman-B', 'HMS-poorman-C', 'HMS-yates-B', 'HMS-yates-C', 'HMS-glass-beads', 'HMS-SURF-0517-M3-C', 'HMS-SURF-0517-M4-C', 'HMS-SURF-0517-C3-C', 'HMS-SURF-0517-C4-C', 'HMS-SURF-0517-M5-C', 'HMS-SURF-0517-M6-C', 'HMS-SURF-0217-M1-C', 'HMS-SURF-0217-M2-C', 'HMS-SURF-0217-C3-C', 'HMS-SURF-0217-C4-C', 'HMS-SURF-0217-M3-C', 'HMS-SURF-0217-M4-C', 'HMS-SURF-0217-M8-B'], 'amp_batch_2.0': ['HMS-SURF-0517-M1-B', 'HMS-SURF-0517-M2-B', 'HMS-SURF-0517-C1-B', 'HMS-SURF-0517-C2-B', 'HMS-neg-ext-33', 'HMS-neg-PCR-33', 'HMS-SURF-0217-M7-B', 'HMS-SURF-0217-C1-B', 'HMS-SURF-0217-C2-B', 'HMS-neg-ext--55', 'HMS-neg-PCR-55'], 'amp_batch_3.0': ['HMS-1128-M8C-28', 'HMS-0416-M3C', 'HMS-0416-M5C'], 'amp_batch_4.0': ['HMS-1128-M7C', 'HMS-1128-M8C-33', 'HMS-1128-C2C', 'HMS-1128-C3C', 'HMS-1128-M5C', 'HMS-1128-M6C', 'HMS-1128-M1B', 'HMS-1128-M2B', 'HMS-1128-C1B', 'HMS-1128-C4B', 'HMS-0416-C2C', 'HMS-0416-C3C', 'HMS-0416-M1B', 'HMS-0416-C1B', 'HMS-blank-3', 'HMS-blank-1', 'HMS-blank-2', 'HMS-PCR-neg'], 'amp_batch_5.0': ['HMS-DeMMO5-steri-140218', 'HMS-DeMMO5-steri-100517', 'HMS-DeMMO5-steri-290817', 'HMS-DeMMO5-steri-281117', 'HMS-DeMMO5-steri-160418', 'HMS-Dec-16-18-PCR-blank'], 'extraction_1': ['HMS-poorman-B', 'HMS-poorman-C', 'HMS-yates-B', 'HMS-yates-C', 'HMS-glass-beads', 'HMS-SURF-0517-M3-C', 'HMS-SURF-0517-M4-C', 'HMS-SURF-0517-C3-C', 'HMS-SURF-0517-C4-C', 'HMS-SURF-0517-M5-C', 'HMS-SURF-0517-M6-C', 'HMS-SURF-0517-M1-B', 'HMS-SURF-0517-M2-B', 'HMS-SURF-0517-C1-B', 'HMS-SURF-0517-C2-B', 'HMS-neg-ext-33', 'HMS-neg-ext--55'], 'extraction_2': ['HMS-SURF-0217-M1-C', 'HMS-SURF-0217-M2-C', 'HMS-SURF-0217-C3-C', 'HMS-SURF-0217-C4-C', 'HMS-SURF-0217-M3-C', 'HMS-SURF-0217-M4-C', 'HMS-SURF-0217-M8-B', 'HMS-SURF-0217-M7-B', 'HMS-SURF-0217-C1-B', 'HMS-SURF-0217-C2-B'], 'extraction_3': ['HMS-1128-M8C-28', 'HMS-0416-M3C', 'HMS-0416-M5C', 'HMS-1128-M7C', 'HMS-1128-M8C-33', 'HMS-1128-C2C', 'HMS-1128-C3C', 'HMS-1128-M5C', 'HMS-1128-M6C', 'HMS-1128-M1B', 'HMS-1128-M2B', 'HMS-1128-C1B', 'HMS-1128-C4B', 'HMS-0416-C2C', 'HMS-0416-C3C', 'HMS-0416-M1B', 'HMS-blank-1', 'HMS-blank-2'], 'extraction_4': ['HMS-0416-C1B', 'HMS-blank-3'], 'extraction_NorthWestern': ['HMS-DeMMO5-steri-140218', 'HMS-DeMMO5-steri-100517', 'HMS-DeMMO5-steri-290817', 'HMS-DeMMO5-steri-281117', 'HMS-DeMMO5-steri-160418'], 'extraction_nan': []}

       self.assertDictEqual(actual.view(dict), expected)
       # TODO check semantic type of actual

    def test_split_batches_no_batch_types(self):
        # this function only operated over the index therefore no data cols
        # are supplied
        data = qiime2.Metadata(pd.DataFrame(index=pd.Index(
            ['sample1', 'sample2', 'sample3', 'sample4'], name='sampleid')))
        actual, = self.split_batches (data)
        expected = {'single_batch': ['sample1', 'sample2', 'sample3', 'sample4']}
        self.assertDictEqual(actual.view(dict), expected)

    # def test_split_batches_no_batch_types(self):
    #     actual = split-batches(--m-sample-metadata-file =self.data,
    #                            --o-batches = batches.qza,
    #                            )
    #     actual = actual[].veiw(pd.Series)
    #     #expected computed by hand
    #     expected = pd.Series({})
    #     pdt.assert_series_equal(actual, expected)


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

