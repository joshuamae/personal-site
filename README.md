# Joshua Mae's Personal Website

My personal website, deployed with Cloudflare Pages.

## Technology

- HTML
- CSS
- JavaScript
- pytest
- Playwright

## Run locally

Serve the project root with any static web server:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Test

Install the test dependencies and Playwright's Chromium browser, then run pytest:

```sh
python3 -m pip install -r requirements.txt
playwright install chromium
pytest
```
