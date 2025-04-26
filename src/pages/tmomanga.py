# -*- coding: utf-8 -*-
"""
"""

from src.pages.base import BaseMeta


class TmoManga(metaclass=BaseMeta):

    base = "https://tmomanga.com"
    search_url = base + "/biblioteca?search=NONE&page=1"

# search
    # search_button = ".open-search-main-menu"  # css selector
    # input_search = "#blog-post-search > input:nth-child(1)"  # css selector
#

# list of comic matches in search
    content_page_divs_css = ".row-eq-height"  # css selector

    items_comic_css = "div.col-xl-3:nth-child(n)"  # css selector
    info_comic_css = ".h5 > a"  # css selector

    # pagination = ".pagination"  # css selector
#


# comic page section
    # title_comic = ".post-title > h1:nth-child(2)"  # css selector
    chapters_content_ul_class = [
        ".sub-chap",  # class selector

    ]

    chapter_css = [
        "li.wp-manga-chapter:nth-child(n)",  # class selector

    ]

    chaper_name_class = "a:nth-child(1)"  # class selector
    chapter_link_class = None  # class selector
#

# into chapter page
    # content_images_comic_css = ".reading-content"  # css selector
    container_images_div_css = "#images_chapter"  # css selector
#
