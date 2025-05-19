# -*- coding: utf-8 -*-
"""
"""

from src.utils import normalize_number

import unittest


class TestNormalizeNumber(unittest.TestCase):

    def test_normalize_number(self) -> None:
        """
        """
        x = ["0.1", "1.1", "2.02", "2.00", "03.007", "10"]

        y = ["0.1", "1.1", "2.2", "2.0", "3.7", "10.0"]

        self.assertEqual([normalize_number(i) for i in x], y)
