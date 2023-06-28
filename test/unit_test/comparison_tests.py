import os
import unittest
import csv
from unittest.mock import patch
from src import detector as pd


class MainMethodTest(unittest.TestCase):
    def assertCsvFilesEqual(self, csv_file_path1, csv_file_path2):
        if csv_file_path1 is None or csv_file_path2 is None:
            self.fail("One of the CSV file paths is None.")

        with open(csv_file_path1, 'r') as file1, open(csv_file_path2, 'r') as file2:
            reader1 = csv.reader(file1)
            reader2 = csv.reader(file2)
            for row1, row2 in zip(reader1, reader2):
                self.assertListEqual(row1, row2)

    def test_main_method_1(self):
        file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository1/main.yml'

        expected_csv_file = './src/output/expected_main.yml_smells_v1.csv'
        actual_output = pd.main_method(file_path)

        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_2(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository1/setup-Archlinux.yml'
        expected_csv_file = 'path/to/expected_2.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_3(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository1/setup-Debian.yml'
        expected_csv_file = 'path/to/expected_3.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_4(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository1/setup-Debian.yml'
        expected_csv_file = 'path/to/expected_4.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_5(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository1/setup-FreeBSD.yml'
        expected_csv_file = 'path/to/expected_5.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_6(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository1/setup-FreeBSD.yml'
        expected_csv_file = 'path/to/expected_6.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_7(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository1/setup-OpenBSD.yml'
        expected_csv_file = 'path/to/expected_7.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_8(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository1/setup-RedHat.yml'
        expected_csv_file = 'path/to/expected_8.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_9(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository1/setup-Ubuntu.yml'
        expected_csv_file = 'path/to/expected_9.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_10(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository1/vhosts.yml'
        expected_csv_file = 'path/to/expected_10.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_11(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/install_and_configure.yml'
        expected_csv_file = 'path/to/expected_11.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_12(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository2/assert.yml'
        expected_csv_file = 'path/to/expected_12.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_13(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository2/converge.yml'
        expected_csv_file = 'path/to/expected_13.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_14(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository2/main.yml'
        expected_csv_file = 'path/to/expected_14.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_15(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository2/prepare.yml'
        expected_csv_file = 'path/to/expected_15.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_16(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository2/verify.yml'
        expected_csv_file = 'path/to/expected_16.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_17(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository3/prepare.yml'
        expected_csv_file = 'path/to/expected_17.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_18(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository3/verify.yml'
        expected_csv_file = 'path/to/expected_18.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_19(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository2/main2.yml'
        expected_csv_file = 'path/to/expected_19.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)

    def test_main_method_20(self):
        csv_file_path = '/home/ghazal/prengdl-reproduce/testScripts/Repository3/verify2.yml'
        expected_csv_file = 'path/to/expected_20.csv'
        actual_output = pd.main_method(csv_file_path)
        self.assertCsvFilesEqual(actual_output, expected_csv_file)


if __name__ == '__main__':
    unittest.main()
