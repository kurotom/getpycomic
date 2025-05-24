# -*- coding: utf-8 -*-
"""
"""

from src.imagehandler import ImagesHandler
from src.requests_data import RequestsData
from src.pathclass import PathClass

from threading import Thread


class Downloader(Thread):

    def __init__(
        self,
        chunk_chapters: list,
        header: dict,
        daemon: bool = True,
    ) -> None:
        """
        """
        Thread.__init__(self, daemon=daemon)
        self.imagehandler = ImagesHandler()
        self.chunk_chapters = chunk_chapters
        self.header = header

    def run(self) -> None:
        """
        Gets the images from the URL and saves them.
        """
        print(self)
        for chapter in self.chunk_chapters:

            for image in chapter.images:
                # image.id
                # image.name
                # image.extention
                # image.link
                # print(image.name, image.extention)

                image.extention = '.jpg'

                image_path_ = PathClass.join(
                                            chapter.path,
                                            image.get_name()
                                        )
                image.path = image_path_

                if PathClass.exists(image_path_) is False:

                    # get image data from url
                    data = RequestsData.request_data(
                            header=self.header,
                            link=image.link
                        )

                    if data is not None:
                        new_image_data_ = self.imagehandler.new_image(
                                                            currentImage=data,
                                                            extention="jpeg",
                                                            sizeImage='small'
                                                        )

                        self.imagehandler.save_image(
                                                path_image=image.path,
                                                image=new_image_data_
                                            )
