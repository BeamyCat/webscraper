import unittest
from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    def test_normalize_url_identity(self):
        input_url = "www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
        
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_normalize_url2(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_normalize_url3(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_normalize_url4(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_beamy(self):
        input_url = "http://beamycat.neocities.org"
        actual = normalize_url(input_url)
        expected = "beamycat.neocities.org"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_beamy2(self):
        input_url = "http://beamycat.neocities.org/"
        actual = normalize_url(input_url)
        expected = "beamycat.neocities.org"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_beamy3(self):
        input_url = "https://beamycat.neocities.org"
        actual = normalize_url(input_url)
        expected = "beamycat.neocities.org"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_beamy4(self):
        input_url = "https://beamycat.neocities.org/"
        actual = normalize_url(input_url)
        expected = "beamycat.neocities.org"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_beamy4(self):
        input_url = "https://beamycat.neocities.org/about/"
        actual = normalize_url(input_url)
        expected = "beamycat.neocities.org/about"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_ext(self):
        input_url = "https://beamycat.neocities.org/first-page/?name=Beamy&genders=girl+things&letter=T&prosecutor=Klavier+Gavin#form"
        actual = normalize_url(input_url)
        expected = "beamycat.neocities.org/first-page/?name=Beamy&genders=girl+things&letter=T&prosecutor=Klavier+Gavin#form"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_ext2(self):
        input_url = "https://beamycat.neocities.org/first-page/?name=Beamy&genders=girl+things&letter=T&prosecutor=Klavier+Gavin#form/"
        actual = normalize_url(input_url)
        expected = "beamycat.neocities.org/first-page/?name=Beamy&genders=girl+things&letter=T&prosecutor=Klavier+Gavin#form"
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
