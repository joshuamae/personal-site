from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from playwright.sync_api import expect, sync_playwright


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class QuietRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


@pytest.fixture(scope="module")
def site_url():
    handler = partial(QuietRequestHandler, directory=PROJECT_ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://127.0.0.1:{server.server_port}"

    server.shutdown()
    thread.join()


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()


def test_first_load_uses_system_theme(page, site_url):
    page.emulate_media(color_scheme="light")
    page.goto(site_url)

    assert page.title() == "Joshua Mae"
    expect(page.get_by_role("heading", name="Joshua Mae")).to_be_visible()
    expect(page.locator("html")).to_have_attribute("data-theme", "light")
    expect(page.get_by_role("button")).to_have_text("Switch to dark mode")


def test_theme_choice_persists(page, site_url):
    page.emulate_media(color_scheme="light")
    page.goto(site_url)
    theme_toggle = page.get_by_role("button")

    theme_toggle.click()

    expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    expect(theme_toggle).to_have_attribute("aria-pressed", "true")
    expect(theme_toggle).to_have_text("Switch to light mode")

    page.reload()

    expect(page.locator("html")).to_have_attribute("data-theme", "dark")
