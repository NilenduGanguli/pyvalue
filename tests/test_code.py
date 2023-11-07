import unittest
from io import StringIO
from unittest.mock import patch
from analyze_code import analyze_code

class TestCodeAnalysis(unittest.TestCase):
    def test_analyze_code_unused_variable(self):
        code = """
        unused_var = 42
        def some_function():
            unused_var = 10
            print(unused_var)
        """
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.readlines.return_value = code.split('\n')
            result = analyze_code('test.py')
            self.assertEqual(result['unused_variable'], ['unused_var'])

    def test_analyze_code_unused_import(self):
        code = """
        import unused_module
        from some_module import unused_function
        """
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.readlines.return_value = code.split('\n')
            result = analyze_code('test.py')
            self.assertEqual(result['unused_import'], ['unused_module', 'unused_function'])

    def test_analyze_code_unused_argument(self):
        code = """
        def some_function(unused_arg):
            pass
        def another_function():
            pass
        """
        with patch('subprocess.Popen') as mock_popen, \
             patch('subprocess.Popen.communicate') as mock_communicate:
            mock_communicate.return_value = (b"Unused argument: unused_arg", b"")
            result = analyze_code('test.py')
            self.assertEqual(result['unused_argument'], ['some_function=>unused_arg'])

if __name__ == '__main__':
    unittest.main()
