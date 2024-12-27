import unittest
from msg_split import HTMLFragmenter  # замените на имя вашего файла
from bs4 import BeautifulSoup


class TestHTMLFragmenter(unittest.TestCase):
    def setUp(self):
        self.max_len = 4096
        self.fragmenter = HTMLFragmenter(self.max_len)

    def test_split_long_html(self):
        html = "<p>" + "a" * 100 + "</p>"
        fragments = list(self.fragmenter.split_html(html))
        self.assertTrue(all(len(fragment) <= self.max_len for fragment in fragments))

    def test_split_with_nested_tags(self):
        html = "<div><p><span>Hello</span></p><p>World</p></div>"
        fragments = list(self.fragmenter.split_html(html))
        self.assertTrue(all(len(fragment) <= self.max_len for fragment in fragments))

    def test_empty_html(self):
        html = ""
        fragments = list(self.fragmenter.split_html(html))
        self.assertEqual(len(fragments), 0)


if __name__ == "__main__":
    unittest.main()
