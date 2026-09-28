import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data


class TestCrawl(unittest.TestCase):
    ########## normalize_url ##########
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
    
    ########## get_heading_from_html ##########
    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)
    
    def test_get_heading_from_html_2(self):
        input_body = """<html>
  <body>
    <h1>Welcome to <b>Boot.dev</b></h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        actual = get_heading_from_html(input_body)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)
    
    def test_get_heading_from_html_3(self):
        input_body = """<html>
  <body>
    <main>
      <h2>This page only has h2</h2>
      <p>Per aspera ad astra.</p>
    </main>
  </body>
</html>"""
        actual = get_heading_from_html(input_body)
        expected = "This page only has h2"
        self.assertEqual(actual, expected)
    
    def test_get_heading_from_html_none(self):
        input_body = """<html>
  <body>
    <main>
      <h3>This page only has h3</h3>
      <p>Per aspera ad astra.</p>
    </main>
  </body>
</html>"""
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    ########## get_first_paragraph_from_html ##########
    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)
    
    def test_get_first_paragraph_from_html_2(self):
        input_body = """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Learn to code by building real projects."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_3(self):
        input_body = """<html>
  <body>
    <main>
      <h2>This page only has h2</h2>
      <p><i>Per aspera ad astra.</i></p>
    </main>
  </body>
</html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Per aspera ad astra."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_none(self):
        input_body = """<html>
  <body>
    <h1>BEHOLD THE MIGHTY SPAN</h1>
    <main>
        <span>Span</span>
    </main>
  </body>
</html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)
    
    ########## get_urls_from_html ##########
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_link_and_image(self):
        input_url = "https://www.boot.dev"
        input_body = """<html>
  <body>
    <a href="https://crawler-test.com">Go to Boot.dev</a>
    <img src="/logo.png" alt="Boot.dev Logo" />
  </body>
</html>"""
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_image_only(self):
        input_url = "https://beamycat.neocities.org"
        input_body = """<html>
  <body>
    <h1>BeamyCat</h1>
    <p>Per aspera ad astra.</p>
    <img src="/img/picrew/beamy_picrew.png" alt="Picrew" />
  </body>
</html>"""
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_many(self):
        input_url = "https://beamycat.neocities.org"
        input_body = """<html>
  <body>
    <nav>
      <a href="/about">About</a>
      <a href="/games">Games</a>
      <a href="/art">Art</a>
    </nav>
    <h1>BeamyCat</h1>
    <p>Per aspera ad astra.</p>
    <img src="/img/picrew/beamy_picrew.png" alt="Picrew" />
    <p>Here's Roxie!</p>
    <img src="/art/img/roxie-rohls.png" alt="Roxanne Rohls" />
    <p>And here's Vivian :3</p>
    <img src="/art/img/vivian-cottonsmith.png" alt="Vivian Cottonsmith" />
    <a href="https://robinproblem.neocities.org">Robin Problem</a>
  </body>
</html>"""
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://beamycat.neocities.org/about", 
            "https://beamycat.neocities.org/games", 
            "https://beamycat.neocities.org/art",
            "https://robinproblem.neocities.org",
        ]
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_none(self):
        input_url = "https://beamycat.neocities.org"
        input_body = """<html>
  <body>
    <h1>BeamyCat</h1>
    <p>Per aspera ad astra.</p>
  </body>
</html>"""
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
    
    ########## get_images_from_html ##########
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_link_and_image(self):
        input_url = "https://www.boot.dev"
        input_body = """<html>
  <body>
    <a href="https://crawler-test.com">Go to Boot.dev</a>
    <img src="/logo.png" alt="Boot.dev Logo" />
  </body>
</html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://www.boot.dev/logo.png"]
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_links_only(self):
        input_url = "https://beamycat.neocities.org"
        input_body = """<html>
  <body>
    <h1>BeamyCat</h1>
    <a href="/about">About</a>
    <p>Per aspera ad astra.</p>
    <a href="https://robinproblem.neocities.org">Robin Problem</a>
  </body>
</html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_many(self):
        input_url = "https://beamycat.neocities.org"
        input_body = """<html>
  <body>
    <nav>
      <a href="/about">About</a>
      <a href="/games">Games</a>
      <a href="/art">Art</a>
    </nav>
    <h1>BeamyCat</h1>
    <p>Per aspera ad astra.</p>
    <img src="/img/picrew/beamy_picrew.png" alt="Picrew" />
    <p>Here's Roxie!</p>
    <img src="/art/img/roxie-rohls.png" alt="Roxanne Rohls" />
    <p>And here's Vivian :3</p>
    <img src="/art/img/vivian-cottonsmith.png" alt="Vivian Cottonsmith" />
    <a href="https://robinproblem.neocities.org">Robin Problem</a>
    <img src="https://neocities.org/img/cat.png" alt="Neocities logo" />
  </body>
</html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://beamycat.neocities.org/img/picrew/beamy_picrew.png", 
            "https://beamycat.neocities.org/art/img/roxie-rohls.png", 
            "https://beamycat.neocities.org/art/img/vivian-cottonsmith.png",
            "https://neocities.org/img/cat.png",
        ]
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_none(self):
        input_url = "https://beamycat.neocities.org"
        input_body = """<html>
  <body>
    <h1>BeamyCat</h1>
    <p>Per aspera ad astra.</p>
  </body>
</html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
    
    ########## extract_page_data ##########
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)
    
    def test_extract_page_data_ext(self):
        input_url = "https://beamycat.neocities.org"
        input_body = """<html>
  <body>
    <nav>
      <a href="/about">About</a>
      <a href="/games">Games</a>
      <a href="/art">Art</a>
    </nav>
    <h1>BeamyCat</h1>
    <p>Per aspera ad astra.</p>
    <img src="/img/picrew/beamy_picrew.png" alt="Picrew" />
    <p>Here's Roxie!</p>
    <img src="/art/img/roxie-rohls.png" alt="Roxanne Rohls" />
    <p>And here's Vivian :3</p>
    <img src="/art/img/vivian-cottonsmith.png" alt="Vivian Cottonsmith" />
    <a href="https://robinproblem.neocities.org">Robin Problem</a>
    <img src="https://neocities.org/img/cat.png" alt="Neocities logo" />
  </body>
</html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://beamycat.neocities.org",
            "heading": "BeamyCat",
            "first_paragraph": "Per aspera ad astra.",
            "outgoing_links": [
                "https://beamycat.neocities.org/about", 
                "https://beamycat.neocities.org/games", 
                "https://beamycat.neocities.org/art",
                "https://robinproblem.neocities.org",
            ],
            "image_urls": [
                "https://beamycat.neocities.org/img/picrew/beamy_picrew.png", 
                "https://beamycat.neocities.org/art/img/roxie-rohls.png", 
                "https://beamycat.neocities.org/art/img/vivian-cottonsmith.png",
                "https://neocities.org/img/cat.png",
            ],
        }
        self.assertEqual(actual, expected)
    
    def test_extract_page_data_bare(self):
        input_url = "https://www.blank.org"
        input_body = "<html><body></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://www.blank.org",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
