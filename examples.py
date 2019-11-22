from py3pin.Pinterest import Pinterest

pinterest = Pinterest(email='email',
                      password='password',
                      username='username',
                      cred_root='cred_root')


# login will obtain and store cookies for further use, they last around 15 days.
# pinterest.login()


def get_user_profile():
    return pinterest.get_user_overview(username='username')


def get_user_boards(username=None):
    boards = []
    board_batch = pinterest.boards(username=username)
    while len(board_batch) > 0:
        boards += board_batch
        board_batch = pinterest.boards(username=username)

    return boards


def get_board_pins(board_id=''):
    board_feed = []
    feed_batch = pinterest.board_feed(board_id=board_id)
    while len(feed_batch) > 0:
        board_feed += feed_batch
        feed_batch = pinterest.board_feed(board_id=board_id)

    return board_feed


def delete_pin(pin_id=''):
    # if pin doesn't exist or you have no rights to delete http 404 or 401 will be thrown
    return pinterest.delete_pin(pin_id=pin_id)


def follow(user_id=''):
    # even if you already follow this user a successful message is returned
    return pinterest.follow_user(user_id=user_id)


def unfollow(user_id=''):
    # even if you don't follow this user a successful message is returned
    return pinterest.unfollow_user(user_id=user_id)


def get_following(username=None, max_items=500):
    # you can get following on any user, default is current user
    # pinterest.get_following(username='some_user')

    following = []
    following_batch = pinterest.get_following(username=username)
    while len(following_batch) > 0 and len(following) < max_items:
        following += following_batch
        following_batch = pinterest.get_following(username=username)

    return following


def get_followers(username=None, max_items=500):
    followers = []
    followers_batch = pinterest.get_user_followers(username=username)
    while len(followers_batch) > 0 and len(followers) < max_items:
        followers += followers_batch
        followers_batch = pinterest.get_user_followers(username=username)

    return followers


def get_home_feed(max_items=100):
    # This is what pinterest displays on your home page
    # useful for auto repins
    home_feed_pins = []
    home_feed_batch = pinterest.home_feed()
    while len(home_feed_batch) > 0 and len(home_feed_pins) < max_items:
        home_feed_pins += home_feed_batch
        home_feed_batch = pinterest.home_feed()

    return home_feed_pins


def repin(pin_id='', board_id='', section_id=None):
    return pinterest.repin(board_id=board_id, pin_id=pin_id, section_id=section_id)


def get_website_pinnable_images():
    # Pinterest endpoint that gives all images on website
    return pinterest.get_pinnable_images(url='https://www.tumblr.com/search/food')


def get_board_pin_recommendations(board_id='', max_items=100):
    rec_pins = []
    rec_batch = pinterest.board_recommendations(board_id=board_id)
    while len(rec_batch) > 0 and len(rec_pins) < max_items:
        rec_pins += rec_batch

    return rec_pins


def pin(board_id='',
        section_id=None,
        image_url='https://i.pinimg.com/170x/32/78/bd/3278bd27073e1ec9c8a708409279768b.jpg',
        description='this is auto pin',
        title='a bot did this',
        link='https://www.google.com/'):
    return pinterest.pin(board_id=board_id, section_id=section_id, image_url=image_url, description=description,
                         title=title, link=link)


def upload_pin(board_id='',
               section_id=None,
               image_path='my_imag.png',
               description='this is auto pin',
               title='a bot did this',
               link='https://www.google.com/'):
    return pinterest.upload_pin(board_id=board_id, section_id=section_id, image_file=image_path,
                                description=description, title=title, link=link)


def search(max_items=100, scope='boards', query='food'):
    # After change in pinterest API, you can no longer search for users
    # Instead you need to search for something else and extract the user data from there.
    # current pinterest scopes are: pins, buyable_pins, my_pins, videos, boards
    results = []
    search_batch = pinterest.search(scope=scope, query=query)
    while len(search_batch) > 0 and len(results) < max_items:
        results += search_batch
        search_batch = pinterest.search(scope=scope, query=query)

    return results


def follow_board(board_id=''):
    return pinterest.follow_board(board_id=board_id)


def unfollow_board(board_id=''):
    return pinterest.unfollow_board(board_id=board_id)


def invite(board_id='', target_user_id=''):
    # If user is already invited to the board, you get 403 error.
    return pinterest.invite(board_id=board_id, user_id=target_user_id)


def delete_invite(board_id='', target_user_id=''):
    # If user is not invited to the board, you get 403 error.
    return pinterest.delete_invite(board_id=board_id, invited_user_id=target_user_id)


def get_board_invites(board_id=''):
    return pinterest.get_board_invites(board_id=board_id)


def comment_on_pin(pin_id='', comment_text='comment'):
    # Forbidden and not found are thrown if you don't have permissions or comment does not exist
    return pinterest.comment(pin_id=pin_id, text=comment_text)


def delete_comment(pin_id='', comment_id=''):
    # Forbidden and not found are thrown if you don't have permissions or comment does not exist
    return pinterest.delete_comment(pin_id=pin_id, comment_id=comment_id)


def get_pin_comments(pin_id=''):
    return pinterest.get_comments(pin_id=pin_id)


def load_pin_by_id(pin_id=''):
    return pinterest.load_pin(pin_id=pin_id)


# to pin/repin to section you just need to provide section id parameter to the respective function
# repin(board_id=board_id, section_id=section_id, pin_id='pin_id')
# pin(board_id=board_id, section_id=section_id)


def create_board_section(board_id='', section_name=''):
    return pinterest.create_board_section(board_id=board_id, section_name=section_name)


def delete_board_section(section_id=''):
    return pinterest.delete_board_section(section_id=section_id)


def get_board_sections(board_id=''):
    return pinterest.get_board_sections(board_id=board_id)


def get_board_section_feed(section_id=''):
    return pinterest.get_section_pins(section_id=section_id)

