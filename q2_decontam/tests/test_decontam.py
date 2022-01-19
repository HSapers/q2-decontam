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


import qiime2
from qiime2.plugin.testing import TestPluginBase
from qiime2.plugin.util import transform

from q2_types.feature_table import BIOMV210Format
from q2_decontam.actions.decontam import _list_to_featuretablebatches

import numpy as np
import pandas as pd
import biom
import time

class TestsPreprocessing(TestPluginBase):

    package = 'q2_decontam.tests'

    def setUp(self):
        super().setUp()
        table = self.get_data_path('feature_table_test.biom')
        self.table = qiime2.Artifact.import_data(
            'FeatureTable[Frequency]', table)

        # test data:
        # amplification controls are never extracted
        # extraction controls are never controls for amplifications
        # amplification contaminants should appear in everything amplified
        # extraction contaminants should appear in everything extracted
        # amplification controls: sample3, sample6
        # extraction controls: sample2, sample5
        # amplification contaminant: ASV_4
        # extraction contaminant: ASV_5

        # this is what is in self.table
        self.feature_table = biom.Table(
            np.array([[100, 0, 0, 100, 0, 0], [0, 0, 0, 100, 0, 0],
                      [100, 0, 0, 0, 0, 0], [10, 10, 10, 10, 10, 10],
                      [10, 10, 0, 10, 10, 0]]),
                      ['ASV_1', 'ASV_2', 'ASV_3', 'ASV_4', 'ASV_5'],
                      ['sample1', 'sample2', 'sample3', 'sample4',
                       'sample5', 'sample6'])

        #self.feature_table_artifact = qiime2.Artifact(self.feature_table)

        self.meta_data = qiime2.Metadata(pd.DataFrame(
           {'sample_type': ['experimental', 'control', 'control',
                            'experimental', 'control', 'control'],
            'amplification_type': ['experimental', 'experimental', 'control',
                                   'experimental', 'experimental', 'control'],
            'extraction': ['1', '1', np.nan, '2', '2', np.nan],
            'amplification': ['1', '1', '1', '2', '2', '2']},
           index=pd.Index(['sample1', 'sample2', 'sample3', 'sample4',
                           'sample5', 'sample6'], name='sampleid')))

        self.extraction_1 = biom.Table(
            np.array([[100, 0], [0, 0], [100, 0], [10, 10], [10, 10]]),
                      ['ASV_1', 'ASV_2', 'ASV_3', 'ASV_4', 'ASV_5'],
                      ['sample1', 'sample2'])

        self.extraction_2 = biom.Table(
            np.array([[100, 0], [100, 0], [0, 0], [10, 10], [10, 10]]),
                      ['ASV_1', 'ASV_2', 'ASV_3', 'ASV_4', 'ASV_5'],
                      ['sample4', 'sample5'])

        self.amplification_1 = biom.Table(
            np.array([[100, 0, 0], [0, 0, 0], [100, 0, 0],
                      [10, 10, 10], [10, 10, 0]]),
                      ['ASV_1', 'ASV_2', 'ASV_3', 'ASV_4', 'ASV_5'],
                      ['sample1', 'sample2', 'sample3'])

        self.amplification_2 = biom.Table(
            np.array([[100, 0, 0], [100, 0, 0], [0, 0, 0],
                      [10, 10, 10], [10, 10, 0]]),
                      ['ASV_1', 'ASV_2', 'ASV_3', 'ASV_4', 'ASV_5'],
                      ['sample4','sample5', 'sample6'])

        self.split_batches = self.plugin.actions['split_batches']
        self.split_samples = self.plugin.actions['split_samples']
        self._list_to_featuretablebatches = \
            self.plugin.actions['_list_to_featuretablebatches']

    def test_smoke(self):
    # will only fail if setup doesn't work
        self.assertTrue(True)

    def test_split_batches_batch_types_categorical(self):
        # data must be categorical, only str
        md = qiime2.Metadata(pd.DataFrame(
           {'extraction': ['1', '1', np.nan, '2', '2', np.nan],
            'amplification': ['1', '1', '1', '2', '2', '2']},
           index=pd.Index(['sample1', 'sample2', 'sample3', 'sample4',
                           'sample5', 'sample6'], name='sampleid')))
        # returns a result that contains an artifact the ',' returns the
        # first thing in the result, the artifact itself
        actual, = self.split_batches(md, ['extraction', 'amplification'])
        print(actual.view(dict))
        # expected computed by hand
        expected = {'amplification_1': ['sample1', 'sample2', 'sample3'],
                    'amplification_2': ['sample4', 'sample5', 'sample6'],
                    'extraction_1': ['sample1', 'sample2'],
                    'extraction_2': ['sample4', 'sample5'],
                    'extraction_nan': []}

        self.assertDictEqual(actual.view(dict), expected)
        # TODO check semantic type of actual


    def test_split_batches_no_batch_types_categorical(self):
        # function only operated over index, no data cols supplied
        md = qiime2.Metadata(pd.DataFrame(index=pd.Index(
            ['sample1', 'sample2'], name='sampleid')))
        actual, = self.split_batches(md)
        expected = {'single_batch': ['sample1', 'sample2']}
        self.assertDictEqual(actual.view(dict), expected)


    def test_split_batches_batch_types_numerical(self):
        # data must be categorical, only str
        md = qiime2.Metadata(pd.DataFrame(
           {'extraction': [1, 1, np.nan, 2, 2, np.nan],
            'amplification': [1, 1, 1, 2, 2, 2]},
           index=pd.Index(['sample1', 'sample2', 'sample3', 'sample4',
                           'sample5', 'sample6'], name='sampleid')))
        # returns a result that contains an artifact the ',' returns the
        # first thing in the result, the artifact itself
        actual, = self.split_batches(md, ['extraction', 'amplification'])

        # expected computed by hand
        expected = {'amplification_1.0': ['sample1', 'sample2', 'sample3'],
                    'amplification_2.0': ['sample4', 'sample5', 'sample6'],
                    'extraction_1.0': ['sample1', 'sample2'],
                    'extraction_2.0': ['sample4', 'sample5'],
                    'extraction_nan': []}

        self.assertDictEqual(actual.view(dict), expected)
        # TODO check semantic type of actual


    def test_list_to_featuretablebatches(self):

        input_biom_tables = [self.extraction_1,
                             self.extraction_2,
                             self.amplification_1,
                             self.amplification_2]

        ft_list = \
            [transform(f, to_type=BIOMV210Format) for f in input_biom_tables]

        name_list = ['extraction_1', 'extraction_2',
                     'amplification_1', 'amplification_2']

        actual = _list_to_featuretablebatches(ft_list, name_list)
        actual = [(str(path), table) for path, table in
                  (actual.batches.iter_views(biom.Table))]

        tables = [transform(f, to_type = biom.Table) for f in ft_list]
        expected = [
            ('amplification_1.biom', tables[2]),
            ('amplification_2.biom', tables[3]),
            ('extraction_1.biom', tables[0]),
            ('extraction_2.biom', tables[1]),
        ]

        self.assertEqual(actual, expected)


    # def test_split_samples_single(self):
    #
    #     bt = ['amplification', 'extraction']
    #
    #     ft = qiime2.Artifact.import_data(
    #         'FeatureTable[Frequency]', self.feature_table)
    #
    #     # print(ft.view(pd.DataFrame))
    #
    #     actual, = self.split_samples(ft, self.meta_data, bt)
    #     # print(actual.type) FeatureTableBatches[frequency] holding FeatureTables
    #
    #     actual_batches_dir_fmt = (actual.view(actual.format))
    #     # print(type(actual_batches_dir_fmt))
    #     # 'q2_decontam.format_types.SampleBatchesDirFmt'
    #
    #     x = list(actual_batches_dir_fmt.batches.iter_views(biom.Table))
    #     # print(actual_batches_dir_fmt.batches)
    #     dfs = actual_batches_dir_fmt.batches.iter_views(pd.DataFrame)
    #     for df in dfs:
    #         print(df)
    #
    #     actual_batches_dir_fmt = [(str(path), table) for path, table in
    #               (x)]
    #     # print(f'actual_batches_dir_fmt {actual_batches_dir_fmt}')
    #
    #     list_of_files = ['batches/extraction_1.biom',
    #                      'batches/extraction_2.biom',
    #                      'batches/amplification_1.biom',
    #                      'batches/amplification_2.biom']
    #
    #     # turn each biom table into a DF
    #     # remove 'zero' cols
    #     # turn back into biom tables
    #
    #     ft_list = []
    #     for name in list_of_files:
    #         path = self.get_data_path(name)
    #         fmt = BIOMV210Format(path, mode='r')
    #         ft_list.append(fmt)
    #     tables = [transform(f, to_type=biom.Table) for f in ft_list]
    #
    #     exp_dfs = [transform(f, to_type=pd.DataFrame) for f in tables]
    #     print(exp_dfs,'&*%$#')
    #
    #     for df, e in zip(dfs, exp_dfs):
    #         print(df)
    #         print(e)
    #         print()
    #
    #     expected = [
    #         ('amplification_1.biom', tables[2]),
    #         ('amplification_2.biom', tables[3]),
    #         ('extraction_1.biom', tables[0]),
    #         ('extraction_2.biom', tables[1]),
    #     ]
    #     print(f'expected {expected}')
    #
    #     self.assertEqual(actual_batches_dir_fmt, expected)

    # def test_split_samples_single(self):
    #     #dict = {'amplification_1': ['sample1', 'sample2', 'sample3']}
    #     #yaml_d = yaml.safe_dump(dict, default_flow_style=False)
    #     batch_set_test = self.get_data_path('amp_1_test.yml')
    #     actual = self.split_samples(self.table, batch_set_test)
    #
    #     e_table = self.get_data_path('amplification_1.biom')
    #     expected = Artifact.import_data('FeatureTable[Frequency]',e_table)
    #
    #     self.assertEqual(actual.view(biom.Table), expected.view(biom.Table))




 # emtpy metadata - should be handled by q2
 # test empty batch type will evaluate to colname_nan
 # assert raises - when I do this things after
 #   with assert raises regex - check message  - correct value error for #2
