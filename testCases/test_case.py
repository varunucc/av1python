from unittest import TestCase
from example_code import mul


class testing_cases(TestCase):

    def test_mul(self):
        self.assertEqual(mul(2, 3), 6)
