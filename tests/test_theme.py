import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression


@pytest.mark.parametrize(
    ("system_theme", "expected_theme", "next_theme", "visible_icon"),
    [
        pytest.param("light", "light", "dark", ".moon-icon", id="system-light"),
        pytest.param("dark", "dark", "light", ".sun-icon", id="system-dark"),
    ],
)
def test_initial_theme_follows_system_preference(
    page: Page,
    site_url: str,
    system_theme: str,
    expected_theme: str,
    next_theme: str,
    visible_icon: str,
):
    page.emulate_media(color_scheme=system_theme)
    page.goto(site_url)

    expect(page.locator("html")).to_have_attribute("data-theme", expected_theme)
    expect(
        page.get_by_role("button", name=f"Switch to {next_theme} mode")
    ).to_be_visible()
    expect(page.locator(visible_icon)).to_be_visible()


@pytest.mark.smoke
def test_theme_choice_persists_after_reload(page: Page, site_url: str):
    page.emulate_media(color_scheme="light")
    page.goto(site_url)
    theme_toggle = page.locator("#theme-toggle")

    theme_toggle.click()

    expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    expect(theme_toggle).to_have_attribute("aria-label", "Switch to light mode")

    page.reload()

    expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    assert page.evaluate("localStorage.getItem('theme')") == "dark"


@pytest.mark.parametrize(
    ("saved_theme", "system_theme"),
    [
        pytest.param("light", "dark", id="saved-light"),
        pytest.param("dark", "light", id="saved-dark"),
    ],
)
def test_saved_theme_overrides_system_preference(
    page: Page,
    site_url: str,
    saved_theme: str,
    system_theme: str,
):
    page.add_init_script(f"localStorage.setItem('theme', '{saved_theme}')")
    page.emulate_media(color_scheme=system_theme)
    page.goto(site_url)

    expect(page.locator("html")).to_have_attribute("data-theme", saved_theme)


def test_page_tracks_system_theme_changes_without_a_saved_choice(
    page: Page, site_url: str
):
    page.emulate_media(color_scheme="light")
    page.goto(site_url)

    page.emulate_media(color_scheme="dark")

    expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    expect(page.get_by_role("button", name="Switch to light mode")).to_be_visible()


def test_saved_choice_is_not_replaced_by_a_system_theme_change(
    page: Page, site_url: str
):
    page.add_init_script("localStorage.setItem('theme', 'light')")
    page.emulate_media(color_scheme="light")
    page.goto(site_url)

    page.emulate_media(color_scheme="dark")

    expect(page.locator("html")).to_have_attribute("data-theme", "light")
    expect(page.get_by_role("button", name="Switch to dark mode")).to_be_visible()


def test_theme_toggle_works_when_storage_is_unavailable(
    page: Page, site_url: str
):
    page_errors = []
    page.on("pageerror", lambda error: page_errors.append(error))
    page.add_init_script(
        """
        for (const method of ["getItem", "setItem"]) {
          Object.defineProperty(Storage.prototype, method, {
            configurable: true,
            value() {
              throw new DOMException("Storage is unavailable", "SecurityError");
            },
          });
        }
        """
    )
    page.emulate_media(color_scheme="light")
    page.goto(site_url)

    page.get_by_role("button", name="Switch to dark mode").click()

    expect(page.locator("html")).to_have_attribute("data-theme", "dark")
    expect(page.get_by_role("button", name="Switch to light mode")).to_be_visible()
    assert page_errors == []
