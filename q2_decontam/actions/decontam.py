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

# import glob
import pandas as pd
import subprocess
import h5py

# import qiime2 as q2
import qiime2.util
from q2_types.feature_table import BIOMV210Format

import biom
from typing import Optional, Tuple, Any, List
from ..format_types import FilterFormat
# from q2_types.feature_table import FeatureTable
# from q2_types.feature_data import Taxonomy

from ..format_types import SampleBatchesDirFmt, FeatureTableBatches

def run_commands(cmds, verbose=True):
    if verbose:
        print("Running external command line application(s). This may print "
              "messages to stdout and/or stderr.")
        print("The command(s) being run are below. These commands cannot "
              "be manually re-run as they will depend on temporary files that "
              "no longer exist.")
    for cmd in cmds:
        if verbose:
            print("\nCommand:", end=' ')
            print(" ".join(cmd), end='\n\n')
        subprocess.run(cmd, check=True)

# this needs to written as a pipeline don't need type notations, but do need
# a context object/parameter) dependency inversion/injection (inversion of
# control - external function that knows my function takes a thing chooses
# which thing to take in and plugs in )- framework will use ctx - framework
# will inject some context in here, ignore when registering
# https://dev.qiime2.org/latest/actions/pipelines/
# https://github.com/qiime2/q2-diversity/blob/
# 645aaf3c8ba52456730e354d8ba90f27987f3d50/q2_diversity/_alpha/_pipeline.py
# #L12 for each control type  - create a pipeline loop over the different
# control types

# extract a batch to extract a batch
# loop over col state to split each batch
# paralellize each batch
# feature table - each sample we have the score per feature

# |ASV|sampleID|score|batch| long format if we need custom filtering
# downstream |ASV|batch_1_score|...|batch_n_score| compatible with q2 needs
# pairing with metatdata |batch|ASV1|...|ASVn|

# metatable - arbitary number of biom tables in a table - as many files as
# we want in a azq - new format  - method - extract table, extract one table
# out of metatable
# output is a dict - k=batch, v= list of sample IDS or list of lists, in put a list of batch IDs, call fiters on feature tables
# function for filtering tables based on the list/dictionary
# |amplification_ID|extraction_ID|sequence_ID - internal dict - col headers and values - list of sets of id's for each col

# only look at one col at a time
# may not need to run if only have one batch
def split_batches(
        # don't need to explictly need a metatdata param, will be called
        # TODO warn user that they are not splitting into batches
        # warning: a single batch will be containing all sample ids
        sample_metadata: qiime2.Metadata,
        # list of batch type col headers ['ext_id', 'amp_id', 'seq_id']
        batch_types: List[str] = None,
        ) -> dict:

    batch_dict = {}
    if batch_types is not None:
        for batch_type in batch_types:
            # will raise err if not there
            col = sample_metadata.get_column(batch_type)
            series = col.to_series()
            # get list of all batch type IDs
            for batch_id in series.unique():
                k = f'{batch_type}_{batch_id}'
                v = list(series[series==batch_id].index)
                batch_dict[k] = v
    else:
        k = 'single_batch'
        v = list(sample_metadata.to_dataframe().index) # the sample ID col
        batch_dict[k] = v

    return batch_dict
#if registered, will return semantic type that it's registered with
def feature_table_batch_artifact_list(ctx, batch_set):
    artifact_list = []
    batch_dict =  batch_set.view(dict)
    for k, v in batch_dict:
        df = pd.DataFrame(index=pd.Series(v, name='ids'))
        metatdata_artifact = ctx.make_artifact(Metadata, df)
        artifact_list.append(metatdata_artifact)

        return artifact_list

#pipelines input and output artifacts, going to be running other actions that are already returning artifacts
def split_samples(ctx, table, sample_metadata, batch_types):
    # get rel actions
    filter_samples = ctx.get_action('feature_table', 'filter_samples')
    split_batches = ctx.get_action('decontam', 'split_batches') #give semantic type

    # get batches of sample IDs - BatchSet:YAML, write test to test return type based on q2 action split batches rather than the python
    batches = split_batches(sample_metadata, batch_types)
    batch_dict = batches.view(dict)

    result = SampleBatchesDirFmt()
    # create a biom table for subsets of sample ids, one table for each batch - this may be factored out into a function
    for batch, ids in batch_dict.items():
        if ids:
            df = pd.DataFrame(index=pd.Series(ids, name='ids'))
            # make/get metadata argument from the df
            filtered_table, = filter_samples(table=table, metadata=ids,)
            format = filtered_table.view(BIOMV210Format)
            path = result.batches.path_maker(batch)
            qiime2.util.duplicate(str(format), path)
#if this is called in a pipeline, you're doing something wrong
    artifact = ctx.make_artifact(FeatureTableBatches[table.type.fields[0]],
                                 result)

    return artifact

# def split_samples(ctx, table, batch_dict):
    #batch_set.view(dict)
#     # TODO change 'batch_dict' to better param name
#     filter_samples = ctx.get_action('feature_table', 'filter_samples')
#     result = SampleBatchesDirFmt()
#
#     for batch, ids in batch_dict:
#         if ids:
#             filtered_table, = filter_samples(table=table, metadata_file=ids,)
#             path = result.batches.path_maker(batch)
#             with h5py.File(path, 'wb') as file:
#                 file.write(filtered_table)
#
#     return result







# if expected['extraction_nan'] != []: explicit
#    filter_table(...)

#if expected['extraction_nan']: implicit
#    filter_table(....)


#here expected is the dict being generated (batch_dict)
# an empty list evaluates to false, will not filter a table if empty

#batch_type = col head for 'type of control batch'
#batch_id = the unique values within each batch_type col

#set of sample IDs associated with each batch_ID (that needs to be made unique)


# create a format like ymal
# turn dict into ymal
# generic ymal format that doesn't care what content is, write transform that dumps in contnet
# validator will care about content - when we see ymal format with this semantic type - we're going to chek that these are true - recycle code - can all hae different contents in dic, go into q2 types later

#q2 types- ymal fmt Ymal could keep this https://github.com/qiime2/q2-types/blob/master/q2_types/per_sample_sequences/_format.py#L217-L228
# use this but add features to it - has ununal import - grab from q2-type per_sample_sequences will not be final location....


# def prepare_control_batches(
#         ctx, table: biom.Table, # table = Artifact.load('some_table.qza')
#         sample_metadata: qiime2.Metadata,
#         sample_type_col: str,
#         experimental_samples_name: str = 'experimental') -> \
#         # Tuple[biom.Table, ...]:
# throw a doc string below header with type information to track
# see core metrics for directory structure: https://github.com/qiime2/q2-diversity/blob/ff515b3668510b19e1204b69e598177ad4b1c7de/q2_diversity/plugin_setup.py#L280
#output dir is autogened as a parameter
#returning the directory structure  - return a yaml directory format artifact
#give a semantic type to the dictory - on disk actually a yaml dir format
#save to disk as I go or create a list of feature tables as I go. Feature tables(semantic) write as biome table(format), stick into directory - coerce into artifact
#collection of things - aggregates abunch of stuff
#return f'{ft_name}_{dict_key}.table'
#     sample_metadata = sample_metadata.to_dataframe()
#     # create a list of unique values for each
#     # control type metadata col sample_type
#     control_types = set(sample_metadata[sample_type_col].unique())
#     #test to make sure the sample type col is in the list of metadata col names
#     meta_cols = set(sample_metadata.columns)
#     if sample_type_col in meta_cols: #identity (object in memory) or value
#         print('do stuff')
#     else:
#         raise ValueError(f'{sample_type_col} is not in metadata')

    # use filter samples to create a list of samples
    # where sample_type = each unique value
    # return lists of sample ids associated with each sample_type except
    # use filter features on returned lists keep only features present in at
    # least 2 samples were sample_type = experimental
    # return subsets of feature tables with features in 2 or more experimental
    # samples named by sample_type
    # pipelines interact with artifacts (higher than methods and vis) coordinate objects
    # method or vis receives some view of the data - the representation of the data
    # ctx in pipeline - get the action


#process_step ['ext', 'amp', 'seq']
#for step in process step
#    list(unique.value())



# def control_batches(table: biom.Table, # table = feature_table.view(biom.Table)
#                     sample_metadata: qiime2.Metadata,
#                     controls: list,
#                     extraction_key:Optional[str] = None,
#                     amplification_key:Optional[str] = None,
#                     sequence_run_key:Optional[str] = None) -> biom.Table:
#
#     sample_metadata = sample_metadata.to_dataframe()
#     control_col  = list(sample_metadata.col[names])
#     control_types = list(sample_metadata.nunique())
#     if control_col != control_types:
#         print('') #raise error here see python docs - value error?
#
#     dict = {}
#
#     for control_type in controls:
#         control_type_ids = list(sample_metadata[control_type].unique())
#
#         for con in control_type_ids:
#             table = filter_features(table=table,
#                                     metadata=sample_metadata,
#                                     where=[control_type] == con)
#             k = f'table_{control_type}_{con}'
#             dict[k] = table
#     # look at output, return
#     # look at dada2 - denoise single produces a bunch of outputs - u
#     # undefined number tables **put in message
#     # outputs tables list FeatureTable
#
#
#
#     if extraction_key is not None:
#         extractions = list(sample_metadata[extraction_key].unique())
#
#         for ext in extractions:
#             filter_features(table=table, metadata=sample_metadata,
#             where=[extraction_key]==ext)
#             #return table as f'table_extraction_{ext}'
#
#
#
#
# # filter table
#     # extraction_ids_ext-identifier x n
#     # amplification_ids_amp-identifier x n
#     # sequencing_ids_seq-identifier x n
#
#
# def filter_features(table: biom.Table, min_frequency: int = 0,
#                     max_frequency: int = None, min_samples: int = 0,
#                     max_samples: int = None,
#                     metadata: qiime2.Metadata = None, where: str = None,
#                     exclude_ids: bool = False,
#                     filter_empty_samples: bool = True) \
#         -> biom.Table:
#     _filter_table(table=table, min_frequency=min_frequency,
#                   max_frequency=max_frequency, min_nonzero=min_samples,
#                   max_nonzero=max_samples, metadata=metadata,
#                   where=where, axis='observation', exclude_ids=exclude_ids,
#                   filter_opposite_axis=filter_empty_samples)
#
#     return table
