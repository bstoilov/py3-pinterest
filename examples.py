from py3pin.Pinterest import Pinterest

username = 'username'
password = 'password'
email = 'email'
# cred_root is the place the user sessions and cookies will be stored you should specify this to avoid permission issues
cred_root = 'cred_root'

pinterest = Pinterest(email=email,
                      password=password,
                      username=username,
                      cred_root=cred_root)


def get_user_profile():
    return pinterest.get_user_overview(username='username')


def get_user_boards():
    # load specific user boards
    # board_batch = pinterest.boards(username='username')

    # load current user boards
    boards = []
    board_batch = pinterest.boards()
    while len(board_batch) > 0:
        boards += board_batch
        board_batch = pinterest.boards()

    return boards


def get_board_pins():
    board_id = 'board_id'
    board_url = 'board_url'
    board_feed = []
    feed_batch = pinterest.board_feed(board_id=board_id, board_url=board_url)
    while len(feed_batch) > 0:
        board_feed += feed_batch
        feed_batch = pinterest.board_feed(board_id=board_id, board_url=board_url)

    return board_feed


def delete_pin():
    # if pin doesn't exist or you have no rights to delete http 404 or 401 will be thrown
    return pinterest.delete_pin(pin_id='pin_id')


def follow():
    # even if you already follow this user a successful message is returned
    return pinterest.follow_user(user_id='user_id', username='username')


def unfollow():
    # even if you don't follow this user a successful message is returned
    return pinterest.unfollow_user(user_id='user_id', username='username')


def get_following():
    # you can get following on any user, default is current user
    # pinterest.get_following(username='some_user')

    following = []
    following_batch = pinterest.get_following()
    while len(following_batch) > 0:
        following += following_batch
        following_batch = pinterest.get_following()
    return following


def get_followers():
    # you can get followers on any user, default is current user
    # pinterest.get_user_followers(username='some_user')
    username = 'username'

    followers = []
    followers_batch = pinterest.get_user_followers(username=username)
    while len(followers_batch) > 0:
        followers += followers_batch
        followers_batch = pinterest.get_user_followers(username=username)
    return followers


def get_home_feed():
    # This is what pinterest displays on your home page
    # useful for auto repins
    max_length = 100
    home_feed_pins = []
    home_feed_batch = pinterest.home_feed()
    while len(home_feed_batch) > 0:
        home_feed_pins += home_feed_batch
        home_feed_batch = pinterest.home_feed()
        if len(home_feed_pins) > max_length:
            break
    return home_feed_pins


def repin():
    pin_id = 'pin_id'
    board_id = 'board_id'
    return pinterest.repin(board_id=board_id, pin_id=pin_id)


def get_website_pinnable_images():
    # Pinterest endpoint that gives all images on website
    return pinterest.get_pinnable_images(url='https://www.tumblr.com/search/food')


def get_board_pin_recommendations():
    # Recommended pins for board
    board_url = 'board_url'
    board_id = 'board_id'
    max_len = 100
    rec_pins = []
    rec_batch = pinterest.board_recommendations(board_url=board_url, board_id=board_id)
    while len(rec_batch) > 0:
        rec_pins += rec_batch
        if len(rec_pins) > max_len:
            break

    return rec_pins


def pin():
    board_id = 'board_id'
    image_url = 'image url'
    description = 'this is auto pin'
    title = 'a bot did this'
    link = 'https://www.google.com/'
    return pinterest.pin(board_id=board_id, image_url=image_url, description=description, title=title, link=link)


def delete_pin():
    pin_id = 'some pin id'
    return pinterest.delete_pin(pin_id=pin_id)


def search():
    # After change in pinterest API, you can no longer search for users
    # Instead you need to search for something else and extract the user data from there.
    # current pinterest scopes are: pins, buyable_pins, my_pins, videos, boards
    results = []
    max_results = 100
    search_batch = pinterest.search(scope='boards', query='food')
    while len(search_batch) > 0:
        results += search_batch
        if len(results) > max_results:
            break

    return results


def follow_board():
    board_url = 'board_url'
    board_id = 'board_id'
    return pinterest.follow_board(board_url=board_url, board_id=board_id)


def unfollow_board():
    board_url = 'board_url'
    board_id = 'board_id'
    return pinterest.unfollow_board(board_url=board_url, board_id=board_id)


def invite():
    # If user is already invited to the board, you get 403 error.
    board_url = 'board_url'
    board_id = 'board_id'
    target_user_id = 'user_id'
    return pinterest.invite(board_id=board_id, board_url=board_url, user_id=target_user_id)


def delete_invite():
    # If user is not invited to the board, you get 403 error.
    board_url = 'board_url'
    board_id = 'board_id'
    target_user_id = 'user_id'
    return pinterest.delete_invite(board_id=board_id, board_url=board_url, invited_user_id=target_user_id)


def get_board_invites():
    board_url = 'board_url'
    board_id = 'board_id'
    invites = []
    invites_batch = pinterest.get_board_invites(board_url=board_url, board_id=board_id)
    while len(invites_batch) > 0:
        invites += invites_batch
    return invites


def comment_on_pin():
    # Forbidden and not found are thrown if you don't have permissions or comment does not exist
    pin_id = 'pin_id'
    comment_text = 'spammy comment'
    return pinterest.comment(pin_id=pin_id, text=comment_text)


def delete_comment():
    # Forbidden and not found are thrown if you don't have permissions or comment does not exist
    pin_id = 'pin_id'
    comment_id = 'comment_id'
    return pinterest.delete_comment(pin_id=pin_id, comment_id=comment_id)


def get_pin_comments():
    return pinterest.get_comments(pin_id='pin_id')


def load_pin_by_id():
    return pinterest.load_pin(pin_id='pin_id')
