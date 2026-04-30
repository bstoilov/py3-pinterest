from py3pin.Pinterest import Pinterest

pinterest = Pinterest(email='email',
                      password='password',
                      username='username',
                      cred_root='cred_root')

# Proxies example:
# proxies = {"http": "http://username:password@proxy_ip:proxy_port"}
# pinterest = Pinterest(email='email', password='pass', username='name', cred_root='cred_root', proxies=proxies)

# Login obtains and stores cookies for further use, they last around 15 days.
# After the first successful login, cookies are persisted to disk and reused automatically.
# pinterest.login()


# ── User ──────────────────────────────────────────────────────────────

def get_user_profile():
    return pinterest.get_user_overview(username='username')


def get_user_pins_batched(username=None, max_items=500):
    pins = []
    pin_batch = pinterest.get_user_pins(username=username, reset_bookmark=True)
    while len(pin_batch) > 0 and len(pins) < max_items:
        pins += pin_batch
        pin_batch = pinterest.get_user_pins(username=username)
    return pins


# ── Boards ────────────────────────────────────────────────────────────

def get_user_boards_batched(username=None):
    boards = []
    board_batch = pinterest.boards(username=username, reset_bookmark=True)
    while len(board_batch) > 0:
        boards += board_batch
        board_batch = pinterest.boards(username=username)
    return boards


def get_boards(username=None):
    return pinterest.boards_all(username=username)


def create_board(name='', description='', category='other', privacy='public', layout='default'):
    return pinterest.create_board(name=name, description=description, category=category,
                                  privacy=privacy, layout=layout)


def delete_board(board_id=''):
    return pinterest.delete_board(board_id=board_id)


# ── Board Sections ────────────────────────────────────────────────────

def create_board_section(board_id='', section_name=''):
    return pinterest.create_board_section(board_id=board_id, section_name=section_name)


def delete_board_section(section_id=''):
    return pinterest.delete_board_section(section_id=section_id)


def get_board_sections(board_id=''):
    return pinterest.get_board_sections(board_id=board_id, reset_bookmark=True)


def get_board_section_feed(section_id=''):
    return pinterest.get_section_pins(section_id=section_id, reset_bookmark=True)


# ── Board Feed & Recommendations ─────────────────────────────────────

def get_board_pins_batched(board_id=''):
    board_feed = []
    feed_batch = pinterest.board_feed(board_id=board_id, reset_bookmark=True)
    while len(feed_batch) > 0:
        board_feed += feed_batch
        feed_batch = pinterest.board_feed(board_id=board_id)
    return board_feed


def get_board_pin_recommendations(board_id='', max_items=100):
    rec_pins = []
    rec_batch = pinterest.board_recommendations(board_id=board_id, reset_bookmark=True)
    while len(rec_batch) > 0 and len(rec_pins) < max_items:
        rec_pins += rec_batch
        rec_batch = pinterest.board_recommendations(board_id=board_id)
    return rec_pins


# ── Pins ──────────────────────────────────────────────────────────────

def load_pin_by_id(pin_id=''):
    return pinterest.load_pin(pin_id=pin_id)


def pin(board_id='',
        section_id=None,
        image_url='https://i.pinimg.com/170x/32/78/bd/3278bd27073e1ec9c8a708409279768b.jpg',
        description='this is auto pin',
        title='a bot did this',
        alt_text='alt text',
        link='https://www.google.com/'):
    return pinterest.pin(board_id=board_id, section_id=section_id, image_url=image_url,
                         alt_text=alt_text, description=description, title=title, link=link)


def upload_pin(board_id='',
               section_id=None,
               image_path='my_image.png',
               description='this is auto pin',
               title='a bot did this',
               link='https://www.google.com/'):
    return pinterest.upload_pin(board_id=board_id, section_id=section_id, image_file=image_path,
                                description=description, title=title, link=link)


def upload_video(board_id='',
                 video_path='my_video.mov',
                 title='video pin',
                 description='uploaded with py3-pinterest',
                 link='https://www.google.com/'):
    return pinterest.upload_video_pin(board_id=board_id, video_file=video_path,
                                      title=title, description=description, link=link)


def delete_pin(pin_id=''):
    return pinterest.delete_pin(pin_id=pin_id)


def repin(pin_id='', board_id='', section_id=None):
    return pinterest.repin(board_id=board_id, pin_id=pin_id, section_id=section_id)


# ── Comments ──────────────────────────────────────────────────────────

def comment_on_pin(pin_id='', comment_text='comment'):
    return pinterest.comment(pin_id=pin_id, text=comment_text)


def delete_comment(pin_id='', comment_id=''):
    return pinterest.delete_comment(pin_id=pin_id, comment_id=comment_id)


def get_pin_comments(pin_id=''):
    return pinterest.get_comments(pin_id=pin_id, reset_bookmark=True)


# ── Follow / Unfollow ────────────────────────────────────────────────

def follow(user_id=''):
    return pinterest.follow_user(user_id=user_id)


def unfollow(user_id=''):
    return pinterest.unfollow_user(user_id=user_id)


def follow_board(board_id=''):
    return pinterest.follow_board(board_id=board_id)


def unfollow_board(board_id=''):
    return pinterest.unfollow_board(board_id=board_id)


def get_following_batched(username=None, max_items=500):
    following = []
    following_batch = pinterest.get_following(username=username, reset_bookmark=True)
    while len(following_batch) > 0 and len(following) < max_items:
        following += following_batch
        following_batch = pinterest.get_following(username=username)
    return following


def get_following(username=None):
    return pinterest.get_following_all(username=username)


def get_followers_batched(username=None, max_items=500):
    followers = []
    followers_batch = pinterest.get_user_followers(username=username, reset_bookmark=True)
    while len(followers_batch) > 0 and len(followers) < max_items:
        followers += followers_batch
        followers_batch = pinterest.get_user_followers(username=username)
    return followers


def get_followers(username=None):
    return pinterest.get_user_followers_all(username=username)


# ── Home Feed ─────────────────────────────────────────────────────────

def get_home_feed(max_items=100):
    home_feed_pins = []
    home_feed_batch = pinterest.home_feed(reset_bookmark=True)
    while len(home_feed_batch) > 0 and len(home_feed_pins) < max_items:
        home_feed_pins += home_feed_batch
        home_feed_batch = pinterest.home_feed()
    return home_feed_pins


# ── Search ────────────────────────────────────────────────────────────

def search(max_items=100, scope='boards', query='food'):
    results = []
    search_batch = pinterest.search(scope=scope, query=query, reset_bookmark=True)
    while len(search_batch) > 0 and len(results) < max_items:
        results += search_batch
        search_batch = pinterest.search(scope=scope, query=query)
    return results


def visual_search(pin_id=''):
    pin_data = pinterest.load_pin(pin_id=pin_id)
    return pinterest.visual_search(pin_data=pin_data, reset_bookmark=True)


def type_ahead(term="apple"):
    return pinterest.type_ahead(term=term)


def get_website_pinnable_images():
    return pinterest.get_pinnable_images(url='https://www.tumblr.com/search/food')


# ── Invites ───────────────────────────────────────────────────────────

def invite(board_id='', target_user_id=''):
    return pinterest.invite(board_id=board_id, user_id=target_user_id)


def delete_invite(board_id='', target_user_id=''):
    return pinterest.delete_invite(board_id=board_id, invited_user_id=target_user_id)


def get_board_invites(board_id=''):
    return pinterest.get_board_invites(board_id=board_id)


def get_board_invites_all(board_id=''):
    return pinterest.get_board_invites_all(board_id=board_id)


# ── Notes ─────────────────────────────────────────────────────────────

def add_pin_note(pin_id='', note='test note'):
    pinterest.add_pin_note(pin_id=pin_id, note=note)
