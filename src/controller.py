# -*- coding: utf-8 -*-
"""

"""

from src.models import (
        Comic,
        Chapter,
        ImageChapter
    )

# from src.imagehandler import ImagesHandler
from src.ziphandler import ZipHandler
from src.chapter_by_volume import ChapterClassifierByVolume
from src.requests_data import RequestsData
from src.pathclass import PathClass
from src.status import Status

from src.downloader import Downloader

from src.errorhandlerdecorator import register_error

# ENGINES
from src.engines import (
    Selenium,

)
#

#
from src.pages import (
    TmoManga,
    ZonaTmo
)
#

from time import sleep
from math import ceil

from typing import (
        List,
        Union,
        Literal,
    )

FilterTypes = Literal["id", "xpath", "tag_name", "css_selector"]


Supported_Webs = {
    "tmomanga": TmoManga,
    "zonatmo": ZonaTmo
}


class GetPyComic:
    """
    """

    DIRECTORY = "GetPyComic"

    def __init__(
        self,
        web: Literal["tmomanga", "zonatmo"] = "tmomanga",
        engine: Literal["selenium", "playwright"] = "selenium",
        show: bool = True,
        setup: bool = True
    ) -> None:
        """
        """
        self.scraper = None

        self.current_comic = None  # `Comic` instance

        self.show = show  # show gui scraper
        self.setup = setup  # setup scraper

        self.parent_path = PathClass.dirname(path=__file__)
        # print('--> ', self.parent_path)

        # Selenium
        self.geckodriver_path = PathClass.join(
                                            self.parent_path,
                                            "drivers",
                                            "geckodriver"
                                        )

        self.status = Status(
                            controller=self,
                            base_path=self.parent_path
                        )

        self.DIRECTORY_GETPYCOMIC = ""

        self.web_site = None

        self.set_base_dir()

        self.select_web(web)


        # resume work in case of error.
        # self.check_error_resume_work()

        if setup:
            self.change_engine(engine)

    def close_scraper(self) -> None:
        """
        """
        if self.scraper is not None:
            self.scraper.close()

    def select_web(
        self,
        web: str
    ) -> None:
        """
        """
        try:
            self.web_site = Supported_Webs[web]
        except KeyError as e:
            self.web_site = Supported_Webs["tmomanga"]

    def change_engine(
        self,
        engine: Literal["selenium", "playwright"]
    ) -> None:
        """
        """
        if self.scraper is not None:
            self.close_scraper()

        if engine == "selenium":
            current_scraper = Selenium(
                                    geckodriver=self.geckodriver_path,
                                    show=self.show,
                                    setup=self.setup,
                                    status=self.status,
                                )
        elif engine == "playwright":
            current_scraper = None

        self.scraper = current_scraper

        print("current scraper ", self.scraper)

    def set_base_dir(
        self,
        path: str = None
    ) -> None:
        """
        """
        if path is None:
            new_base = PathClass.join(
                                    PathClass.get_home,
                                    GetPyComic.DIRECTORY
                                )
        else:
            new_base = PathClass.join(
                                    PathClass.get_home,
                                    path
                                )
        self.DIRECTORY_GETPYCOMIC = new_base
#
#  scraper
#
    # @register_error("search")
    def search(
        self,
        search: str
    ) -> list:
        """
        """
        print("search: ", self.web_site)

        if self.scraper is not None:

            results = self.scraper.search(
                    string=search,
                    webclass=self.web_site,
                )

            return results

    # @register_error("get_chapters")
    def get_chapters(
        self,
        comic: Comic,
        n_chapters: int = None,
        range: List[int] = None,
    ) -> Comic:
        """
        """
        if self.scraper is not None:

            self.current_comic = comic

            self.scraper.get_chapters(
                                comic=comic,
                                webclass=self.web_site,
                                n_chapters=n_chapters,
                                range=range,
                            )
            return comic

    # @register_error("get_images_chapter")
    def get_images_chapter(
        self,
        comic: Comic = None,
    ) -> Comic:
        """
        """
        print("get_images ", self.scraper)
        if self.scraper is not None:

            if comic is None:
                comic = self.current_comic

            for ch in comic.chapters:
                self.scraper.get_images(
                                    chapter=ch,
                                    webclass=self.web_site,
                                )
            return comic
#
#  scraper
#
    @property
    def get_current_comic(self) -> list:
        """
        """
        return self.current_comic
#
#
#
    def save_comic(
        self,
        comicObj: Comic = None,
        n_threads: int = 4,
    ) -> None:
        """
        """
        if comicObj is None:
            comicObj = self.current_comic

        comic_path = PathClass.join(
                                    PathClass.get_desktop(),
                                    GetPyComic.DIRECTORY,
                                    comicObj.name
                                )

        comicObj.path = comic_path

        PathClass.makedirs(path=comic_path)

        for chapter in comicObj.chapters:

            chapter_dir = PathClass.join(
                                        comic_path,
                                        chapter.name
                                        )

            PathClass.makedirs(path=chapter_dir)

            chapter.path = chapter_dir

            n_images = len(chapter.images)


            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

            if self.web_site.base[-1] != "/":
                refer_site = self.web_site.base + "/"
            else:
                refer_site = self.web_site.base

            header_request = {
                "Referer": refer_site,  # avoid hotlinking
                'User-Agent': user_agent,
            }


            if n_images < 10:
                downloader_thread = Downloader(
                                            list_images=chapter.images,
                                            chapter_path=chapter.path,
                                            header=header_request,
                                            daemon=True
                                        )

                downloader_thread.start()
                downloader_thread.join()

            else:
                threads_list = []
                n_chunk_images = ceil(n_images / n_threads)

                for i in range(0, n_images, n_chunk_images):
                    chunk_images = chapter.images[i: i + n_chunk_images]

                    downloader_thread = Downloader(
                                                list_images=chunk_images,
                                                chapter_path=chapter.path,
                                                header=header_request,
                                                daemon=True
                                            )

                    threads_list.append(downloader_thread)
                    downloader_thread.start()


                for th in threads_list:
                    th.join()

    def sorter_chapters_by_volumes(
        self,
        chapters_by_volume: dict,
        comic: Comic = None,
    ) -> Union[dict, None]:
        """
        Sorter chapters downloaded into volumes using a diccionaries of digits,
        these values indicate the chapters to be stored in volumes.

        To determine the volume is a single digit (`int`), to determine the
        chapters a string of digits separated by a hyphen or a list of digits
        (`int`) can be used.

        If you do not give one, by default all chapters are merged into one
        volume.

        Chapter information by volume can be obtained at `https://comick.io/`.

        Examples:

            # Single Comic
            sorter_chapters_by_volumes(
                chapters_by_volume={1: [1, 2], 2: [3, 5]}
            )

            sorter_chapters_by_volumes(
                chapters_by_volume={1: "1-2", 2: "3-5"}
            )

        Args
            chapters_by_volume: dictionary for one comic book. The number of
                                elements must be exactly the same.
            comic: instance of `Comic`, if not given, the current instance of
                   `Comic` will be used.

        Returns
            dict: returns a dicctionary with volume number as key and `Volume`
                  insance as value.
        """
        if comic is None:
            comic = self.current_comic


        ch_vl = ChapterClassifierByVolume()

        if isinstance(chapters_by_volume, dict):
            chapters_sorter = ch_vl.sorter(
                        comicObj=comic,
                        chapters_by_volume=chapters_by_volume
                    )

            # print('#### > ', chapters_sorter)

            comic.volumes = chapters_sorter
            self.current_comic = comic

            return comic


    def to_cbz(
        self,
        comic: Comic = None,
        preserve_images: bool = True
    ) -> None:
        """
        Convert to CBZ file.
        """
        if comic is None:
            comic = self.current_comic
        # print(comic.name)
        # print(comic.link)
        # print(comic.chapters)
        # print(comic.path)
        # print(comic.volumes)

        if comic.volumes is None:
            return

        for volume, volumechapterObj in comic.volumes.items():

            # print(f"{volume}".zfill(3), [i.path for i in chapters])

            cbz_name = "%s - %s (%s).cbz" % (
                comic.name.title(),
                f"{volume}".zfill(3),
                volumechapterObj.get_range_chapters()
            )

            path_cbz = PathClass.join(
                                    comic.path,
                                    cbz_name
                                )

            print(">> ", path_cbz)

            ZipHandler.to_zip(
                    cbz_path=path_cbz,
                    list_chapters=volumechapterObj.list_chapters
                )

            if preserve_images is False:
                self.delete_images(list_chapters=volumechapterObj.list_chapters)

    def delete_images(
        self,
        list_chapters: List[Chapter]
    ) -> None:
        """
        """
        for chapter in list_chapters:
            # print('--> ', PathClass.absolute_path(path=chapter.path))
            PathClass.delete(
                    path=PathClass.absolute_path(path=chapter.path)
                )


    def to_json(self) -> None:
        """
        """
        print("to_json")
        self.status.to_json()

    def to_load(self) -> None:
        """
        """
        self.status.to_load()
