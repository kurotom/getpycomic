# -*- coding: utf-8 -*-
"""
Handler related to files ZIP.
"""

import zipfile

import os

from typing import List

from src.models import (
        Chapter
    )


class ZipHandler:
    """
    """

    def to_zip(
        cbz_path: str,
        list_chapters: List[Chapter]
    ) -> None:
        """
        """

        if not cbz_path.endswith('.cbz'):
            cbz_path = cbz_path + '.cbz'

        # print(cbz_path)
        # print(list_chapters[0], list_chapters[-1])
        # print([i.name for i in list_chapters])

        with zipfile.ZipFile(
                file=cbz_path, mode='w',
                compression=zipfile.ZIP_DEFLATED,
                allowZip64=False
        ) as zip_file:

            for chapter in list_chapters:
                for images in chapter.images:
                    # print(images.path)
                    zip_file.write(images.path)
