<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/0/08/Pinterest-logo.png" alt="Pinterest" width="100">
</p>

<h1 align="center">py3-pinterest</h1>

<p align="center">
  <strong>The most complete unofficial Pinterest API client for Python</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/py3-pinterest/"><img src="https://img.shields.io/pypi/v/py3-pinterest.svg?style=for-the-badge&logo=pypi&logoColor=white" alt="PyPI"></a>
  &nbsp;
  <a href="https://pypi.org/project/py3-pinterest/"><img src="https://img.shields.io/pypi/pyversions/py3-pinterest.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  &nbsp;
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge" alt="License"></a>
  &nbsp;
  <a href="https://github.com/bstoilov/py3-pinterest/stargazers"><img src="https://img.shields.io/github/stars/bstoilov/py3-pinterest?style=for-the-badge&logo=github" alt="Stars"></a>
</p>

<br>

<p align="center">
  <b>📌 Pin</b> · <b>📤 Upload Images & Videos</b> · <b>📋 Manage Boards</b> · <b>👥 Follow</b> · <b>🔍 Search</b> · <b>💬 Comment & Message</b>
</p>

<p align="center">
  <em>No API key needed. Works by mimicking browser requests to Pinterest's internal endpoints.</em>
</p>

---

## 🚀 What's New in v2.0.0

> **The comeback release.** Nearly every core feature has been fixed, modernized, or rewritten.

| | Highlight |
|---|---|
| 🎬 | **Video pin uploads** — full Story Pin / Idea Pin support via S3 upload flow |
| 🖼️ | **Image uploads rewritten** — old broken `/upload-image/` replaced with working S3 flow |
| 📄 | **Pagination fixed** — `reset_bookmark` bug fixed across all 12 paginated methods |
| 🔐 | **Login hardened** — cookie banner handling, language-independent selectors, proper cleanup |
| 🗑️ | **Board deletion** — new `delete_board()` method |
| 📂 | **Board sections** — now supports `page_size` (up to 100, was hardcoded to 25) |
| 🛡️ | **No more data loss** — Registry no longer `rmtree`'s your directories on init |
| 📦 | **Dependency pins** — `selenium>=4.0.0`, `webdriver-manager>=4.0.0` |

<details>
<summary><b>📋 Full list of resolved issues (click to expand)</b></summary>
<br>

| Issue | Description | Status |
|-------|-------------|--------|
| [#220](https://github.com/bstoilov/py3-pinterest/issues/220) | Video upload not supported | ✅ Fixed |
| [#219](https://github.com/bstoilov/py3-pinterest/issues/219) | Login — element not interactable (cookie banner) | ✅ Fixed |
| [#218](https://github.com/bstoilov/py3-pinterest/issues/218) | Error in search (pin & board) | ✅ Fixed |
| [#217](https://github.com/bstoilov/py3-pinterest/issues/217) | 403 Forbidden — `_ngjs` URL prefix | ✅ Fixed |
| [#213](https://github.com/bstoilov/py3-pinterest/issues/213) | Search page size & pagination | ✅ Fixed |
| [#209](https://github.com/bstoilov/py3-pinterest/issues/209) | `pin()` unexpected keyword `image_path` | ✅ Fixed |
| [#208](https://github.com/bstoilov/py3-pinterest/issues/208) | `load_pin` KeyError `v3GetPinQuery` | ✅ Fixed |
| [#207](https://github.com/bstoilov/py3-pinterest/issues/207) | 404 on `PinResource/create` | ✅ Fixed |
| [#205](https://github.com/bstoilov/py3-pinterest/issues/205) | `load_pin` — `__PWS_DATA__` / `props` error | ✅ Fixed |
| [#204](https://github.com/bstoilov/py3-pinterest/issues/204) | 401 Unauthorized on `/upload-image/` | ✅ Fixed |
| [#203](https://github.com/bstoilov/py3-pinterest/issues/203) | `get_user_pins` stops short on large accounts | ✅ Fixed |
| [#202](https://github.com/bstoilov/py3-pinterest/issues/202) | Timeout `<object>` error (selenium 3 + urllib3 2) | ✅ Fixed |
| [#200](https://github.com/bstoilov/py3-pinterest/issues/200) | Downstream `extruct` issue | ✅ N/A (dependency removed) |
| [#195](https://github.com/bstoilov/py3-pinterest/issues/195) | Login error — ChromeDriver URL change | ✅ Fixed |
| [#193](https://github.com/bstoilov/py3-pinterest/issues/193) | Login fails for non-English locales | ✅ Fixed |
| [#191](https://github.com/bstoilov/py3-pinterest/issues/191) | ChromeDriver download 404 | ✅ Fixed |
| [#188](https://github.com/bstoilov/py3-pinterest/issues/188) | 404 on `PinResource/create` | ✅ Fixed |
| [#187](https://github.com/bstoilov/py3-pinterest/issues/187) | `get_board_sections` limited to 25 | ✅ Fixed |
| [#184](https://github.com/bstoilov/py3-pinterest/issues/184) | Bad request — can't create pins | ✅ Fixed |
| [#181](https://github.com/bstoilov/py3-pinterest/issues/181) | 403 Forbidden on `PinResource/create` | ✅ Fixed |
| [#178](https://github.com/bstoilov/py3-pinterest/issues/178) | Can't upload a new pin | ✅ Fixed |
| [#176](https://github.com/bstoilov/py3-pinterest/issues/176) | Issue creating pins | ✅ Fixed |
| [#175](https://github.com/bstoilov/py3-pinterest/issues/175) | Can't post a new pin | ✅ Fixed |
| [#174](https://github.com/bstoilov/py3-pinterest/issues/174) | Pinning fails with HTML output | ✅ Fixed |
| [#156](https://github.com/bstoilov/py3-pinterest/issues/156) | Credentials not storing | ✅ Fixed |
| [#148](https://github.com/bstoilov/py3-pinterest/issues/148) | Facing problem with pinning image | ✅ Fixed |
| [#147](https://github.com/bstoilov/py3-pinterest/issues/147) | How to create video pins? | ✅ Fixed |
| [#139](https://github.com/bstoilov/py3-pinterest/issues/139) | `data/` directory automatic removal | ✅ Fixed |
| [#138](https://github.com/bstoilov/py3-pinterest/issues/138) | KeyError `resources` in `load_pin` | ✅ Fixed |
| [#137](https://github.com/bstoilov/py3-pinterest/issues/137) | Pin from local file not working | ✅ Fixed |
| [#136](https://github.com/bstoilov/py3-pinterest/issues/136) | Pin and delete function not working | ✅ Fixed |
| [#130](https://github.com/bstoilov/py3-pinterest/issues/130) | Story pin creation | ✅ Fixed |
| [#108](https://github.com/bstoilov/py3-pinterest/issues/108) | Login broken (API updates) | ✅ Fixed |

</details>

---

## 📦 Installation

```bash
pip install py3-pinterest
```

**Requirements:** Python 3.8+ &nbsp;·&nbsp; Google Chrome (for login only)

---

## ⚡ Quick Start

```python
from py3pin.Pinterest import Pinterest

pinterest = Pinterest(
    email='you@email.com',
    password='your_password',
    username='your_username',
    cred_root='cred_root'       # cookies stored here, created automatically
)

# Login once — cookies are saved and reused automatically (~15 days)
pinterest.login()

# Pin an image
pinterest.pin(
    board_id='123456789',
    image_url='https://example.com/image.jpg',
    title='My Pin',
    description='Pinned with py3-pinterest'
)
```

---

## 🎬 Upload Pins

### Image from local file

```python
pinterest.upload_pin(
    board_id='123456789',
    image_file='photo.jpg',
    title='My Pin',
    description='Uploaded with py3-pinterest',
    link='https://example.com'
)
```

### Video pin ✨

```python
pinterest.upload_video_pin(
    board_id='123456789',
    video_file='video.mov',
    title='My Video Pin',
    description='Video uploaded with py3-pinterest',
    link='https://example.com'
)
```

> 💡 Requires `ffmpeg` and `ffprobe` on PATH. Or provide `duration_ms`, `width`, `height`, and `cover_image_file` manually to skip the dependency.

### Pin from URL

```python
pinterest.pin(
    board_id='123456789',
    image_url='https://example.com/image.jpg',
    title='Pin Title',
    description='Pin description'
)
```

### Repin

```python
pinterest.repin(board_id='board_id', pin_id='pin_id')
```

---

## 📌 Pin Management

```python
pinterest.load_pin(pin_id='pin_id')         # Get full pin data
pinterest.delete_pin(pin_id='pin_id')        # Delete a pin
pinterest.get_pinnable_images(url='...')      # Get pinnable images from any website
```

---

## 📋 Boards

```python
# List boards
boards = pinterest.boards(username='someone')          # One page
boards = pinterest.boards_all(username='someone')       # All boards

# Create & delete
pinterest.create_board(name='My Board', description='A new board')
pinterest.delete_board(board_id='board_id')

# Board feed — all pins in a board
pins = pinterest.board_feed(board_id='board_id', reset_bookmark=True)

# Recommendations ("More ideas")
recs = pinterest.board_recommendations(board_id='board_id', reset_bookmark=True)
```

### Board Sections

```python
pinterest.create_board_section(board_id='board_id', section_name='My Section')
pinterest.delete_board_section(section_id='section_id')
pinterest.get_board_sections(board_id='board_id')       # Supports page_size up to 100
pinterest.get_section_pins(section_id='section_id')

# Pin directly to a section
pinterest.pin(board_id='board_id', section_id='section_id', image_url='...')
pinterest.upload_pin(board_id='board_id', section_id='section_id', image_file='...')
```

---

## 👤 Users

```python
pinterest.get_user_overview(username='someone')
pinterest.get_user_pins(username='someone', reset_bookmark=True)
```

---

## 👥 Follow / Unfollow

```python
# Users
pinterest.follow_user(user_id='user_id')
pinterest.unfollow_user(user_id='user_id')

# Boards
pinterest.follow_board(board_id='board_id')
pinterest.unfollow_board(board_id='board_id')

# Get following & followers (batched)
following = pinterest.get_following(username='someone', reset_bookmark=True)
followers = pinterest.get_user_followers(username='someone', reset_bookmark=True)

# Get all at once
all_following = pinterest.get_following_all(username='someone')
all_followers = pinterest.get_user_followers_all(username='someone')
```

---

## 🔍 Search

```python
# Scopes: pins, buyable_pins, my_pins, videos, boards
results = pinterest.search(scope='pins', query='home decor', reset_bookmark=True)
```

### Visual Search

```python
pin_data = pinterest.load_pin(pin_id='pin_id')
results = pinterest.visual_search(pin_data, x=10, y=50, w=100, h=100)
```

### Type-ahead

```python
pinterest.type_ahead(term='apple')
```

---

## 💬 Comments

```python
pinterest.comment(pin_id='pin_id', text='Nice pin!')
pinterest.delete_comment(pin_id='pin_id', comment_id='comment_id')
pinterest.get_comments(pin_id='pin_id', reset_bookmark=True)
```

---

## ✉️ Messages

```python
conversations = pinterest.get_conversations()
messages = pinterest.load_conversation(conversation_id='conv_id')

# Send text, pin, or both
pinterest.send_message(conversation_id='conv_id', message='Hey!')
pinterest.send_message(conversation_id='conv_id', pin_id='pin_id')
pinterest.send_message(conversation_id='conv_id', pin_id='pin_id', message='Check this out')
```

---

## 🏠 Home Feed

```python
pins = pinterest.home_feed(reset_bookmark=True)
```

---

## 📖 Pagination

Most list methods are **batched** — they return one page per call. Loop until empty:

```python
all_pins = []
batch = pinterest.board_feed(board_id='board_id', reset_bookmark=True)
while batch:
    all_pins += batch
    batch = pinterest.board_feed(board_id='board_id')

print(f'Total: {len(all_pins)} pins')
```

> Always pass `reset_bookmark=True` on the first call to start fresh.

---

## 🌐 Proxy Support

```python
proxies = {"http": "http://user:pass@proxy_ip:port"}
pinterest = Pinterest(
    email='...', password='...', username='...',
    cred_root='cred_root', proxies=proxies
)

pinterest.login(proxy='ip:port')
```

---

## 🔐 Login & Session

```python
pinterest.login()                           # Headless Chrome
pinterest.login(headless=False)             # Visible browser (for debugging)
pinterest.login(proxy='ip:port')            # Through a proxy
pinterest.login(lang='en')                  # Set browser language
pinterest.logout()
```

Cookies persist to disk and are reused across runs. Re-login when you start seeing 401/403 errors (~every 15 days).

---

## 🧩 Working with Responses

All methods return the raw Pinterest response:

```python
resp = pinterest.upload_pin(board_id='...', image_file='photo.jpg', title='Test')
data = resp.json()

pin_id = data["resource_response"]["data"]["id"]
board_id = data["resource_response"]["data"]["board"]["id"]
```

---

## 📂 Examples

Full working examples in the [`Examples/`](Examples/) directory:

| File | Description |
|:-----|:------------|
| [`examples.py`](Examples/examples.py) | 🗂️ Comprehensive overview of all features |
| [`upload_examples.py`](Examples/upload_examples.py) | 📤 Image and video upload |
| [`board_sections_example.py`](Examples/board_sections_example.py) | 📂 Board sections and section pins |
| [`download_board_images.py`](Examples/download_board_images.py) | ⬇️ Download all images from boards |
| [`follow_examples.py`](Examples/follow_examples.py) | 👥 Search, follow users and boards |
| [`mass_board_invites.py`](Examples/mass_board_invites.py) | 📨 Bulk board invites from search |
| [`messages_example.py`](Examples/messages_example.py) | ✉️ Conversations and messaging |
| [`get_board_followers.py`](Examples/get_board_followers.py) | 👤 Get board followers |

---

## 🤝 Contributing

Found a bug or want to add a feature? [Open an issue](https://github.com/bstoilov/py3-pinterest/issues) or submit a PR.

Thanks to all contributors:
@alglez, @anonymustard, @Ashad001, @bahrmichaelj, @CapofWeird, @edersonff, @elmissouri16, @erenalpt, @evezus, @fratamico, @Gmanicus, @imgVOID, @kruvatz, @magicaltoast, @marcosfelt, @mfhassan22, @Nviard, @RKuttruff, @VeemPees, @victorviro, @vladradishevsky, @vriadlee, @vtni, @yaonur

## 📚 Community Guides

- [Get started with Pinterest automation](https://martechwithme.com/how-to-automate-pinterest-interactions-python) — MarTechWithMe
- [Automated posting to Pinterest (Russian)](https://www.youtube.com/watch?v=TQBceIiv_Gk) — Analitiq YouTube

---

<p align="center">
  <b>MIT License</b> · Made with ❤️ by <a href="https://github.com/bstoilov">@bstoilov</a>
</p>
