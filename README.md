# py3-pinterest
Unofficial Pinterest API implemented in python 3 that can do almost all pinterest tasks like comment, pin, repin, follow, unfollow and more.
It is implemented by directly calling the pinterest servers, mimicking an actual browser, so you don't need pinterest API key.

If you see any issues, or find bugs feel free to report them here on the github repo.


## Install using pip
```pip install py3-pinterest```

## Functionalities

### For working code examples see examples.py

### Create new instance of the API

```pinterest = Pinterest(email='your email goes here', password='password goes here', username='look in pinterest url', cred_root='cred root dir')```

cred_root is the dir (automatically created if missing) that will store some cookies nad sessions, so you don't need to login before each request.
Make sure you specify a path with read/write persmissions.

### Login
```pinterest.login()```

Logs you in and stores the cookies needed for further requests. Pinterest session have several hours before they expire, if inacitve.
If you keep making requests you will keep the session alive and you might not need to login, if you receive unauthorized error on api call, then you need to call this method.
Keep in mind that too much login request might lock your account.

### Load profile
```user_overview = pinterest.get_user_overview()```


### Get boards
```board_batch = pinterest.boards(username='username')```

If username is left blank, current logged in user will be used.

### Get board pins
```board_batch = pinterest.boards()```

### Delete pin
```pinterest.delete_pin(pin_id='pin_id')```

If there is no such pin 404 Not found is thrown
If you don't have permissions to delete is 403 Forbidden is thrown.

### Follow
```pinterest.follow_user(user_id='target_user_id', username='target_username')```

Follow limit is 300 per day, after that they might place you on watch list


### Unfollow

```pinterest.unfollow_user(user_id='target_user_id', username='target_username')```

Unfollow limit is 350 per day, after that they might place you on watch list

### Get following

```following_batch = pinterest.get_following(username='some_user')```

If username is not provided current user will be used

### Get followers

```followers_batch=pinterest.get_user_followers(username='some_user')```

If username is not provided current user will be used

### Get home feed pins

``` home_feed_batch = pinterest.home_feed()```

### Get board recommendations (this is the 'more ideas' api)

```rec_batch = pinterest.board_recommendations(board_url=board_url, board_id=board_id)```

### Repin

```pinterest.repin(board_id='board_id', pin_id='pin_id')```

### Get pinnable images

```pinterest.get_pinnable_images(url='https://www.tumblr.com/search/food')```

### Pin

```pinterest.pin(board_id=board_id, image_url=image_url, description=description, title=title)```

### Search

```search_batch = pinterest.search(scope='boards', query='food')```

Current pinterest scopes are: pins, buyable_pins, my_pins, videos, users, boards

### Follow board

```pinterest.follow_board(board_url=board_url, board_id=board_id)```

### Unfollow board

```pinterest.unfollow_board(board_url=board_url, board_id=board_id)```

### Invite to board

```pinterest.invite(board_id=board_id, board_url=board_url, user_id=target_user_id)```

### Delete board invite

```pinterest.delete_invite(board_id=board_id, board_url=board_url, invited_user_id=target_user_id)```

### Get board invites

```invites_batch = pinterest.get_board_invites(board_url=board_url, board_id=board_id)```

### Comment

```pinterest.comment(pin_id=pin_id, text=comment_text)```

### Delete comment 
```pinterest.delete_comment(pin_id=pin_id, comment_id=comment_id)```

### Get Pin comments

```pinterest.get_comments(pin_id='pin_id')```

### Get pin by id

```pinterest.load_pin(pin_id='pin_id')```




