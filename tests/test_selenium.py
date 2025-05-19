# -*- coding: utf-8 -*-
"""
I wrote these tests with the help of AI because I have never written this kind
of tests.
"""
import unittest
from unittest.mock import (
                        patch,
                        MagicMock
                    )

from src.models import (
                        Comic,
                        Chapter,
                        ImageChapter
                    )
from src.engines.selenium import Selenium
from src.status import Status

from selenium.webdriver.common.by import By


class TestSeleniumClass(unittest.TestCase):
    @patch('src.selenium.webdriver.Firefox')
    @patch('src.selenium.Service')
    def test_setup_initializes_driver(self, mock_service, mock_firefox):
        # Preparar mocks
        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver

        scraper = Selenium(
                            geckodriver="fake/path/geckodriver",
                            setup=True
                        )

        # Ensure that webdriver. Firefox is called and that self.driver is set.
        mock_firefox.assert_called_once()
        self.assertIsNotNone(scraper.driver)

        # Verify that detection avoidance scripts are executed.
        mock_driver.execute_script.assert_called()

    @patch('src.selenium.webdriver.Firefox')
    @patch('src.selenium.Service')
    def test_scraper_close(self, mock_service, mock_firefox):
        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver

        scraper = Selenium(
                            geckodriver="fake/path/geckodriver",
                            setup=True
                        )

        scraper.close()

        # Ensure that webdriver. Firefox is called and that self.driver is set.
        mock_firefox.assert_called_once()
        self.assertIsNone(scraper.driver)

    @patch('src.selenium.WebDriverWait')
    @patch('src.selenium.webdriver.Firefox')
    @patch('src.selenium.Service')
    def test_wait_for_element(self, mock_service, mock_firefox, mock_webdriverwait):
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_firefox.return_value = mock_driver

        instance_wait = mock_webdriverwait.return_value
        instance_wait.until.return_value = mock_element

        scraper = Selenium(
                            geckodriver="fake/path/geckodriver",
                            setup=True
                        )

        result = scraper.wait_for_element(
                                type="id",
                                html_element="menu"
                            )

        self.assertEqual(result, mock_element)

    @patch('src.selenium.webdriver.Firefox')
    @patch('src.selenium.Service')
    def test_search(self, mock_service, mock_firefox):

        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver

        mock_div_content = MagicMock()
        mock_div_item = MagicMock()
        mock_a_item = MagicMock()

        # mock driver element
        mock_driver.get.return_value = None
        mock_driver.find_element.return_value = mock_div_content

        # mock element item of webpage, <ul>
        mock_div_content.find_elements.return_value = [mock_div_item]
        # <li>
        mock_div_item.find_element.return_value = mock_a_item
        # <a>
        mock_a_item.get_attribute.side_effect = ["Comic", "https://sample.com/comic"]

        scraper = Selenium(
                            geckodriver="fake/path/geckodriver",
                            setup=True
                        )

        # webclass
        webclass = MagicMock()
        webclass.search_url = "https://sample.com/search?q=comic"
        webclass.content_page_divs_css = "div.comics"
        webclass.items_comic_css = ".item"
        webclass.info_comic_css = "a"

        results = scraper.search(string="Sample", webclass=webclass)

        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], Comic)
        self.assertEqual(results[0].name, "Comic")
        self.assertEqual(results[0].link, "https://sample.com/comic")

    @patch('src.engines.selenium.webdriver.Firefox')
    @patch('src.engines.selenium.Service')
    def test_get_chapters_updates_comic(self, MockService, MockFirefox):
        # 1) Mock WebDriver
        mock_driver = MagicMock()
        MockFirefox.return_value = mock_driver

        # 2) Instantiate scraper without running setup
        scraper = Selenium(geckodriver="fake/path/geckodriver", show=True, setup=False)
        scraper.driver = mock_driver


        # mocking `Status` instance
        mock_status = MagicMock()
        mock_status.comic_name = "Comic"
        mock_status.method = "get_chapters"

        scraper.status = mock_status


        # 3) Prepare Comic and webclass
        comic = Comic(name="Test Comic", link="https://sample.com/comic")
        comic.chapters = []

        webclass = MagicMock()
        webclass.chapters_content_ul_class = ['.subchap']
        webclass.chapter_css = ['li']

        # 4) Simulate two <li> elements in the page
        mock_li_1 = MagicMock()
        mock_li_2 = MagicMock()
        mock_list = [mock_li_1, mock_li_2]
        scraper.element_find_elements = MagicMock(return_value=mock_list)
        scraper.iterator_find_elements = MagicMock(return_value=MagicMock())

        # 5) Stub iterate_chapters to capture its call and set comic.chapters
        def fake_iterate(*args, **kwargs):
            # comicObj is either positional or keyword
            comicObj = kwargs.get('comicObj') if 'comicObj' in kwargs else args[1]
            list_chapters = kwargs.get('list_chapters') if 'list_chapters' in kwargs else args[-1]
            comicObj.chapters = list_chapters
        scraper.iterate_chapters = fake_iterate

        # 6) Call get_chapters
        result = scraper.get_chapters(comic, webclass)

        # 7) Assertions
        self.assertIs(result, comic)
        mock_driver.get.assert_called_once_with(comic.link)
        self.assertEqual(comic.chapters, mock_list)


    @patch('src.engines.selenium.re', autospec=True)
    @patch('src.engines.selenium.normalize_number', autospec=True)
    @patch('src.engines.selenium.webdriver.Firefox')
    @patch('src.engines.selenium.Service')
    def test_iterate_chapters_creates_chapter_objects(
        self,
        MockService,
        MockFirefox,
        mock_norm,
        mock_re_module
    ):
        # --- Mock WebDriver and URL behavior ---
        mock_driver = MagicMock()
        mock_driver.current_window_handle = 'MAIN'
        mock_driver.window_handles = ['MAIN']
        mock_driver.current_url = 'https://sample.com/comic/ch1'
        MockFirefox.return_value = mock_driver

        # --- Prepare scraper and assign mocks ---
        scraper = Selenium(geckodriver="fake/path/geckodriver", show=True, setup=False)
        scraper.driver = mock_driver
        # mocking `Status` instance
        mock_status = MagicMock()
        mock_status.comic_name = "Comic"
        mock_status.method = "iterate_chapters"

        scraper.status = mock_status

        # --- Patch regex to find a single group '1' ---
        mock_re_module.findall.return_value = ['1']
        mock_norm.side_effect = lambda x: x

        # --- Prepare comic ---
        comic = Comic(name="Test Comic", link="https://sample.com/comic")
        comic.chapters = []

        # --- Webclass selectors ---
        webclass = MagicMock()
        webclass.chaper_name_class = 'a.name'
        webclass.chapter_link_class = 'a.link'
        webclass.container_images_div_css = '#images'

        # --- Create a single <li> with name and link elements ---
        li = MagicMock()
        name_elem = MagicMock()
        link_elem = MagicMock()
        name_elem.get_attribute.return_value = 'Chapter 1'
        link_elem.get_attribute.return_value = 'https://sample.com/comic/ch1'

        def li_find(by, selector):
            if by == By.CSS_SELECTOR and selector == webclass.chaper_name_class:
                return name_elem
            if by == By.CSS_SELECTOR and selector == webclass.chapter_link_class:
                return link_elem
            raise AssertionError(f'Unexpected selector: {selector}')
        li.find_element.side_effect = li_find

        # --- Stub tab-switching and image extraction to avoid side-effects ---
        scraper.driver.execute_script = MagicMock()
        scraper.wait_to_load_content_change_tab = MagicMock()
        scraper.get_images_chapter = MagicMock()

        # --- Execute iterate_chapters ---
        scraper.iterate_chapters(comicObj=comic, webclass=webclass, list_chapters=[li])

        # --- Assertions ---
        self.assertEqual(len(comic.chapters), 1)
        chap = comic.chapters[0]
        self.assertIsInstance(chap, Chapter)
        self.assertEqual(chap.id, 1.0)
        self.assertEqual(chap.name, '1.0')
        self.assertEqual(chap.link, mock_driver.current_url)


if __name__ == '__main__':
    unittest.main()
