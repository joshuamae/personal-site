from datetime import date
from urllib.request import urlopen
from xml.etree import ElementTree

import pytest
from playwright.sync_api import Page, expect


SITE_ORIGIN = "https://www.joshuamae.com"
pytestmark = pytest.mark.regression


def read_site_file(site_url: str, path: str) -> str:
    with urlopen(f"{site_url}/{path}", timeout=5) as response:
        assert response.status == 200
        return response.read().decode("utf-8")


def test_homepage_exposes_search_and_social_metadata(homepage: Page):
    expect(homepage.locator('html[lang="en-US"]')).to_have_count(1)
    expect(homepage.locator('meta[name="description"]')).to_have_attribute(
        "content",
        "Hi! My name is Joshua Mae. I currently work in IT and enjoy learning about tech.",
    )
    expect(homepage.locator('link[rel="canonical"]')).to_have_attribute(
        "href", f"{SITE_ORIGIN}/"
    )
    expect(homepage.locator('meta[property="og:title"]')).to_have_attribute(
        "content", "Joshua Mae"
    )
    expect(homepage.locator('meta[property="og:type"]')).to_have_attribute(
        "content", "website"
    )
    expect(homepage.locator('meta[property="og:image"]')).to_have_attribute(
        "content", f"{SITE_ORIGIN}/imgs/preview_image.png"
    )


def test_robots_file_allows_crawling_and_declares_sitemap(site_url: str):
    robots = read_site_file(site_url, "robots.txt").lower()

    assert "user-agent: *" in robots
    assert "disallow:" not in robots
    assert f"sitemap: {SITE_ORIGIN}/sitemap.xml" in robots


def test_sitemap_is_valid_and_contains_the_canonical_homepage(site_url: str):
    sitemap = read_site_file(site_url, "sitemap.xml")
    root = ElementTree.fromstring(sitemap)
    namespace = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = root.findall("sitemap:url", namespace)

    assert len(urls) == 1
    assert urls[0].findtext("sitemap:loc", namespaces=namespace) == f"{SITE_ORIGIN}/"

    last_modified = urls[0].findtext("sitemap:lastmod", namespaces=namespace)
    assert last_modified is not None
    date.fromisoformat(last_modified)
