# py3-pinterest

Unofficial Pinterest REST API client for Python 3. Mimics browser requests to interact with Pinterest's internal API endpoints (no official API key needed).

Published on PyPI as `py3-pinterest`. Package directory is `py3pin`.

## Project Structure

```
py3pin/                  # Main package
  Pinterest.py           # Core client class - all API methods live here
  RequestBuilder.py      # Builds URL-encoded POST/GET payloads for Pinterest's internal API format
  BookmarkManager.py     # Manages pagination bookmarks (Pinterest uses opaque bookmark tokens for cursor-based pagination)
  Registry.py            # Persists session cookies to disk as JSON files (one file per username)
  __version__.py         # Single source of version (currently 1.3.0)
Examples/                # Usage examples (no automated test suite exists)
setup.py                 # Packaging and PyPI upload via `python setup.py upload`
```

## Architecture

**Pinterest.py** is the main client. It:
- Initializes a `requests.Session` with browser-like headers (User-Agent spoofing)
- Uses Selenium + ChromeDriver for login (handles Pinterest's JS-heavy login flow), then extracts cookies
- Stores/loads cookies via `Registry` so subsequent runs skip login
- All API calls hit Pinterest's internal `resource/` endpoints with JSON payloads encoded by `RequestBuilder`
- Pagination: methods accept `reset_bookmark=False` param; `BookmarkManager` tracks bookmark tokens per-resource so calling the same method repeatedly fetches the next page

**Key patterns:**
- Pinterest endpoints follow the pattern `https://www.pinterest.com/resource/{ResourceName}/{action}/`
- POST body is URL-encoded with a `data` field containing JSON with `options` and `context`
- GET requests append the same structure as query parameters
- Proxy support via `proxies` and `proxy_host` constructor params

## Dependencies

Python >= 3.5. Key deps: `requests`, `beautifulsoup4`, `requests-toolbelt`, `selenium`, `webdriver-manager`.

## Publishing

```bash
pip install twine
python setup.py upload  # builds sdist+wheel, uploads via twine, tags git
```
