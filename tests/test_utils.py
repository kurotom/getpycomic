# -*- coding: utf-8 -*-
"""
"""
from getpycomic.utils import (
    parser_volumes,
    parser_chapter,
    normalize_number
)


import unittest


class TestNormalizeNumber(unittest.TestCase):

    def test_normalize_number(self) -> None:
        """
        """
        x = ["0.1", "1.1", "2.02", "2.00", "03.007", "10"]

        y = ["0.1", "1.1", "2.2", "2.0", "3.7", "10.0"]

        self.assertEqual([normalize_number(i) for i in x], y)



class TestCliFunctions(unittest.TestCase):

    def test_parser_volumes(self) -> None:
        """
        """
        vol = "1: [1, 4],2: [5, 9]"
        r = parser_volumes(string=vol)
        self.assertEqual(type(r), dict)

    def test_parser_volumes_empy(self) -> None:
        """
        """
        vol = None
        r = parser_volumes(string=vol)
        self.assertEqual(type(r), dict)
        self.assertEqual(len(r["matrix"]), 0)

    def test_parser_volumes_bad_values(self) -> None:
        """
        """
        vols = [
            "1: [1,],2: [9]",
            "",
            "0"
        ]
        r = [parser_volumes(string=i)["matrix"] for i in vols]
        self.assertTrue(all([i == {} for i in r]))

    def test_parser_chapter_n_chapters(self) -> None:
        """
        """
        ch = "5"
        r = parser_chapter(string=ch)
        self.assertIsInstance(r['n_chapters'], list)
        self.assertEqual(r['range'], None)
        self.assertEqual(r['update'], False)

    def test_parser_chapter_n_chapters_float_plus(self) -> None:
        """
        """
        ch = "5.1+"
        r = parser_chapter(string=ch)
        self.assertIsInstance(r['n_chapters'], list)
        self.assertEqual(r['range'], None)
        self.assertEqual(r['update'], True)

    def test_parser_chapter_chapter_plus(self) -> None:
        """
        """
        ch = "5+"
        r = parser_chapter(string=ch)
        self.assertIsInstance(r['n_chapters'], list)
        self.assertEqual(r['range'], None)
        self.assertEqual(r['update'], True)

    def test_parser_chapter_range(self) -> None:
        """
        """
        ch = "1-8"
        r = parser_chapter(string=ch)
        self.assertEqual(r['n_chapters'], None)
        self.assertIsInstance(r['range'], list)
        self.assertEqual(r['update'], False)

    def test_parser_chapter_all(self) -> None:
        """
        """
        ch = "all"
        r = parser_chapter(string=ch)
        self.assertEqual(r['n_chapters'], None)
        self.assertEqual(r['range'], None)
        self.assertEqual(r['update'], False)
