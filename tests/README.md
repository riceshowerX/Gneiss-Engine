# Gneiss-Engine Tests

This directory contains unit tests for the Gneiss-Engine library.

## Running Tests

To run all tests, use the following command from the project root directory:

```bash
python -m unittest discover tests
```

To run a specific test file:

```bash
python -m unittest tests/test_image.py
```

To run a specific test case:

```bash
python -m unittest tests.test_image.TestImage
```

To run a specific test method:

```bash
python -m unittest tests.test_image.TestImage.test_resize
```

## Test Coverage

To generate a test coverage report, you'll need to install the `pytest` and `pytest-cov` packages:

```bash
pip install pytest pytest-cov
```

Then run:

```bash
pytest --cov=gneiss tests/
```

For a more detailed HTML report:

```bash
pytest --cov=gneiss --cov-report=html tests/
```

This will create a `htmlcov` directory with an HTML coverage report.

## Adding New Tests

When adding new tests:

1. Create a new test file in the `tests` directory with a name that starts with `test_`.
2. Create a test class that inherits from `unittest.TestCase`.
3. Add test methods that start with `test_`.
4. Use assertions to verify that your code behaves as expected.

Example:

```python
import unittest
from gneiss import Image

class TestNewFeature(unittest.TestCase):
    def test_new_feature(self):
        # Test code here
        img = Image("path/to/test/image.jpg")
        result = img.new_feature()
        self.assertEqual(result, expected_value)