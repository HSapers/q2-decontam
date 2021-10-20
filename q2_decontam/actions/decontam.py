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
# import pandas as pd
import subprocess

# import qiime2 as q2
import qiime2.util
import biom
from typing import Optional, Tuple
from ..format_types import FilterFormat
# from q2_types.feature_table import FeatureTable
# from q2_types.feature_data import Taxonomy


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

# this needs to written as a pipeline don't need type notations, but do need a
# context object/parameter)
# dependency inversion/injection (inversion of control - external function
# that knows my function takes a thing chooses which thing
# to take in and plugs in )- framework will use ctx - framework will inject
# some context in here, ignore when registering
# https://dev.qiime2.org/latest/actions/pipelines/
# https://github.com/qiime2/q2-diversity/blob/
# 645aaf3c8ba52456730e354d8ba90f27987f3d50/q2_diversity/_alpha/_pipeline.py#L12


def prepare_control_batches(
        ctx, table: biom.Table,
        sample_metadata: qiime2.Metadata,
        sample_type_col: str,
        experimental_samples_name: str = 'experimental') -> \
        Tuple[biom.Table, ...]:

    sample_metadata = sample_metadata.to_dataframe()
    # create a list of unique values for each
    # control type metadata col sample_type
    control_types = set(sample_metadata[sample_type_col].unique())
    #test to make sure the sample type col is in the list of metadata col names
    control_cols = set(sample_metadata.columns)
    if sample_type_col in control_cols: #identity (object in memory) or value
        print('do stuff')
    else:
        raise ValueError(f'{sample_type_col} is not in metadata')

    # use filter samples to create a list of samples
    # where sample_type = each unique value
    # return lists of sample ids associated with each sample_type except
    # use filter features on returned lists keep only features present in at
    # least 2 samples were sample_type = experimental
    # return subsets of feature tables with features in 2 or more experimental
    # samples named by sample_type


def control_batches(table: biom.Table,
                    sample_metadata: qiime2.Metadata,
                    controls: list,
                    extraction_key:Optional[str] = None,
                    amplification_key:Optional[str] = None,
                    sequence_run_key:Optional[str] = None) -> biom.Table:

    sample_metadata = sample_metadata.to_dataframe()
    control_col  = list(sample_metadata.col[names])
    control_types = list(sample_metadata.nunique())
    if control_col != control_types:
        print('') #raise error here see python docs - value error?

    dict = {}

    for control_type in controls:
        control_type_ids = list(sample_metadata[control_type].unique())

        for con in control_type_ids:
            table = filter_features(table=table,
                                    metadata=sample_metadata,
                                    where=[control_type] == con)
            k = f'table_{control_type}_{con}'
            dict[k] = table
    # look at output, return
    # look at dada2 - denoise single produces a bunch of outputs - u
    # undefined number tables **put in message
    # outputs tables list FeatureTable



    if extraction_key is not None:
        extractions = list(sample_metadata[extraction_key].unique())

        for ext in extractions:
            filter_features(table=table, metadata=sample_metadata,
            where=[extraction_key]==ext)
            #return table as f'table_extraction_{ext}'




# filter table
    # extraction_ids_ext-identifier x n
    # amplification_ids_amp-identifier x n
    # sequencing_ids_seq-identifier x n


def filter_features(table: biom.Table, min_frequency: int = 0,
                    max_frequency: int = None, min_samples: int = 0,
                    max_samples: int = None,
                    metadata: qiime2.Metadata = None, where: str = None,
                    exclude_ids: bool = False,
                    filter_empty_samples: bool = True) \
        -> biom.Table:
    _filter_table(table=table, min_frequency=min_frequency,
                  max_frequency=max_frequency, min_nonzero=min_samples,
                  max_nonzero=max_samples, metadata=metadata,
                  where=where, axis='observation', exclude_ids=exclude_ids,
                  filter_opposite_axis=filter_empty_samples)

    return table
