# -*- coding: utf-8 -*-
"""
"""

from threading import Thread

from time import sleep


from typing import TypeVar

Selenium = TypeVar("Selenium")
Comic = TypeVar("Comic")
Queue = TypeVar("Queue")


class ThreadSelenium(Thread):

    def __init__(
        self,
        scraper: Selenium,
        comicObj: Comic,
        cookies: dict,
        webclass: object,
        container_queue: Queue,
        chunk_chapters: list,
        daemon: bool = True
    ) -> None:
        """
        """
        super().__init__(daemon=daemon)
        self.scraper = scraper
        self.comicObj = comicObj
        self.cookies = cookies
        self.webclass = webclass

        self.container_queue = container_queue
        self.chunk_chapters = chunk_chapters


    def run(self) -> None:
        """
        """
        print(">>>> ", self)
        print(self.scraper.driver)

        # init setup
        self.scraper.setup()

        # load base web
        self.scraper.driver.get(self.webclass.base)
        sleep(0.5)

        # copy cookies to new scraper
        for cookie in self.cookies:
            self.scraper.driver.add_cookie(cookie)

        # reload driver
        self.scraper.driver.refresh()

        chapters = self.scraper.iterate_get_chapter_images(
                                        comicObj=self.comicObj,
                                        webclass=self.webclass,
                                        list_chapters=self.chunk_chapters,
                                        is_thread=True,
                                        # cookies=self.cookies,
                                    )

        # close current driver in thread
        self.scraper.close()

        # puts `Chapter` instance on queue
        for chapter in chapters:
            self.container_queue.put(chapter)
