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

#testing functionality for a single function
#unit test - every line of code or logical branch works a test that looks at the if case and a test that
#look at the else case

class TestPrepareControlBatches(unittest.TestCase):
    def test_sample_type_col_in_control_cols(self):
        self.assertTrue(False) #write a failing test first, know test is running and failing when it should