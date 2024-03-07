import unittest

# Automatically discover and load all test modules in the current directory
test_suite = unittest.defaultTestLoader.discover(start_dir='.', pattern='test_*.py')

# Run the test suite
test_runner = unittest.TextTestRunner()
test_runner.run(test_suite)
