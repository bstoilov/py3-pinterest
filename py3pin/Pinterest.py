import json
import os
import requests
import requests.cookies
from requests.structures import CaseInsensitiveDict
from py3pin.Registry import Registry
from py3pin.RequestBuilder import RequestBuilder
from bs4 import BeautifulSoup
from py3pin.BookmarkManager import BookmarkManager

AGENT_STRING = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) " \
               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"

# Pinterest endpoints
HOME_PAGE = 'https://www.pinterest.com/'
LOGIN_PAGE = 'https://www.pinterest.com/login/?referrer=home_page'
CREATE_USER_SESSION = 'https://www.pinterest.com/resource/UserSessionResource/create/'
USER_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/UserResource/get'
BOARD_PICKER_RESOURCE = 'https://www.pinterest.com/resource/BoardPickerBoardsResource/get'
BOARDS_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/BoardsResource/get'
CREATE_BOARD_RESOURCE = 'https://www.pinterest.com/resource/BoardResource/create/'
FOLLOW_BOARD_RESOURCE = 'https://www.pinterest.com/resource/BoardFollowResource/create/'
UNFOLLOW_BOARD_RESOURCE = 'https://www.pinterest.com/resource/BoardFollowResource/delete/'
FOLLOW_USER_RESOURCE = 'https://www.pinterest.com/resource/UserFollowResource/create/'
UNFOLLOW_USER_RESOURCE = 'https://www.pinterest.com/resource/UserFollowResource/delete/'
USER_FOLLOWING_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/UserFollowingResource/get'
USER_FOLLOWERS_RESOURCE = 'https://www.pinterest.com/resource/UserFollowersResource/get'
PIN_RESOURCE_CREATE = 'https://www.pinterest.com/resource/PinResource/create/'
REPIN_RESOURCE_CREATE = 'https://www.pinterest.com/resource/RepinResource/create/'
PIN_LIKE_RESOURCE = 'https://www.pinterest.com/resource/PinLikeResource/create/'
PIN_UNLIKE_RESOURCE = 'https://www.pinterest.com/resource/PinLikeResource/delete/'
DELETE_PIN_RESOURCE = 'https://www.pinterest.com/resource/PinResource/delete/'
PIN_COMMENT_RESOURCE = 'https://www.pinterest.com/resource/PinCommentResource/create/'
BOARD_INVITE_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/BoardInviteResource/create/'
BOARD_DELETE_INVITE_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/BoardCollaboratorResource/delete/'
SEARCH_RESOURCE = 'https://www.pinterest.com/resource/SearchResource/get'
BOARD_RECOMMEND_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/BoardContentRecommendationResource/get'
PINNABLE_IMAGES_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/FindPinImagesResource/get'
BOARD_FEED_RESOURCE = 'https://www.pinterest.com/resource/BoardFeedResource/get'
USER_HOME_FEED_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/UserHomefeedResource/get'
BASE_SEARCH_RESOURCE = 'https://www.pinterest.com/resource/BaseSearchResource/get'
BOARD_INVITES_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/BoardInvitesResource/get'
CREATE_COMMENT_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/AggregatedCommentResource/create/'
GET_PIN_COMMENTS_RESOURCE = 'https://www.pinterest.com/_ngjs/resource/AggregatedCommentFeedResource/get'
LOAD_PIN_URL_FORMAT = 'https://www.pinterest.com/pin/{}/'
DELETE_COMMENT = 'https://www.pinterest.com/_ngjs/resource/AggregatedCommentResource/delete/'


class Pinterest:

    def __init__(self, password='', proxies=None, username='', email='', cred_root='data'):
        self.pin_cache = {}
        self.email = email
        self.username = username
        self.password = password
        self.req_builder = RequestBuilder()
        self.bookmark_manager = BookmarkManager()

        self.http = requests.session()
        self.proxies = proxies
        self.data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), cred_root,
                                      self.email) + os.sep
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        self.registry = Registry('%sregistry.dat' % self.data_path)
        self.old_cookies = self.registry.get(Registry.Key.COOKIES)
        if self.old_cookies:
            self.http.cookies.update(self.old_cookies)

        self.login_failed = False

    def request(self, method, url, data=None, files=None):
        headers = CaseInsensitiveDict([
            ('Accept', 'text/html,image/webp,image/apng,*/*;q=0.8'),
            ('Accept-Encoding', 'gzip, deflate'),
            ('Accept-Language', 'en-US,en;q=0.8'),
            ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
            ('Cache-Control', 'no-cache'),
            ('Connection', 'keep-alive'),
            ('Host', 'www.pinterest.com'),
            ('Origin', 'https://www.pinterest.com'),
            ('Referer', HOME_PAGE),
            ('X-Requested-With', 'XMLHttpRequest'),
            ('Accept', 'application/json'),
            ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
            ('User-Agent', AGENT_STRING)])
        csrftoken = self.http.cookies.get('csrftoken')
        if csrftoken:
            headers.update([('X-CSRFToken', csrftoken)])

        response = self.http.request(method, url, data=data, headers=headers, files=files, proxies=self.proxies)
        if response.status_code == 401:
            self.login()
            response = self.http.request(method, url, data=data, headers=headers, files=files, proxies=self.proxies)

        response.raise_for_status()
        self.registry.update(Registry.Key.COOKIES, response.cookies)
        return response

    def get(self, url):
        return self.request('GET', url=url)

    def post(self, url, data=None, files=None):
        return self.request('POST', url=url, data=data, files=files)

    def login(self):
        if self.login_failed:
            raise Exception("Wrong credentials")
        self.get(HOME_PAGE)
        self.get(LOGIN_PAGE)
        options = {'username_or_email': self.email, 'password': self.password}
        source_url = '/login/?referrer=home_page'
        data = self.req_builder.buildPost(options=options, source_url=source_url)

        response = {}
        try:
            response = self.post(url=CREATE_USER_SESSION, data=data)
            response = response.json()
        except Exception as e:
            self.login_failed = True
            raise Exception("Wrong credentials")
        return response

    def get_user_overview(self, username=None):
        if username is None:
            username = self.username

        options = {"isPrefetch": 'false', "username": username, "field_set_key": "profile"}
        url = self.req_builder.buildGet(url=USER_RESOURCE, options=options, source_url='/')
        result = self.get(url=url).json()

        result = result['resource_response']['data']

        user_data = {
            'last_name': result['last_name'],
            'following_count': result['following_count'],
            'full_name': result['full_name'],
            'id': result['id'],
            'first_name': result['first_name'],
            'domain_url': result['domain_url'],
            'followed_by_me': result['explicitly_followed_by_me'],
            'website_url': result['website_url'],
            'board_count': result['board_count'],
            'username': result['username'],
            'follower_count': result['follower_count'],
            'pin_count': result['pin_count'],
            'avatar': result['image_large_url']
        }
        return user_data

    def boards(self, username=None, page_size=50):
        if username is None:
            username = self.username

        next_bookmark = self.bookmark_manager.get_bookmark(primary='boards', secondary=username)
        options = {
            "page_size": page_size,
            "privacy_filter": "all",
            "sort": "custom",
            "username": username,
            "isPrefetch": False,
            "include_archived": True,
            "field_set_key": "profile_grid_item",
            "group_by": "visibility",
            "redux_normalize_feed": True,
            "bookmarks": [next_bookmark]
        }

        url = self.req_builder.buildGet(url=BOARDS_RESOURCE, options=options, source_url='/cocococoho/boards/')
        result = self.get(url=url).json()
        bookmark = result['resource']['options']['bookmarks'][0]

        self.bookmark_manager.add_bookmark(primary='boards', secondary=username, bookmark=bookmark)
        boards = []
        for board in result['resource_response']['data']:
            boards.append({
                'id': board['id'],
                'name': board['name'],
                'url': board['url'],
                'description': board['description'],
                'pin_count': board['pin_count'],
                'privacy': board['privacy']
            })
        return boards

    def create_board(self, name, description='', category='other', privacy='public', layout='default'):
        options = {
            "name": name,
            "description": description,
            "category": category,
            "privacy": privacy,
            "layout": layout,
            "collab_board_email": 'true',
            "collaborator_invites_enabled": 'true'
        }

        source_url = '/{}/boards/'.format(self.email)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        r = self.post(url=CREATE_BOARD_RESOURCE, data=data)
        result = r.json()
        if result['resource_response']['error'] is None:
            board = result['resource_response']['data']
            return board
        return None

    def follow_board(self, board_id, board_url):
        options = {"board_id": board_id}
        data = self.req_builder.buildPost(options=options, source_url=board_url)
        return self.post(url=FOLLOW_BOARD_RESOURCE, data=data).json()

    def unfollow_board(self, board_id, board_url):
        options = {"board_id": board_id}
        data = self.req_builder.buildPost(options=options, source_url=board_url)
        return self.post(url=UNFOLLOW_BOARD_RESOURCE, data=data).json()

    def follow_user(self, user_id, username):
        options = {"user_id": user_id}
        source_url = '/{}/'.format(username)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        return self.post(url=FOLLOW_USER_RESOURCE, data=data).json()

    def unfollow_user(self, user_id, username):
        options = {"user_id": user_id}
        source_url = '/{}/'.format(username)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        return self.post(url=UNFOLLOW_USER_RESOURCE, data=data).json()

    def get_following(self, username=None, page_size=250):
        if username is None:
            username = self.username

        next_bookmark = self.bookmark_manager.get_bookmark(primary='following', secondary=username)
        if next_bookmark == '-end-':
            return []

        source_url = '/{}/_following/'.format(self.email)
        options = {
            'isPrefetch': 'false',
            'hide_find_friends_rep': 'false',
            'username': username,
            'page_size': page_size,
            'bookmarks': [next_bookmark]
        }

        url = self.req_builder.buildGet(url=USER_FOLLOWING_RESOURCE, options=options, source_url=source_url)

        result = self.get(url=url).json()
        result = result['resource_response']

        bookmark = '-end-'
        if 'bookmark' in result:
            bookmark = result['bookmark']

        self.bookmark_manager.add_bookmark(primary='following', secondary=username, bookmark=bookmark)

        following = []
        for f in result['data']:
            entry = {
                'username': f['username'],
                'id': f['id'],
                'follower_count': f['follower_count'],
                'board_count': f['board_count']
            }
            following.append(entry)
        return following

    def get_user_followers(self, username=None, page_size=250):
        if username is None:
            username = self.username

        next_bookmark = self.bookmark_manager.get_bookmark(primary='followers', secondary=username)
        if next_bookmark is '-end-':
            return []
        options = {
            'isPrefetch': False,
            'hide_find_friends_rep': True,
            'username': username,
            'page_size': page_size,
            'bookmarks': [next_bookmark]
        }
        source_url = '/{}/_followers/'.format(self.username)

        url = self.req_builder.buildGet(url=USER_FOLLOWERS_RESOURCE, options=options, source_url=source_url)
        result = self.get(url=url).json()
        result = result['resource_response']

        bookmark = '-end-'

        if 'bookmark' in result:
            bookmark = result['bookmark']

        self.bookmark_manager.add_bookmark(primary='followers', secondary=username, bookmark=bookmark)

        followers = []
        for f in result['data']:
            entry = {
                'username': f['username'],
                'id': f['id'],
                'follower_count': f['follower_count'],
                'board_count': f['board_count'],
                'followed_by_me': f['explicitly_followed_by_me'],
                'followers': f['follower_count']
            }
            followers.append(entry)

        return followers

    def pin(self, board_id, image_url, description='', link='', title=''):
        options = {
            "board_id": board_id,
            "image_url": image_url,
            "description": description,
            "link": link if link else image_url,
            "scrape_metric": {"source": "www_url_scrape"},
            "method": "scraped",
            "title": title
        }
        source_url = '/pin/find/?url={}'.format(self.req_builder.url_encode(image_url))
        data = self.req_builder.buildPost(options=options, source_url=source_url)

        return self.post(url=PIN_RESOURCE_CREATE, data=data).json()

    def repin(self, board_id, pin_id):
        options = {
            "board_id": board_id,
            "pin_id": pin_id,
            "is_buyable_pin": False
        }
        source_url = '/pin/{}/'.format(pin_id)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        return self.post(url=REPIN_RESOURCE_CREATE, data=data).json()

    def delete_pin(self, pin_id):
        options = {"id": pin_id}
        source_url = '/{}/'.format(self.username)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        return self.post(url=DELETE_PIN_RESOURCE, data=data).json()

    def comment(self, pin_id, text):
        pin_data = self.load_pin(pin_id=pin_id)
        options = {
            "objectId": pin_data['aggregated_pin_data']['id'],
            "pinId": pin_id,
            "tags": "[]",
            "text": text
        }
        data = self.req_builder.buildPost(options=options, source_url=pin_id)

        return self.post(url=CREATE_COMMENT_RESOURCE, data=data)

    def load_pin(self, pin_id):
        url = LOAD_PIN_URL_FORMAT.format(pin_id)
        resp = self.get(url=url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        scripts = soup.findAll('script')
        pin_data = {}
        for s in scripts:
            if 'pins' in s.text and 'aggregated_pin_data' in s.text:
                pin_data = json.loads(s.text)

        pin_data = pin_data['pins'][pin_id]
        return pin_data

    def get_comments(self, pin_id, page_size=50):
        if pin_id not in self.pin_cache:
            pin_data = self.load_pin(pin_id=pin_id)
            self.pin_cache[pin_id] = pin_data
        else:
            pin_data = self.pin_cache[pin_id]

        next_bookmark = self.bookmark_manager.get_bookmark(primary='pin_comments', secondary=pin_id)
        options = {
            "isPrefetch": False,
            "objectId": pin_data['aggregated_pin_data']['id'],
            "page_size": page_size,
            "redux_normalize_feed": True,
            "bookmarks": [next_bookmark]
        }
        source_url = '/pin/{}/'.format(pin_id)
        url = self.req_builder.buildGet(url=GET_PIN_COMMENTS_RESOURCE, options=options, source_url=source_url)
        resp = self.get(url=url).json()
        resp = resp['resource_response']

        bookmark = '-end-'
        if 'bookmark' in resp:
            bookmark = resp['bookmark']

        self.bookmark_manager.add_bookmark(primary='pin_comments', secondary=pin_id, bookmark=bookmark)

        comments = []
        for r in resp['data']:
            comments.append({
                'created_at': r['created_at'],
                'user': {
                    'username': r['user']['username'],
                    'id': r['user']['id']
                },
                'text': r['text'],
                'id': r['id']

            })
        return comments

    def delete_comment(self, pin_id, comment_id):
        options = {"commentId": comment_id}
        source_url = "/pin/{}/".format(pin_id)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        return self.post(url=DELETE_COMMENT, data=data).json()

    def invite(self, board_id, board_url, user_id):
        options = {"board_id": board_id, "invited_user_ids": [user_id]}
        data = self.req_builder.buildPost(options=options, source_url=board_url)
        return self.post(url=BOARD_INVITE_RESOURCE, data=data).json()

    def get_board_invites(self, board_id, board_url, page_size=100):
        options = {
            "isPrefetch": False,
            "board_id": board_id,
            "sort": "viewer_first",
            "field_set_key": "boardEdit",
            "status_filters": "new,accepted,contact_request_not_approved,pending_approval",
            "include_inactive": True,
            "page_size": page_size
        }
        url = self.req_builder.buildGet(url=BOARD_INVITES_RESOURCE, options=options, source_url=board_url)
        resp = self.get(url=url).json()
        data = resp['resource_response']['data']

        invites = []
        for inv in data:
            invites.append({
                'status': inv['status'],
                'invited_by': {
                    'username': inv['invited_by_user']['username'],
                    'id': '547539404604880944'
                },
                'invited_user': {
                    'username': inv['invited_user']['username'],
                    'id': inv['invited_user']['id']
                }
            })
        return invites

    def delete_invite(self, board_id, board_url, invited_user_id, also_block=False):
        options = {
            "ban": also_block,
            "board_id": board_id,
            "field_set_key": "boardEdit",
            "invited_user_id": invited_user_id
        }
        data = self.req_builder.buildPost(options=options, source_url=board_url)
        return self.post(url=BOARD_DELETE_INVITE_RESOURCE, data=data).json()

    def search(self, scope, query, page_size=250):

        next_bookmark = self.bookmark_manager.get_bookmark(primary='search', secondary=query)
        if next_bookmark == '-end-':
            return []

        terms = query.split(' ')
        query = "%20".join(terms)
        term_meta_arr = []
        for t in terms:
            term_meta_arr.append('term_meta[]=' + t)
        term_arg = "%7Ctyped&".join(term_meta_arr)
        source_url = '/search/{}/?q={}&rs=typed&{}%7Ctyped'.format(scope, query, term_arg)
        options = {
            "isPrefetch": False,
            "auto_correction_disabled": False,
            "query": query,
            "redux_normalize_feed": True,
            "rs": "typed",
            "scope": scope,
            "page_size": page_size,
            "bookmarks": [next_bookmark]
        }
        url = self.req_builder.buildGet(url=BASE_SEARCH_RESOURCE, options=options, source_url=source_url)
        resp = self.get(url=url).json()

        bookmark = resp['resource']['options']['bookmarks'][0]
        self.bookmark_manager.add_bookmark(primary='search', secondary=query, bookmark=bookmark)
        return resp['resource_response']['data']['results']

    def board_recommendations(self, board_id='', board_url='', page_size=50):
        next_bookmark = self.bookmark_manager.get_bookmark(primary='boards', secondary=board_id)

        if next_bookmark == '-end-':
            return []

        options = {
            "isPrefetch": False,
            "type": "board",
            "id": board_id,
            "page_size": page_size,
            "bookmarks": [next_bookmark]
        }
        source_url = board_url + '/more_ideas/'
        url = self.req_builder.buildGet(url=BOARD_RECOMMEND_RESOURCE, source_url=source_url, options=options)

        r = self.get(url=url).json()
        bookmark = r['resource']['options']['bookmarks'][0]
        self.bookmark_manager.add_bookmark(primary='boards', secondary=board_id, bookmark=bookmark)

        repin_ideas = []
        data_arr = r['resource_response']['data']
        for data in data_arr:
            if 'repin_count' in data:
                repin_ideas.append({
                    'id': data['id'],
                    'repin_count': data['repin_count'],
                    'description': data['description'],
                    'title': data['grid_title'],
                    'saves': data['aggregated_pin_data']['aggregated_stats']['saves'],
                    'owner_id': data['pinner']['id'],
                    'owner_username': data['pinner']['username']
                })
        return repin_ideas

    def get_pinnable_images(self, url):
        options = {"isPrefetch": 'false',
                   "url": url,
                   "source": "pin_create",
                   "appendItems": 'false',
                   "followRedirects": 'true'
                   }
        url = self.req_builder.buildGet(url=PINNABLE_IMAGES_RESOURCE, source_url='/pin-builder/', options=options)

        r = self.get(url=url).json()
        res = r['resource_response']['data']['items']
        urls = []
        for item in res:
            if 'url' in item:
                urls.append(item['url'])
        return urls

    def home_feed(self, page_size=100):

        next_bookmark = self.bookmark_manager.get_bookmark(primary='home_feed')
        if next_bookmark == '-end-':
            return []

        options = {
            "bookmarks": [next_bookmark],
            "isPrefetch": False,
            "field_set_key": "hf_grid_partner",
            "in_nux": False,
            "prependPartner": True,
            "prependUserNews": False,
            "static_feed": False,
            "page_size": page_size
        }
        source_url = '/'
        url = self.req_builder.buildGet(url=USER_HOME_FEED_RESOURCE, source_url=source_url, options=options)

        response = self.get(url=url).json()

        bookmark = '-end-'

        if 'bookmark' in response['resource_response']:
            bookmark = response['resource_response']['bookmark']

        self.bookmark_manager.add_bookmark(primary='home_feed', bookmark=bookmark)

        feed_items = []

        for p in response['resource_response']['data']:
            if 'pinner' in p:
                item = {
                    'image': p['images']['orig']['url'],
                    'saves': p['aggregated_pin_data']['aggregated_stats']['saves'],
                    'id': p['id'],
                    'pinner': p['pinner'],
                    'title': p['title']
                }
                if 'rich_summary' in p and p['rich_summary'] is not None:
                    item['title'] = p['rich_summary']['display_name']
                feed_items.append(item)

        return feed_items

    def board_feed(self, board_url='', board_id='', page_size=250):
        next_bookmark = self.bookmark_manager.get_bookmark(primary='board_feed', secondary=board_id)

        if next_bookmark == '-end-':
            return []

        options = {
            "isPrefetch": False,
            "board_id": board_id,
            "board_url": board_url,
            "field_set_key": "partner_react_grid_pin",
            "filter_section_pins": True,
            "layout": "default",
            "page_size": page_size,
            "redux_normalize_feed": True,
            "bookmarks": [next_bookmark]
        }

        url = self.req_builder.buildGet(url=BOARD_FEED_RESOURCE, source_url=board_url, options=options)
        response = self.get(url=url).json()
        bookmark = response['resource']['options']['bookmarks'][0]
        self.bookmark_manager.add_bookmark(primary='board_feed', secondary=board_id, bookmark=bookmark)

        pins = []
        for pin in response['resource_response']['data']:
            pin_data = extract_pin(pin)
            if pin_data is not None:
                pins.append(pin_data)
        return pins


def extract_pins(results):
    pins = []
    for result in results:
        if result['type'] == 'pin':
            pins.append(extract_pin(result))
    return pins


def extract_pin(result):
    if 'aggregated_pin_data' not in result:
        return None
    pin_data = {}

    rich_summary = None
    if 'rich_summary' in result and result['rich_summary'] is not None:
        rich_summary = result['rich_summary']

    if rich_summary is not None and 'type_name' in rich_summary:
        pin_data['type'] = result['rich_summary']['type_name']

    if 'description' in result:
        pin_data['description'] = result['description']
    if rich_summary is not None and 'display_description' in rich_summary:
        pin_data['description'] = rich_summary['display_description']

    pin_data['title'] = result['title']
    if not pin_data['title']:
        pin_data['title'] = result['grid_title']

    pin_data['saves'] = 0
    if 'aggregated_pin_data' in result and 'saves' in result['aggregated_pin_data']['aggregated_stats']:
        pin_data['saves'] = result['aggregated_pin_data']['aggregated_stats']['saves']

    if 'is_repin' in result:
        pin_data['is_repin'] = result['is_repin']

    pin_data['id'] = result['id']
    pin_data['image'] = result['images']['orig']['url']
    pin_data['board'] = {
        'name': result['board']['name'],
        'url': result['board']['url'],
    }
    pin_data['pinner'] = {
        'id': result['pinner']['id'],
        'username': result['pinner']['username'],
    }

    return pin_data
