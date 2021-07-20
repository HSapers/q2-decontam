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

import os

import qiime2.plugin.model as model
from qiime2.plugin import SemanticType

# Define a new semantic type. This is really just an abstract symbol which
# can be used to constrain/define valid compositions of actions.
Slides = SemanticType('Slides')


class RevealSectionsFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        # TODO: ran out of time
        pass


class RevealAssetFormat(model.BinaryFileFormat):
    def _validate_(self, level='min'):
        # This is for any file that will be embeded in the presentation
        # there is no particular requirement for these files and they may
        # be anything.
        pass


class RevealSectionsDirFmt(model.DirectoryFormat):
    slides = model.File('slides.html', format=RevealSectionsFormat)
    assets = model.FileCollection('assets/.*', format=RevealAssetFormat)

    @assets.set_path_maker
    def assets_pathmaker(path):
        return os.path.join('assets', path)
