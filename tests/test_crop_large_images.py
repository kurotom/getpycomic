# -*- coding: utf-8 -*-
"""
"""

from getpycomic.imagehandler import ImagesHandler


from PIL import Image
import unittest
import io


class TestSeleniumClass(unittest.TestCase):

    def setUp(self):
        """
        """
        self.data = io.BytesIO()
        img = Image.new("RGB", (900,6000), (255,255,255))
        img.save(self.data, format="JPEG")
        self.chunks = ImagesHandler.crop(data=self.data, sizeImage="medium")

    def test_crop_large_images(self):
        """
        """
        self.assertEqual(4, len(self.chunks))

    def test_format_size(self):
        for chunk in self.chunks:
            im = Image.open(chunk)
            self.assertEqual(im.format, "JPEG")

    def test_format(self):
        for chunk in self.chunks:
            im = Image.open(chunk)
            self.assertEqual(im.format, "JPEG")
