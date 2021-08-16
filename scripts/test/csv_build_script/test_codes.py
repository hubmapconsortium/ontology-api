import unittest
from unittest.mock import patch

import pandas as pd
from scripts.csv_build_script.codes import Codes


class TestCodes(unittest.TestCase):

    @patch('scripts.csv_build_script.codes.pd.read_csv')
    def setUp(self, mock_read_csv):
        def resp1(filename: str) -> None:
            d = {
                'CodeID:ID': [
                    "MTHSPL J7A92W69L7", "NCI C76777", "ATC N07XX07"
            ], 'SAB': [
                    "MTHSPL", "NCI", "ATC"
            ],
                'CODE': [
                    "J7A92W69L7", "C76777", "N07XX07"
                ]
            }
            return pd.DataFrame(data=d)
        filename = 'Dummy.csv'
        mock_read_csv.side_effect = [resp1(filename)]
        self.codes = Codes(filename)

    def test_find_codeid_value_exists(self):
        result = self.codes.find_codeid('ATC N07XX07')
        self.assertTrue(result)

    def test_find_codeid_value_does_not_exist(self):
        result = self.codes.find_codeid('NOT THERE')
        self.assertFalse(result)
