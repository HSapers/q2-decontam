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

import pandas as pd

import qiime2 as q2
import qiime2.util
import yaml

from q2_types.feature_table import FeatureTable
from q2_types.feature_data import Taxonomy
from q2_decontam.plugin_setup import plugin
from q2_types.per_sample_sequences import YamlFormat

from .format_types import FilterFormat

# transform Filter to CategoricalMetadataColumn(MetadataColumn)
@plugin.register_transformer
def _1(ff: FilterFormat) -> qiime2.Metadata:
    return qiime2.Metadata.load(str(ff))

# dictionary to yaml format
@plugin.register_transformer
def _2(obj: dict) -> YamlFormat:
    ff = YamlFormat() #allocate location for making a ymal
    with ff.open() as fh:
        yaml.safe_dump(obj, fh, default_flow_style = False)
    return ff

# yaml to dict
@plugin.register_transformer
def _3(ff: YamlFormat) -> dict:
    with ff.open() as fh:
        return yaml.safe_load(fh)

def tidy_data(metadata: qiime2.Metadata, tax_table: Taxonomy, feature_table: FeatureTable, outfile: str ):
    ASV_table = q2.Artifact.load(feature_table)
    ASV_df = ASV_table.view(q2.Metadata).to_dataframe()

    tax_table = q2.Artifact.load(tax_table)
    tax_df = tax_table.view(q2.Metadata).to_dataframe()

    metadata_df = pd.read_csv(metadata, sep='\t')
    # set index
    ASV_df_1 = ASV_df.reset_index()
    # change first col to sample_id
    ASV_df_1 = ASV_df_1.rename(columns={"id": "sampleid", })

    # melt into tidy df
    ASV_df_1 = pd.melt(ASV_df_1, id_vars=['sampleid'],
                       var_name='ASV', value_name='reads')
    # make reads numeric
    ASV_df_1['reads'].apply(pd.to_numeric, errors='coerce')

    # calculate relative abundance per sample
    ASV_df_1['rel_abun'] = ASV_df_1['reads'] / ASV_df_1.groupby('sampleid')['reads'].transform('sum')

    # merge with metadata
    ASV_meta_df = ASV_df_1.merge(metadata_df, on='sampleid')

    # merge with tax table
    ASV_meta_tax_df = pd.merge(ASV_meta_df,
                               tax_df,
                               left_on='ASV',
                               right_on='Feature ID'
                               )

    # create a total reads per sample column
    ASV_meta_tax_df['total_reads'] = (ASV_meta_tax_df.groupby(['sampleid'])['reads'].transform('sum'))

    #remove all ASVs that have no reads in samples in metadata
    tidy_df = ASV_meta_tax_df[ASV_meta_tax_df['read']>0]

    # see how many singletons are left after subsetting. Dada2 should get rid of singletons, but can re-inroduced after sub setting samples. We will remove these with caution - they are not true singletons, but are only observed once in the remaining samples.
    ASVs_remaining = (list(tidy_df.groupby(['ASV'])['reads'].transform('sum')))
    number_of_singletons = sum(float(num) == 1 for num in ASVs_remaining)

    # get a list of the singlton ASV names
    tidy_df['ASV_sums'] = (tidy_df.groupby(['ASV'])['reads'].transform('sum'))
    ASV_singleton_list = (list((tidy_df[(tidy_df['ASV_sums'] == 1)])['ASV']))

    # drop the singeton ASVs
    tidy_df_nos = tidy_df[tidy_df['ASV_sums'] > 1]

    # drop the extra data
    tidy_df_nos.drop(['ASV_sums'], axis=1, inplace=True)

    # write out master table as csv
    tidy_df_nos.to_csv(f"{outfile}.csv", index=False)

    # check how many samples and ASVs we have remaining
    print(('There are {} samples and {} ASVs remaining').format((len(list(tidy_df_nos['sampleid'].unique()))),
                                                                (len(list(tidy_df_nos['ASV'].unique())))))
    print('{} singleton ASVs were removed'.format(number_of_singletons))
    print('list of singleton ASVs stored as ASV_singleton_list')
    print(f'master dataframe saved as {outfile}.csv')



#return metadata or metadata  like - like list of ids - filter featureTable  - creating id sets kept or to be removed can be dropped into pipeline and filtered
#working with 3rd party tools - those tools have been optimzed in ways that I'm not going to mess with  - inherit upstream behaviour - will be faster/more reliable - call another function that already exsists
#genome sampler - set of ids
#feature table filter - pass as metadata - need a metadata transformer to convert the list of ids into metadata
#define type for long form table using python class structure

#define type for feature table filter (some function of set of things that will be removed or preserved, filter is a verb,
# but a filter can be a noun - out out the set of things using that set of it  - subtype of metadata  - a name for the filter (the list of ids) FeatureTable[Filter]
# transform to metadata - feature table differentials in q2 types lop off numeric part of code

# pipelines - actions (methods, visualizers, pipelines) all inherit from action pipelines have a context object to get a bunch of methods and run inside pipeline - reach in and grad actions from other plugins and run
