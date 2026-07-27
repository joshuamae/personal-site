import pytest
from playwright.sync_api import Page, expect


pytestmark = pytest.mark.regression


def test_page_has_accessible_landmarks_and_control_names(homepage: Page):
    expect(homepage.get_by_role("main")).to_be_visible()
    expect(
        homepage.get_by_role("navigation", name="Social profiles")
    ).to_be_visible()
    expect(
        homepage.get_by_role("link", name="Joshua Mae on GitHub")
    ).to_be_visible()
    expect(
        homepage.get_by_role("link", name="Joshua Mae on LinkedIn")
    ).to_be_visible()
    expect(homepage.locator("#theme-toggle")).to_have_attribute(
        "aria-label", "Switch to dark mode"
    )
    expect(homepage.locator('svg[aria-hidden="true"]')).to_have_count(4)


def test_interactive_controls_follow_a_logical_keyboard_order(homepage: Page):
    github = homepage.get_by_role("link", name="Joshua Mae on GitHub")
    linkedin = homepage.get_by_role("link", name="Joshua Mae on LinkedIn")
    theme_toggle = homepage.locator("#theme-toggle")

    homepage.keyboard.press("Tab")
    expect(github).to_be_focused()

    homepage.keyboard.press("Tab")
    expect(linkedin).to_be_focused()

    homepage.keyboard.press("Tab")
    expect(theme_toggle).to_be_focused()


def test_reduced_motion_preference_disables_transitions(
    page: Page, site_url: str
):
    page.emulate_media(reduced_motion="reduce")
    page.goto(site_url)

    for selector in ("body", ".social-link", ".theme-toggle"):
        transition_duration = page.locator(selector).first.evaluate(
            "(element) => getComputedStyle(element).transitionDuration"
        )
        assert transition_duration == "0s"
