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

from qiime2.plugin import (Plugin, Metadata)  # type q2.metadata is the object
from .actions import hello, text_vis
from .format_types import Greeting, GreetingFormat, GreetingDirectoryFormat, \
    Filter, FilterFormat, FilterDirectoryFormat
# from q2_types.feature_table import (
#    FeatureTable, Frequency, RelativeFrequency)
from q2_types.feature_data import (
    FeatureData, Taxonomy)

# could also import specific actions and put these into the registration below

# This is the plugin object. It is what the framework will load and what an
# interface will interact with. Basically every registration we perform will
# involve this object in some way.
plugin = Plugin("decontam", version="0.0.1.dev",
                website="https://github.com/Hsapers/q2-decontam")

plugin.register_semantic_types(Greeting, Filter)
plugin.register_formats(GreetingFormat, GreetingDirectoryFormat,
                        FilterFormat, FilterDirectoryFormat)

plugin.register_semantic_type_to_format(
    FeatureData[Filter], FilterDirectoryFormat)

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
    inputs={'greeting':Greeting},
    input_descriptions={'greeting':'text file returned by hello'},
    parameters={},
    parameter_descriptions={},
    name='Greeting text',
    description="generate a viewable image of the Greeting text"
)

# plugin.methods.register_function(
#     function=filter_asv_singletons,
#     inputs={'table': FeatureTable[Frequency]},
#     parameters={'sample_metadata': Metadata},
#     input_descriptions={'table': 'the feature table to be filtered'},
#     parameter_descriptions={'sample_metadata': 'metadata'},
#     outputs=[('ids_to_filter', Filter)],
#     name='remove singletons',
#     description='removes ASVs with 0 reads or singleton ASVs that may have '
#                 'been introduced during up'
#                 'stream filtering before entering the decontam pipeline.'
# )
