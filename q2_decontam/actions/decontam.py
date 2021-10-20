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

import glob
import subprocess
import pandas as pd
import biom
from typing import Optional, Tuple

import qiime2 as q2
import qiime2.util


from ..format_types import FilterFormat


#from q2_types.feature_table import FeatureTable
#from q2_types.feature_data import Taxonomy
#no subtypes?

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


def filter_asv_singletons (table: biom.Table,
                           sample_metadata: q2.Metadata) -> FilterFormat:

    ASV_df = table.to_dataframe()
    ASV_df.reset_index(inplace=True)
    ASV_df.rename(columns={"id": "sampleid", })

    meta_df=sample_metadata.to_dataframe()
    print(meta_df)
    #meta_df = pd.read_csv(sample_metadata, sep='\t')

    ASV_df = pd.melt(ASV_df, id_vars=['sampleid'],
                        var_name='ASV', value_name='reads')
    ASV_df['reads'].apply(pd.to_numeric, errors='coerce')
    ASV_meta_df = ASV_df.merge(meta_df, on='sampleid')
    temp_1_df = ASV_meta_df[ASV_meta_df['read'] > 0]

    ASVs_remaining = (list(temp_1_df.groupby(['ASV'])['reads'].transform('sum')))
    number_of_singletons = sum(float(num) == 1 for num in ASVs_remaining)

    temp_1_df['ASV_sums'] = (temp_1_df.groupby(['ASV'])['reads'].transform('sum'))
    ASV_singleton_list = (list((temp_1_df[(temp_1_df['ASV_sums'] == 1)])['ASV']))

    temp_2_df = temp_1_df[temp_1_df['ASV_sums'] > 1]

    temp_2_df.drop(['ASV_sums'], axis=1, inplace=True)

    filter_df = pd.DataFrame(ASV_singleton_list, columns=['ASV'])
    filter_df[filter]='singleton'

    print(('There are {} samples and {} ASVs remaining').format((len(list(temp_2_df['sampleid'].unique()))),
                                                                 (len(list(temp_2_df['ASV'].unique())))))
    print('{} singleton ASVs were removed'.format(number_of_singletons))

    #return pd.Series(ASV_singleton_list)
    return filter_df.to_csv(index=False, sep= '/t')

#this needs to written as a pipeline don't need type notations, but do need a context object/parameter)
#dependency inversion/injection (inversion of control - external function taht knows my function takes a thing chooses which thing
# to take in and plugs in )- framework will use ctx - framework will inject some context in here, ignore when registering
#https://dev.qiime2.org/latest/actions/pipelines/
#https://github.com/qiime2/q2-diversity/blob/645aaf3c8ba52456730e354d8ba90f27987f3d50/q2_diversity/_alpha/_pipeline.py#L12

def prepare_control_batches(ctx, table: biom.Table, sample_metadata: qiime2.Metadata, sample_type_col: str,
                            experimental_samples_name: str = 'experimental') -> Tuple[biom.Table, ...]:

    sample_metadata = sample_metadata.to_dataframe()
    #create a list of unique values for each control type metadata col sample_type
    control_types = set(sample_metadata[sample_type_col].unique())
    #test to make sure the sample type col is in the list of metadata col names
    control_cols = set(sample_metadata.columns)
    if sample_type_col in control_cols: #identity (object in memory) or value
        print('do stuff')
    else:
        raise ValueError(f'{sample_type_col} is not in metadata')

    # #use filter samples to create a list of samples where sample_type = each unique value
    # return lists of sample ids associated with each sample_type except
    # use filter features on returned lists keep only features present in at least 2 samples were sample_type = experimental
    # return subsets of feature tables with features in 2 or more experimental samples named by sample_type


def control_batches (table: biom.Table,
                           sample_metadata: qiime2.Metadata,
                            controls: list,
                        extraction_key:Optional[str] = None,
                        amplification_key:Optional[str] = None,
                        sequence_run_key:Optional[str] = None)  -> biom.Table:#is this the Stype, Ptype what the transformer takes in out what it outputs?

    sample_metadata = sample_metadata.to_dataframe()
    control_col  = list(sample_metadata.col[names])
    control_types = list(sample_metadata.nunique())
    if control_col != control_types
        print('') #raise error here see python docs - value error?

    dict = {}

    for control_type in controls:
        control_type_ids = list(sample_metadata[control_type].unique())

        for con in control_type_ids:
            table = filter_features(table=table, metadata=sample_metadata, where=[control_type] == con)
            k = f'table_{control_type}_{con}'
            dict[k] = table
    #look at output, return
    #look at dada2 - denoise single produces a bunch of outputs - undefined number tables **put in message
    #outputs tables list FeatureTable



    if extraction_key is not None:
         extractions = list(sample_metadata[extraction_key].unique())

        for ext in extractions:
            filter_features(table=table, metadata=sample_metadata, where=[extraction_key]==ext)
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



def remove_ASVs_unique_to_controls(data, suffix):
    """this function will remove all ASVs that are only present in control samples in the current sample
    extraction group for ASVs that comprise at least the current min relative abundance in each sample.
    Three files are returned: a dataframe with the ASVs removed, and a dataframe with the ASVs unique to
    controls in one col and ASVs in both controls and experimental samples in the other col

    function to split tables - helper function used internally - split into extraction batches and amplification batches
    from metatdata derive the subsets  - need to define the sets of samples that we care about
    -one of the following
    -extraction set
    -amplification set
    -sequencing set

    1) define batch
    biom api - split down into subsets

    2) don't score any ASV not present in at least 2 experimental samples
    -this will remove ASVs only in controls regardless of the number of control wihthin a batch
    -not being scored, just removed to decontam
    -creates a sub-pop of ASVs to score
    -inflate rel ab of contaminants we care about in control samples, give them a higher score, allowing
    for a less sensitive threshold
    within a batch
    ASV needs to be in >2 samples  - ask if only samples
# return 2 col matrix with ASV id and sample id
# need new filter function as well


    """

#parameterize the column names for sequence run and extraction

    sequence_run_list = list(data['sequence_run'].unique())
    lol = []
    for run in sequence_run_list:
        ext_list = list((data[data['sequence_run'] == run])['extraction'].unique())
        lol.append(ext_list)
    extractions = dict(zip(sequence_run_list, lol))

    print('there are {} input ASVs'.format(len(data['ASV'].unique())))

    count = 1

    for k, v in extractions.items():
        count = count + 1
        extraction_group = k
        extraction = v

        df = data[(data['extraction'].isin(extraction))]
        ASV_remove = []
        ASV_experimental = []

        control_ASV = list((df[
            df['sample_type'].str.contains('control') & (df['rel_abun'] > 0) & (df['extraction'].isin(extraction))])[
                               'ASV'].unique())
        Experimental_ASV = list((df[df['sample_type'].str.contains('experimental') & (df['rel_abun'] > 0) & (
            df['extraction'].isin(extraction))])['ASV'].unique())

        ASV_input = len(df['ASV'].unique())

        for ASV in control_ASV:
            if ASV in Experimental_ASV:
                ASV_experimental.append(ASV)
            else:
                ASV_remove.append(ASV)

        ASV_unique_to_controls_removed = df[~df['ASV'].isin(ASV_remove)]
        ASV_remove = pd.DataFrame(ASV_remove, columns=['ASV'])
        ASV_remove['source'] = 'unique to ext group {}'.format(extraction_group)

        # print(('there are {} ASVs in input table and {} ASVs in controls and {} ASVs in Experimental').format(ASV_input, (len(control_ASV)), (len(Experimental_ASV))))
        print('removed {} ASVs from the experimental samples in extractions {}'.format((len(ASV_remove)), extraction))

        filename = 'ASV_removed_{}'.format(extraction_group)
        filename2 = 'ASV_control_ext_group_{}'.format(extraction_group)

        ASV_unique_to_controls_removed.to_csv(('{}.csv'.format(filename)), index=False)
        ASV_remove.to_csv(('{}.csv'.format(filename2)), index=False)

    filenamelist = glob.glob('ASV_removed*.csv')
    dataframes = [pd.read_csv(f) for f in filenamelist]
    controls_removed = pd.concat(dataframes)

    filenamelist2 = glob.glob('ASV_control_ext_group_*.csv')
    dataframes2 = [pd.read_csv(f) for f in filenamelist2]
    ASVs_removed = pd.concat(dataframes2)

    # re-calculate total reads and rel_abun
    controls_removed.drop('rel_abun', axis=1, inplace=True)  # drop rel_abun col
    controls_removed.drop('total_reads', axis=1, inplace=True)
    controls_removed['rel_abun'] = controls_removed['reads'] / controls_removed.groupby('sampleid')['reads'].transform(
        'sum')
    controls_removed['total_reads'] = (controls_removed.groupby(['sampleid'])['reads'].transform('sum'))

    controls_removed.to_csv(('master_{}.csv'.format(suffix)), index=False)
    ASVs_removed.to_csv(('ASV_unique_to_controls.csv'), index=False)

    # print(('{} ASVs were removed in total').format(len(ASVs_removed['ASV'])))
    print(('There are {} samples and {} ASVs remaining').format((len(list(controls_removed['sampleid'].unique()))),
                                                                (len(list(controls_removed['ASV'].unique())))))

    return print(
        'master with ASVs unique to controls removed saved at master_{}.csv, table of ASVs removed saved at ASV_unique_to_controls.csv'.format(
            suffix))


def update_tables(feature_table, metadata, tax_table, tidy_data_table, suffix):
    # """takes q2 formatted dataframes, a list of sample ids and a list of ASV names and removes samples and ASVs from dataframes, saves as both a .csv and as a .qza for qiime2"""
    ASV_table = q2.Artifact.load(feature_table)
    ASV_df = ASV_table.view(q2.Metadata).to_dataframe()

    tax_table = q2.Artifact.load(tax_table)
    tax_df = tax_table.view(q2.Metadata).to_dataframe()

    metadata_df = pd.read_csv(metadata, sep='\t')

    df = pd.read_csv(tidy_data_table)

    # create list of remaining sample ID's
    sampleids = list(df['sampleid'].unique())
    # create list of remaining ASVs
    ASVs = list(df['ASV'].unique())

    df_ASV1 = ASV_df[ASVs]
    df_ASV2 = df_ASV1.loc[sampleids]
    df_tax = tax_df.loc[ASVs]
    df_meta = metadata_df[(metadata_df['sampleid'].isin(sampleids))]

    print(
        (f'there are {df_ASV2.shape[0]} samples and {df_ASV2.shape[1]} ASVs remaining as per ASV table'))
    print(
        ('there are {} samples and {} ASVs remaining as per metadata').format((len(list(df_meta['sampleid'].unique()))),
                                                                              (len(list(df_ASV2.columns)))))
    print((f'there are {df_tax.shape[0]} AVSs remaing as per tax table'))

    table_artifact = q2.Artifact.import_data('FeatureTable[Frequency]', df_ASV2)
    table_artifact.save('ASV_{}.qza'.format(suffix))

    table_artifact = q2.Artifact.import_data('FeatureData[Taxonomy]', df_tax)
    table_artifact.save('tax_{}.qza'.format(suffix))

    print(f'saving ASV_{suffix}.csv')
    print(f'saving ASV_{suffix}.qza')
    print(f'saving tax_{suffix}.csv')
    print(f'saving tax_{suffix}.qza')
    print(f'saving meta_{suffix}.tsv')

    return df_ASV2.to_csv(f'ASV_{suffix}.csv'), df_tax.to_csv(f'tax_{suffix}.csv'), df_meta.to_csv(
        f'meta_{suffix}.tsv', index=False, sep='\t')