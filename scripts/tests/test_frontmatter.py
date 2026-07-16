"""
Tests for scripts/frontmatter.py's generate_front_matter, focused on the
optional link_title parameter (Hugo's native linkTitle field, used to
shorten a page's sidebar/breadcrumb label -- see scripts/writer.py for
where the override value comes from).
"""
import unittest

from scripts.frontmatter import generate_front_matter


class GenerateFrontMatterLinkTitleTests(unittest.TestCase):
    def test_omits_link_title_line_by_default(self):
        front_matter = generate_front_matter(title="Some Page", weight=10, source="https://example.com")

        self.assertNotIn('linkTitle', front_matter)

    def test_omits_link_title_line_when_explicitly_none(self):
        front_matter = generate_front_matter(title="Some Page", weight=10, source="https://example.com", link_title=None)

        self.assertNotIn('linkTitle', front_matter)

    def test_includes_link_title_line_when_given(self):
        front_matter = generate_front_matter(
            title="How to Get Started with Clean Code", weight=10, source="https://example.com",
            link_title="Get Started",
        )

        self.assertIn('linkTitle: "Get Started"', front_matter)
        self.assertIn('title: "How to Get Started with Clean Code"', front_matter)

    def test_link_title_is_yaml_escaped_like_title(self):
        front_matter = generate_front_matter(
            title="Some Page", weight=10, source="https://example.com",
            link_title='Say "Hi"',
        )

        self.assertIn('linkTitle: "Say \\"Hi\\""', front_matter)


class GenerateFrontMatterSidebarHideTests(unittest.TestCase):
    def test_omits_sidebar_block_by_default(self):
        front_matter = generate_front_matter(title="Some Page", weight=10, source="https://example.com")

        self.assertNotIn('sidebar:', front_matter)

    def test_includes_sidebar_hide_block_when_requested(self):
        front_matter = generate_front_matter(
            title="Some Page", weight=10, source="https://example.com",
            sidebar_hide=True,
        )

        self.assertIn('sidebar:\n  hide: true\n', front_matter)


if __name__ == '__main__':
    unittest.main()
