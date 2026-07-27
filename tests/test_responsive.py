import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression


@pytest.mark.parametrize(
    "viewport",
    [
        pytest.param({"width": 320, "height": 568}, id="small-phone"),
        pytest.param({"width": 768, "height": 1024}, id="tablet"),
    ],
)
def test_layout_remains_visible_without_horizontal_overflow(
    page: Page, site_url: str, viewport: dict[str, int]
):
    page.set_viewport_size(viewport)
    page.goto(site_url)

    expect(page.get_by_role("heading", name="Joshua Mae")).to_be_visible()
    expect(page.get_by_role("navigation", name="Social profiles")).to_be_visible()
    expect(page.locator("#theme-toggle")).to_be_visible()

    has_horizontal_overflow = page.evaluate(
        "document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )
    assert not has_horizontal_overflow
