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
import importlib

from qiime2.plugin import Plugin, SemanticType, model

from q2_decontam.format_types import (
    RevealSectionsDirFmt, RevealAssetFormat, RevealSectionsFormat, Slides)
import q2_decontam.actions as actions


# This is the plugin object. It is what the framework will load and what an
# interface will interact with. Basically every registration we perform will
# involve this object in some way.
plugin = Plugin("decontam", version="0.0.1.dev",
                website="https://github.com/ebolyen/q2-reveal")

plugin.register_formats(RevealSectionsDirFmt, RevealSectionsFormat,
                        RevealAssetFormat)

plugin.register_semantic_types(Slides)
plugin.register_semantic_type_to_format(Slides, RevealSectionsDirFmt)


plugin.visualizers.register_function(
    function=actions.render,
    inputs={'slides': Slides},
    parameters={},
    input_descriptions={
        'slides': 'The slides to display.'
    },
    parameter_descriptions={},
    name='Render slides',
    description="Convert a reveal.js slide deck into a self-contained"
                " visualization"
)

importlib.import_module("q2_decontam.transformers")
