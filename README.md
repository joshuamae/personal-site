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

Install the test dependencies and Playwright browsers:

```sh
python3 -m pip install -r requirements.txt
playwright install chromium firefox
```

Run the fast smoke suite in Chromium:

```sh
pytest -m smoke --browser chromium
```

Run the complete regression suite in Chromium and Firefox:

```sh
pytest --browser chromium --browser firefox
```

Tests are organized by concern in `tests/`. Shared server and page setup lives
in `tests/conftest.py`; the `smoke` and `regression` markers can be used to
select the desired suite.
