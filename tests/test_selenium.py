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

from getpycomic.models import (
                        Comic,
                        Chapter,
                        ImageChapter
                    )
from getpycomic.engines.selenium import Selenium
from getpycomic.status import Status

from selenium.webdriver.common.by import By


class TestSeleniumClass(unittest.TestCase):
    @patch('getpycomic.selenium.webdriver.Firefox')
    @patch('getpycomic.selenium.Service')
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

    @patch('getpycomic.selenium.webdriver.Firefox')
    @patch('getpycomic.selenium.Service')
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

    @patch('getpycomic.selenium.WebDriverWait')
    @patch('getpycomic.selenium.webdriver.Firefox')
    @patch('getpycomic.selenium.Service')
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

    @patch('getpycomic.selenium.webdriver.Firefox')
    @patch('getpycomic.selenium.Service')
    def test_search(self, mock_service, mock_firefox):

        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver

        mock_div_content = MagicMock()
        mock_div_item = MagicMock()
        mock_a_item = MagicMock()

        # mock driver element
        mock_driver.get.return_value = None
        mock_driver.find_element.return_value = mock_div_content

        # mock info comic name
        mock_info_item = MagicMock()
        mock_info_item.get_attribute.return_value = "Comic"

        # mock link comic <a>
        mock_a_tag = MagicMock()
        mock_a_tag.get_attribute.return_value = "https://sample.com/comic"

        # create html structure
        mock_info_item.find_element.return_value = mock_a_tag
        mock_div_item.find_element.return_value = mock_info_item
        mock_div_content.find_elements.return_value = [mock_div_item]

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


    @patch('getpycomic.engines.selenium.Selenium.iterator_find_elements')
    @patch('getpycomic.engines.selenium.Selenium.element_find_elements')
    def test_get_chapters_basic(self, mock_element_find_elements, mock_iterator_find_elements):
        # Instancia de la clase que contiene get_chapters
        scraper = Selenium(
                            geckodriver="fake/path/geckodriver",
                            setup=False
                        )
        scraper.driver = MagicMock()
        scraper.status = MagicMock()
        scraper.to_thread_scraping = MagicMock()
        scraper.iterate_get_chapter_images = MagicMock()

        # Comic simulado
        comic = Comic(name="TestComic", link="http://example.com", chapters=[])

        # Webclass simulado
        webclass = MagicMock()
        webclass.chapters_content_ul_class = ".chapters"
        webclass.chapter_css = "li"
        webclass.chaper_name_class = "a"
        webclass.chapter_link_class = "a"
        webclass.button_show_all_chapters = ".showall"

        # Simulación de la lista de capítulos UL
        ul_element = MagicMock()
        mock_iterator_find_elements.return_value = ul_element

        # Simulación de capítulos (li)
        li1 = MagicMock()
        a1 = MagicMock()
        a1.get_attribute.side_effect = ["Chapter 1", "http://example.com/ch1"]
        li1.find_element.side_effect = [a1, a1]

        li2 = MagicMock()
        a2 = MagicMock()
        a2.get_attribute.side_effect = ["Chapter 2", "http://example.com/ch2"]
        li2.find_element.side_effect = [a2, a2]

        mock_element_find_elements.return_value = [li1, li2]

        # Ejecutar
        result = scraper.get_chapters(comic=comic, webclass=webclass)

        # Aserciones
        self.assertEqual(len(result.chapters), 2)
        self.assertEqual(result.chapters[0].link, "http://example.com/ch1")
        self.assertEqual(result.chapters[1].link, "http://example.com/ch2")
        scraper.iterate_get_chapter_images.assert_called_once()


if __name__ == '__main__':
    unittest.main()
