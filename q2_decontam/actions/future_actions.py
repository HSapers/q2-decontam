import qiime2 as q2
import pandas as pd


def update_tables(feature_table, metadata, tax_table, tidy_data_table, suffix):
    """
    takes q2 formatted dataframes, a list of sample ids and a list of asv
    names and removes samples and asvs from dataframes, saves as both a .csv
    and as a .qza for qiime2
    """
    asv_table = q2.Artifact.load(feature_table)
    asv_df = asv_table.view(q2.Metadata).to_dataframe()

    tax_table = q2.Artifact.load(tax_table)
    tax_df = tax_table.view(q2.Metadata).to_dataframe()

    metadata_df = pd.read_csv(metadata, sep='\t')

    df = pd.read_csv(tidy_data_table)

    # create list of remaining sample ID's
    sampleids = list(df['sampleid'].unique())
    # create list of remaining asvs
    asvs = list(df['asv'].unique())

    df_asv1 = asv_df[asvs]
    df_asv2 = df_asv1.loc[sampleids]
    df_tax = tax_df.loc[asvs]
    df_meta = metadata_df[(metadata_df['sampleid'].isin(sampleids))]

    number_samples = len(list(df_meta['sampleid'].unique()))
    number_features = len(list(df_asv2.columns))
    print(f'there are {df_asv2.shape[0]} samples and {df_asv2.shape[1]} '
          'asvs remaining as per asv table')
    print(f'there are {number_samples} samples and {number_features} asvs '
          'remaining as per metadata')
    print(f'there are {df_tax.shape[0]} AVSs remaing as per tax table')

    table_artifact = q2.Artifact.import_data('FeatureTable[Frequency]',
                                             df_asv2)
    table_artifact.save('asv_{}.qza'.format(suffix))

    table_artifact = q2.Artifact.import_data('FeatureData[Taxonomy]', df_tax)
    table_artifact.save('tax_{}.qza'.format(suffix))

    print(f'saving asv_{suffix}.csv')
    print(f'saving asv_{suffix}.qza')
    print(f'saving tax_{suffix}.csv')
    print(f'saving tax_{suffix}.qza')
    print(f'saving meta_{suffix}.tsv')

    return df_asv2.to_csv(f'asv_{suffix}.csv'), df_tax.to_csv(
        f'tax_{suffix}.csv'), df_meta.to_csv(
        f'meta_{suffix}.tsv', index=False, sep='\t')

# grouping sequence runs with extractions

# this function will remove all asvs that are only present in control 
# samples in the current sample extraction group for asvs that comprise at 
# least the current min relative abundance in each sample. Three files are 
# returned: a dataframe with the asvs removed, and a dataframe with the asvs
# unique to controls in one col and asvs in both controls and experimental 
# samples in the other col function to split tables - helper function used 
# internally - split into extraction batches and amplification batches from 
# metatdata derive the subsets  - need to define the sets of samples that we
# care about -one of the following -extraction set -amplification set 
# -sequencing set 1) define batch biom api - split down into subsets 2) 
# don't score any asv not present in at least 2 experimental samples -this 
# will remove asvs only in controls regardless of the number of control 
# wihthin a batch not being scored, just removed to decontam -creates a 
# sub-pop of asvs to score -inflate rel ab of contaminants we care about in 
# control samples, give them a higher score, allowing for a less sensitive 
# threshold within a batch asv needs to be in >2 samples  - ask if only 
# samples return 2 col matrix with asv id and sample id need new filter 
# function as well 


def remove_asvs_unique_to_controls(data, suffix):
    sequence_run_list = list(data['sequence_run'].unique())
    lol = []
    for run in sequence_run_list:
        ext_list = list((data[data['sequence_run'] == run])
                        ['extraction'].unique())
        lol.append(ext_list)
    extractions = dict(zip(sequence_run_list, lol))

    print('there are {} input asvs'.format(len(data['asv'].unique())))

    count = 1

    for k, v in extractions.items():
        count = count + 1
        extraction_group = k
        extraction = v

        df = data[(data['extraction'].isin(extraction))]
        asv_remove = []
        asv_experimental = []

        control_asv = list((df[
            df['sample_type'].str.contains('control') & 
            df['rel_abun'] > 0 & 
            (df['extraction'].isin(extraction))])['asv'].unique())
        Experimental_asv = list(
            (df[df['sample_type'].str.contains('experimental') & 
            (df['rel_abun'] > 0) & (
            df['extraction'].isin(extraction))])['asv'].unique())

        # asv_input = len(df['asv'].unique())

        for asv in control_asv:
            if asv in Experimental_asv:
                asv_experimental.append(asv)
            else:
                asv_remove.append(asv)

        asv_unique_to_controls_removed = df[~df['asv'].isin(asv_remove)]
        asv_remove = pd.DataFrame(asv_remove, columns=['asv'])
        asv_remove['source'] = f'unique to ext group {extraction_group}'

        # print(('there are {} asvs in input table and {} asvs in controls and 
        # {} asvs in Experimental').format(asv_input, (len(control_asv)), 
        # (len(Experimental_asv))))
        print(f'removed {len(asv_remove)} asvs from the experimental '
              'samples in extractions {extraction}')

        filename = 'asv_removed_{}'.format(extraction_group)
        filename2 = 'asv_control_ext_group_{}'.format(extraction_group)

        asv_unique_to_controls_removed.to_csv(
            ('{}.csv'.format(filename)), index=False)
        asv_remove.to_csv(('{}.csv'.format(filename2)), index=False)

    filenamelist = glob.glob('asv_removed*.csv')
    dataframes = [pd.read_csv(f) for f in filenamelist]
    controls_removed = pd.concat(dataframes)

    filenamelist2 = glob.glob('asv_control_ext_group_*.csv')
    dataframes2 = [pd.read_csv(f) for f in filenamelist2]
    asvs_removed = pd.concat(dataframes2)

    # re-calculate total reads and rel_abun
    # drop rel_abun col
    controls_removed.drop('rel_abun', axis=1, inplace=True) 
    controls_removed.drop('total_reads', axis=1, inplace=True)
    controls_removed['rel_abun'] = \
        controls_removed['reads'] / \
        controls_removed.groupby('sampleid')['reads'].transform('sum')
    controls_removed['total_reads'] = \
        (controls_removed.groupby(['sampleid'])['reads'].transform('sum'))

    controls_removed.to_csv(('master_{}.csv'.format(suffix)), index=False)
    asvs_removed.to_csv(('asv_unique_to_controls.csv'), index=False)

    # print(('{} asvs were removed in total').format(len(asvs_removed['asv'])))
    n_controls_removed = len(list(controls_removed['sampleid'].unique()))
    n_control_asvs_removed = (len(list(controls_removed['asv'].unique())))
    print(f'There are {n_controls_removed} samples '
          f'and {n_control_asvs_removed} asvs remaining')

    return print(
        f'master with asvs unique to controls removed '
        f'saved at master_{suffix}.csv, '
        f'table of asvs removed saved at asv_unique_to_controls.csv')

import biom
from ..format_types import FilterFormat
def filter_asv_singletons (table: biom.Table,
                           sample_metadata: q2.Metadata) -> FilterFormat:

    asv_df = table.to_dataframe()
    asv_df.reset_index(inplace=True)
    asv_df.rename(columns={"id": "sampleid", })

    meta_df=sample_metadata.to_dataframe()
    print(meta_df)
    # meta_df = pd.read_csv(sample_metadata, sep='\t')

    asv_df = pd.melt(asv_df, id_vars=['sampleid'],
                        var_name='asv', value_name='reads')
    asv_df['reads'].apply(pd.to_numeric, errors='coerce')
    asv_meta_df = asv_df.merge(meta_df, on='sampleid')
    temp_1_df = asv_meta_df[asv_meta_df['read'] > 0]

    asvs_remaining = \
        list(temp_1_df.groupby(['asv'])['reads'].transform('sum'))
    number_of_singletons = sum(float(num) == 1 for num in asvs_remaining)

    temp_1_df['asv_sums'] = \
        (temp_1_df.groupby(['asv'])['reads'].transform('sum'))
    asv_singleton_list = \
        (list((temp_1_df[(temp_1_df['asv_sums'] == 1)])['asv']))

    temp_2_df = temp_1_df[temp_1_df['asv_sums'] > 1]

    temp_2_df.drop(['asv_sums'], axis=1, inplace=True)

    filter_df = pd.DataFrame(asv_singleton_list, columns=['asv'])
    filter_df[filter]='singleton'

    print(('There are {} samples and {} asvs remaining').
          format((len(list(temp_2_df['sampleid'].unique()))),
          (len(list(temp_2_df['asv'].unique())))))
    print('{} singleton asvs were removed'.format(number_of_singletons))

    # return pd.Series(asv_singleton_list)
    return filter_df.to_csv(index=False, sep='/t')
