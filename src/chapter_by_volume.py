# -*- coding: utf-8 -*-
# -*- codin: utf-8 -*-
"""
"""

from typing import (
        List,
        Union
    )

from src.models import (
        Comic,
        Chapter,
        Volume
    )


class ChapterClassifierByVolume:
    """
    """

    def __init__(self):
        """
        """
        self.volumes = {}
        self.chapters_in_volume = []
        self.chapters_wo_volume = {}

    def clear(self) -> None:
        """
        Clears attributes.
        """
        self.volumes = {}
        self.chapters_in_volume = []
        self.chapters_wo_volume = {}

    def __sequence_check(
        self,
        matrix: dict
    ) -> bool:
        """
        Check sequence of volumes given by user.

        Args
            matrix: dicctionary with volumes and chapters indicators.

        Returns
            bool: `True` or `False` if sequential or not.
        """
        seq_keys = list(matrix.keys())
        return seq_keys == [i for i in range(1, len(seq_keys) + 1)]

    def sorter(
        self,
        comicObj: Comic = None,
        chapters_by_volume: dict = None
    ) -> Union[dict, None]:
        """
        Sorts chapters by volume follow the indication given by user.

        In two formats:
            * chapters_by_volume={volume_int: "start-end"}
            * chapters_by_volume={volume_int: [star, end]}

        *volume_int* must be an integer.
        *start* and *end* must be integers or a string of an integer.

        If the volume is not indicated, all chapters will be stored in a single
        volume.
        If the volume is specified, but not the chapter indicators, the
        remaining chapters will be stored in a single volume.

        Args
            comicObj: `Comic` instance with chapters of comic.
            chapter_by_volume: dicctionary with order of volumes and chapters.

        Returns
            dict: dicctionary with volumes and chapters.
            None: if dicctionary given not is correct.
        """
        self.clear()
        # print(chapters_by_volume)
        # print(chapters_by_volume.values())

        if chapters_by_volume is None or len(chapters_by_volume) == 0:

            self.volumes[1] = Volume(
                                volume=1,
                                list_chapters=[i for i in comicObj.chapters]
                            )

            return self.volumes

        check = self.__sequence_check(matrix=chapters_by_volume)
        if check is False:
            return None

        try:
            for k, v in chapters_by_volume.items():
                if isinstance(v, str):
                    if v != "":
                        v = [int(x) for x in v.split("-")]
                    else:
                        v = []

                # PATH CHAPTERS OF COMIC ON DISC,
                # CAST DIRECTORIES NAMES TO FLOAT.
                if len(v) > 0:
                    for chapterObj in comicObj.chapters:

                        self.__chapter_to_volume(
                                    volume=k,
                                    chapter=chapterObj,
                                    start=float(v[0]),
                                    end=float(v[1])
                                )

                # IF volume is given but not chapters indicators is given.
                elif len(v) == 0:
                    if len(self.volumes) == 0:
                        volume_key = 1
                    else:
                        volume_key = list(self.volumes.keys())[-1] + 1

                    chapters_ = [
                                    i for i in comicObj.chapters
                                    if i.id not in self.chapters_in_volume
                                ]

                    self.volumes[volume_key] = Volume(
                                                    volume=volume_key,
                                                    list_chapters=chapters_
                                                )

                    self.chapters_in_volume += [
                                                i.id for i in comicObj.chapters
                                            ]
                    break

                else:
                    # ERROR: if volume is but only start chapters indicator
                    #        is given
                    msg = 'Must deliver numeric *start* and *end* indicator,\
                     in a list or text string (e.g. "1-2", [1-2]) or leave \
                     blank with an empty string or list or not indicate a \
                     volume.'
                    raise ValueError(msg)

            self.__chapters_wo_volume_and_chapter_indicator(comic=comicObj)

            return self.volumes

        except ValueError as e:
            print(e)
            self.clear()
            return None

    def __chapter_to_volume(
        self,
        volume: int,
        chapter: Chapter,
        start: float = None,
        end: float = None
    ) -> None:
        """
        """
        number_chapter = chapter.id

        if number_chapter not in self.chapters_in_volume:

            # if start <= number_chapter < end + 1:
            if start <= number_chapter <= end:
                # print('> ', volume, start, end, number_chapter)
                if volume not in self.volumes:
                    # self.volumes[volume] = [chapter]
                    self.volumes[volume] = Volume(
                                                    volume=volume,
                                                    list_chapters=[chapter]
                                                )

                else:
                    self.volumes[volume].list_chapters.append(chapter)

                self.chapters_in_volume.append(number_chapter)



    def __chapters_wo_volume_and_chapter_indicator(
        self,
        comic: Comic = None,
        volume: int = None
    ) -> None:
        """
        If volume is given but not chapters indicators is given.
        If some chapters are not in volumes, they are grouped in a single volume.

        Args:
            volume: integer, default is `None`.

        """
        if volume is not None:
            volume_key = volume
        else:
            if len(list(self.volumes.keys())) == 0:
                volume_key = 1
            else:
                volume_key = list(self.volumes.keys())[-1] + 1

        for id_, chapter in self.chapters_wo_volume.items():
            if id_ not in self.chapters_in_volume:
                # print(chapter)

                if volume not in self.volumes:
                    # self.volumes[volume] = [chapter]
                    self.volumes[volume_key] = Volume(
                                                    volume=volume_key,
                                                    list_chapters=[chapter]
                                                )

                else:
                    self.volumes[volume_key].list_chapters.append(chapter)

                # add to chapters_in_volume list
                self.chapters_in_volume.append(chapter.id)
                # remove of chapters_wo_volume dict
                self.chapters_wo_volume.pop(chapter.id)
