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
import pandas as pd

# testing functionality for a single function unit test - every line of code
# or logical branch works a test that looks at the if case and a test that
# look at the else case write a failing test first, know test is running and
# failing when it should setup runs before every test setup testclass runs
# before every class set up - set up context needed in tests set up data in
# the test it self eg - in order to test a method that needs a database,
# set up the connections to the database
# import module to test # from ..module import mytest
# class SomeTests(unitte


d = {'sampleid':['sample1', 'sample2', 'sample3', 'sample4'],
     'sample_type':['control', 'experimental', 'experimental', 'experimental']}
sample_metadata = pd.DataFrame(data=d)


class TestPrepareControlBatches(unittest.TestCase):
    def test_sample_type_col_in_control_cols(self):
        self.assertTrue(False)

    def test_meta_col(self):
        actual = set(sample_metadata.columns)
        expected = {'sampleid', 'sample_type'}
        self.assertSetEqual(actual, expected)

    def test_sample_type_col_in_meta_cols(self):
        meta_cols = {'sampleid', 'sample_type'}
        self.assertIn('sample_type', meta_cols)

    def test_sample_type_col_notin_meta_cols(self):
        meta_cols = {'sampleid', 'sample_type'}
        self.assertNotIn('sample_type', meta_cols,
                         'sample type column is not in metadata')

