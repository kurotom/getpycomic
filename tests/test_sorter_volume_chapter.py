# -*- coding: utf-8 -*-
"""
"""

from src.sorter_volume_chapter import VolumesSorter
from src.models import (
        Comic,
        Chapter,
        ImageChapter
    )

import unittest


class TestVolumesSorter(unittest.TestCase):

    def setUp(self):
        """
        """
        items = [
            [1.00, "A", "A.com"],
            [2.00, "B", "B.com"],
            [3.00, "C", "C.com"],
        ]


        self.comic = Comic(
                    name="Comic",
                    link="comic.com",
                    chapters=[Chapter(id=i[0],name=i[1],link=i[2]) for i in items],
                )

        self.classifier = VolumesSorter()

    def test_sort_strings_ranges(self):
        """
        """
        r = self.classifier.sorter(
            comicObj=self.comic,
            volumes_dict_chapters={
                1: "1-2",
                2: "3-4",
                3: "5-6",
                4: ""
            }
        )
        self.assertIsInstance(r, dict)
        self.assertEqual([i.n_chapters for i in r.values()], [2, 1, 0])
        self.assertEqual(
                    [[i.name for i in v.list_chapters] for k, v in r.items()],
                    [["A", "B"], ["C"], []]
                )

    def test_sort_ints_ranges(self):
        """
        """
        r = self.classifier.sorter(
            comicObj=self.comic,
            volumes_dict_chapters={
                1: [1,2],
                2: [3,4],
                3: [5,6],
                4: []
            }
        )
        self.assertIsInstance(r, dict)
        self.assertEqual([i.n_chapters for i in r.values()], [2, 1, 0])
        self.assertEqual(
                    [[i.name for i in v.list_chapters] for k, v in r.items()],
                    [["A", "B"], ["C"], []]
                )

    def test_sort_not_correct_ranges_string_ints(self):
        """
        """
        r1 = self.classifier.sorter(
            comicObj=self.comic,
            volumes_dict_chapters={
                1: [1, 2],
                2: [2, 3],
                3: [3, 4]
            }
        )

        r2 = self.classifier.sorter(
            comicObj=self.comic,
            volumes_dict_chapters={
                1: "1-2",
                2: "2-3",
                3: "3-4"
            }
        )

        self.assertIsInstance(r2, dict)
        self.assertEqual([i.n_chapters for i in r2.values()], [2, 1])
        self.assertEqual(
                    [[i.name for i in v.list_chapters] for k, v in r1.items()],
                    [["A", "B"], ["C"]]
                )
        self.assertEqual(
                    [[i.name for i in v.list_chapters] for k, v in r2.items()],
                    [["A", "B"], ["C"]]
                )


    def test_sort_not_sequentially_volumes(self):
        """
        """
        r = self.classifier.sorter(
            comicObj=self.comic,
            volumes_dict_chapters={
                1: "1-2",
                3: "3-4"
            }
        )
        self.assertEqual(r, {})

    def test_sort_not_sequentially_chapters(self):
        """
        """
        r = self.classifier.sorter(
            comicObj=self.comic,
            volumes_dict_chapters={
                1: "1-2",
                2: "4-3"
            }
        )
        self.assertEqual(r, {})

    def test_sort_empty(self):
        """
        """
        r = self.classifier.sorter()
        self.assertEqual(r, {})


    def test_sort_chapters_by_volume_custom_value(self):
        """
        """
        r = self.classifier.sorter(
            comicObj=self.comic,
            volumes_dict_chapters=None,
            chapters_by_volume=1
        )
        self.assertIsInstance(r, dict)
        self.assertEqual([i.n_chapters for i in r.values()], [1] * 3)

    def test_sort_chapters_by_volume_default_value(self):
        """
        """
        r = self.classifier.sorter(
            comicObj=self.comic,
            volumes_dict_chapters=None,
            chapters_by_volume=None
        )
        self.assertIsInstance(r, dict)
        self.assertEqual([i.n_chapters for i in r.values()], [3])
