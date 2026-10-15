
from pathlib import Path
import unittest


class WebsiteTests(unittest.TestCase):
    def test_homepage_has_project_title(self):
        html = Path("index.html").read_text(encoding="utf-8")
        self.assertIn("<title>JYB Deployment Project</title>", html)

    def test_homepage_has_project_heading(self):
        html = Path("index.html").read_text(encoding="utf-8")
        self.assertIn("JYB Deployment Project", html)

    def test_homepage_has_version_label(self):
        html = Path("index.html").read_text(encoding="utf-8")
        self.assertIn('id="version"', html)


if __name__ == "__main__":
    unittest.main()
