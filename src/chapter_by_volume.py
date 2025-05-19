# -*- coding: utf-8 -*-
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


class VolumesSorter:
    """
    """
    CHAPTERS_BY_VOLUME = 6

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
        Checks the sequence of volumes and chapter ranges indicated by the user.

        Args
            matrix: dicctionary with volumes and chapters indicators.

        Returns
            bool: `True` or `False` if sequential or not.
        """
        # checks if keys is a int.
        if all([isinstance(i, int) for i in matrix.keys()]) is False:
            return False

        # checks if `keys` is a sequence
        seq_keys = list(matrix.keys())
        # print(seq_keys)
        if seq_keys != [i for i in range(1, len(seq_keys) + 1)]:
            return False

        # checks if `values` is a sequence
        seq_values = [
                    int(x) for i in matrix.values()
                    if i != ""
                    for x in (i.split("-")
                         if isinstance(i, str) else i
                     )
                ]

        seq_values = []
        for val in matrix.values():
            if not val:
                continue
            if isinstance(val, str):
                values = val.split("-")
            if isinstance(val, (list)):
                values = val
            seq_values.extend(int(i) for i in values)

        if sorted(seq_values) != seq_values:
            return False

        return True

    def sorter(
        self,
        comicObj: Comic = None,
        chapters_by_volume: dict = None
    ) -> dict:
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

        # print(comicObj, chapters_by_volume)
        if comicObj is None or isinstance(comicObj, Comic) is False:
            return {}

        # if chapters_by_volume is None, each volume has 6 chapters
        if chapters_by_volume is None or len(chapters_by_volume) == 0:
            chapters_by_volume = {}
            volume_ = 1
            n_chaps = len(comicObj.chapters)
            for i in range(0, n_chaps, VolumesSorter.CHAPTERS_BY_VOLUME):
                chunk = comicObj.chapters[0 + i: VolumesSorter.CHAPTERS_BY_VOLUME + i]
                chap_ids = [i.id for i in chunk]
                chapters_by_volume[volume_] = [min(chap_ids), max(chap_ids)]
                volume_ += 1

        check = self.__sequence_check(matrix=chapters_by_volume)
        # print(">> ", check, chapters_by_volume)
        if check is False:
            return {}

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
                    # ERROR:
                    #   if the volume is specified but only the chapter start
                    #   indicator is specified.
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
        # print(volume, chapter, start, end)
        number_chapter = chapter.id

        if number_chapter not in self.chapters_in_volume:

            if start <= number_chapter <= end:
                # print('> ', volume, start, end, number_chapter)
                if volume not in self.volumes:
                    self.volumes[volume] = Volume(
                                                volume=volume,
                                                list_chapters=[]
                                            )
                    self.volumes[volume].add(chapter)
                else:
                    self.volumes[volume].add(chapter)

                self.chapters_in_volume.append(number_chapter)


    def __chapters_wo_volume_and_chapter_indicator(
        self,
        comic: Comic = None,
        volume: int = None
    ) -> None:
        """
        If volume is given but not chapters indicators is given.
        If some chapters are not in volumes, they are grouped in a single
        volume.

        Args
            comic: `Comic` instance.
            volume: integer, number of volume.

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

                # add to `chapters_in_volume` list
                self.chapters_in_volume.append(chapter.id)
                # remove of `chapters_wo_volume` dict
                self.chapters_wo_volume.pop(chapter.id)
