import os
import unittest
from unittest.mock import patch
from Src import parser as pd


class MainMethodTest(unittest.TestCase):

    @patch('builtins.input', side_effect=['../testScripts/Repository1/main.yml'])
    def test_main_method_1(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository1/setup-Archlinux.yml'])
    def test_main_method_2(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository1/setup-Debian.yml'])
    def test_main_method_3(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository1/setup-Debian.yml'])
    def test_main_method_4(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository1/setup-FreeBSD.yml'])
    def test_main_method_5(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository1/setup-FreeBSD.yml'])
    def test_main_method_6(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository1/setup-OpenBSD.yml'])
    def test_main_method_7(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository1/setup-RedHat.yml'])
    def test_main_method_8(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository1/setup-Ubuntu.yml'])
    def test_main_method_9(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository1/vhosts.yml'])
    def test_main_method_10(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/install_and_configure.yml'])
    def test_main_method_11(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository2/assert.yml'])
    def test_main_method_12(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository2/converge.yml'])
    def test_main_method_13(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository2/main.yml'])
    def test_main_method_14(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository2/prepare.yml'])
    def test_main_method_15(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository2/verify.yml'])
    def test_main_method_16(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository3/prepare.yml'])
    def test_main_method_17(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository3/verify.yml'])
    def test_main_method_18(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository2/main2.yml'])
    def test_main_method_19(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository3/req.yml'])
    def test_main_method_20(self, mock_input):
        actual_output = pd.main_method()

    @patch('builtins.input', side_effect=['../testScripts/Repository3/assert.yml'])
    def test_main_method_21(self, mock_input):
        actual_output = pd.main_method()


if __name__ == '__main__':
    unittest.main()
