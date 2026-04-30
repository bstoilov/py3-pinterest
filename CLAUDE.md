# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Unofficial Pinterest API client for Python 3. Published on PyPI as `py3-pinterest`, package directory is `py3pin`. Mimics browser requests to Pinterest's internal API endpoints — no official API key needed.

## Commands

### Tests
```bash
# All tests (these are integration tests hitting live Pinterest API)
.venv/bin/pytest tests/ -v

# Single test file
.venv/bin/pytest tests/test_boards.py -v

# Single test
.venv/bin/pytest tests/test_boards.py::test_boards_list -v
```

Tests require a `.env` file with `PINTEREST_EMAIL`, `PINTEREST_PASSWORD`, `PINTEREST_USERNAME`. Cookies are cached in `data/` and reused across runs — login only fires when the session is expired.

### Build & Publish
```bash
pip install build twine
python -m build                  # creates sdist + wheel in dist/
twine upload dist/*              # upload to PyPI
```

Publishing is also available via GitHub Actions (`workflow_dispatch`, restricted to `bstoilov`).

## Architecture

Four files make up the core, all in `py3pin/`:

**Pinterest.py** — The client. ~1500 lines, ~50 public methods. All API logic lives here. Key patterns:
- Endpoints follow `https://www.pinterest.com/resource/{ResourceName}/{action}/`
- POST body is URL-encoded with a `data` field containing JSON `{options, context}`
- GET requests encode the same structure as query parameters
- Login uses Selenium + ChromeDriver to handle Pinterest's JS login flow, then extracts cookies
- Upload flow (image & video): register media → upload to S3 → poll VIPResource for status → create pin
- Video pins use `StoryPinResource/create`, image pins use `PinResource/create`
- Media types for registration: `"image-story-pin"` for images, `"video-story-pin"` for videos

**RequestBuilder.py** — Encodes options/context into Pinterest's internal payload format. `buildPost()` for POST body, `buildGet()` for query params. Adds a `_` timestamp parameter.

**BookmarkManager.py** — Tracks opaque pagination tokens. Pinterest uses cursor-based pagination with bookmark strings. Methods store/retrieve/reset bookmarks keyed by `(primary, secondary)`. The `reset_bookmark` param on API methods must be applied *before* the `-end-` check, not inside it.

**Registry.py** — Persists session cookies as JSON to `{cred_root}/{email}`. Loads on init if the file exists. Must never delete existing files/directories.

### Data Flow
1. `Pinterest.__init__` → creates `requests.Session`, `RequestBuilder`, `BookmarkManager`, `Registry`
2. `login()` → Selenium gets cookies → `Registry.update_all()` persists them
3. API calls → `RequestBuilder` encodes payload → `request()` adds CSRF headers → `requests.Session` fires request
4. Paginated calls → `BookmarkManager` tracks position → caller loops until empty list returned

### Test Architecture
- All tests are **integration tests** against the live Pinterest API (no mocks)
- `conftest.py` provides session-scoped `pinterest` client and `test_board` fixtures shared across all test files
- The `pinterest` fixture auto-detects if cookies are valid before triggering Selenium login
- The `test_board` fixture finds or creates a board named "test" — it persists across runs

## Important Conventions

- `reset_bookmark` pattern: the reset must happen **before** `get_bookmark()` and the `-end-` check, not inside the `-end-` block. Every paginated method follows this pattern.
- Pinterest's S3 upload URL comes from the registration response — never hardcode it.
- `upload_url`, `upload_parameters`, and `upload_id` are extracted from the registration response via `_extract_upload_entry()`.
- Image uploads pass `upload_id` (as int) and `image_signature` to `PinResource/create`. Do not construct image URLs.
- Video pins require `canvas_aspect_ratio: 0.56` (9:16 portrait) regardless of actual video dimensions.
- Version is in `py3pin/__version__.py` — single source of truth, read by `setup.py`.
