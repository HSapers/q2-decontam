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

import os

import qiime2.plugin.model as model
from qiime2.plugin import SemanticType

# Define a new semantic type. This is really just an abstract symbol which
# can be used to constrain/define valid compositions of actions.
Greeting = SemanticType('Greeting')

class GreetingFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        # TODO: ran out of time
        pass

GreetingDirectoryFormat = model.SingleFileDirectoryFormat(
    'GreetingFormat', 'greeting.txt', GreetingFormat)
