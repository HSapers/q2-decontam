#   Copyright 2021 Evan Bolyen
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

from q2_decontam.format_types import GreetingDirectoryFormat, GreetingFormat

def hello() -> GreetingFormat:
    gf = GreetingFormat()
    with open(gf, 'w') as output_gh:
        output_gh.write("hello World!")
        return gf
