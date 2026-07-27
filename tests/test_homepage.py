import pytest
from playwright.sync_api import Page, expect


SOCIAL_PROFILES = {
    "Joshua Mae on GitHub": "https://github.com/joshuamae",
    "Joshua Mae on LinkedIn": "https://www.linkedin.com/in/joshuamaetech",
}

pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_homepage_renders_critical_content(homepage: Page):
    assert homepage.title() == "Joshua Mae"
    expect(homepage.get_by_role("heading", name="Joshua Mae")).to_be_visible()
    expect(homepage.get_by_text("IT Specialist", exact=True)).to_be_visible()
    expect(
        homepage.get_by_text("Vermont, United States", exact=True)
    ).to_be_visible()
    expect(
        homepage.get_by_role("navigation", name="Social profiles")
    ).to_be_visible()
    expect(homepage.locator("#theme-toggle")).to_be_visible()


def test_social_profile_links_have_safe_external_link_attributes(homepage: Page):
    for accessible_name, expected_url in SOCIAL_PROFILES.items():
        link = homepage.get_by_role("link", name=accessible_name)
        expect(link).to_have_attribute("href", expected_url)
        expect(link).to_have_attribute("target", "_blank")

        rel_tokens = (link.get_attribute("rel") or "").split()
        assert {"noopener", "noreferrer"} <= set(rel_tokens)


def test_local_stylesheet_and_script_load_without_errors(page: Page, site_url: str):
    failed_responses = []
    page_errors = []
    page.on(
        "response",
        lambda response: failed_responses.append((response.url, response.status))
        if response.url.startswith(site_url) and response.status >= 400
        else None,
    )
    page.on("pageerror", lambda error: page_errors.append(error))

    page.goto(site_url)
    page.wait_for_load_state("networkidle")

    local_resources = page.evaluate(
        """
        () => performance.getEntriesByType("resource")
          .map(({ name }) => name)
          .filter((url) => url.startsWith(location.origin))
        """
    )
    assert f"{site_url}/main.css" in local_resources
    assert f"{site_url}/theme-toggle.js" in local_resources
    assert failed_responses == []
    assert page_errors == []
