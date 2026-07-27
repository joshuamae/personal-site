from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from playwright.sync_api import Page


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class QuietRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


@pytest.fixture(scope="session")
def site_url():
    handler = partial(QuietRequestHandler, directory=PROJECT_ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(
        target=server.serve_forever,
        daemon=True,
        name="personal-site-test-server",
    )
    thread.start()

    yield f"http://127.0.0.1:{server.server_port}"

    server.shutdown()
    server.server_close()
    thread.join(timeout=5)


@pytest.fixture
def homepage(page: Page, site_url: str) -> Page:
    response = page.goto(site_url)

    assert response is not None
    assert response.ok
    return page
