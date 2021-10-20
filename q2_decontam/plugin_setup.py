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

from qiime2.plugin import Plugin

from .actions import hello, text_vis
from .format_types import Greeting, GreetingFormat, GreetingDirectoryFormat

# could also import specific actions and put these into the registration below

# This is the plugin object. It is what the framework will load and what an
# interface will interact with. Basically every registration we perform will
# involve this object in some way.
plugin = Plugin("decontam", version="0.0.1.dev",
                website="https://github.com/Hsapers/q2-decontam")

plugin.register_semantic_types(Greeting)
plugin.register_formats(GreetingFormat, GreetingDirectoryFormat)
plugin.register_semantic_type_to_format(Greeting, GreetingDirectoryFormat)

plugin.methods.register_function(
    function=hello,
    inputs={},
    parameters={},
    input_descriptions={},
    parameter_descriptions={},
    outputs=[('text', Greeting)],
    name='The hello world function',
    description="print 'hello world'"
)

plugin.visualizers.register_function(
    function=text_vis,
    inputs={'greeting': Greeting},
    input_descriptions={'greeting': 'text file returned by hello'},
    parameters={},
    parameter_descriptions={},
    name='Greeting text',
    description=("generate a viewable image of the Greeting text")
)
