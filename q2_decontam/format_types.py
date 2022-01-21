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
import pandas as pd


from qiime2.plugin import ValidationError
import qiime2
import qiime2.plugin.model as model
from qiime2.plugin import SemanticType
from q2_types.feature_table import Frequency, RelativeFrequency, BIOMV210Format
from q2_types.per_sample_sequences import YamlFormat
from q2_types.feature_table._type import FeatureTable
from q2_types.feature_data._type import FeatureData

# Define a new semantic type. This is really just an abstract symbol which
# can be used to constrain/define valid compositions of actions.

Greeting = SemanticType('Greeting')


class GreetingFormat(model.TextFileFormat):
    def _validate_(self, level='min'):
        # TODO: ran out of time
        pass

GreetingDirectoryFormat = model.SingleFileDirectoryFormat(
    'GreetingDirectoryFormat', 'greeting.txt', GreetingFormat
)


Filter = SemanticType('Filter',
                            variant_of=FeatureData.field['type'])

class FilterFormat(model.TextFileFormat):
    def _validate_(self, *args):
        try:
            md = qiime2.Metadata.load(str(self))
        except qiime2.metadata.MetadataFileError as md_exc:
            raise ValidationError(md_exc) from md_exc

        if md.column_count == 0:
            raise ValidationError('Format must contain at least 1 column')

FilterDirectoryFormat = model.SingleFileDirectoryFormat(
    'FilterDirectoryFormat', 'filter.tsv', FilterFormat)

BatchSet = SemanticType('BatchSet')

YamlDirectoryFormat = model.SingleFileDirectoryFormat(
    'YamlDirectoryFormat', 'data.yaml', YamlFormat)


FeatureTableBatches = SemanticType('FeatureTableBatches',
                                   field_names=['content'],
                                   field_members={
                                       'content': (Frequency,
                                                   RelativeFrequency)})

class SampleBatchesDirFmt(model.DirectoryFormat):
    batches = model.FileCollection(r'.*.biom',
                                     format=BIOMV210Format)
    @batches.set_path_maker
    def batches_path_maker(self, batch):
        return f'{batch}.biom'


# This call assigns a default format to a Type, not vice versa. One format
# can be the default for many types. Each type should have a single default
# format

# model.SFDF(<Name of the SFDF - should match the variable being assigned>,
# <name of internal fn>, <file format>)
# This function doesn't magically register anything - we need to manually
# register
# both FileFormat and SFDF before we can use them

# if a new type will become a .qza (FeatureTable will, RelativeFrequency
# probably will not), we must register it to a format or the framework won't
# know how to produce a .qza of that type
