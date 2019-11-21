import json
import os

import requests
import mimetypes
import requests.cookies
from requests_toolbelt import MultipartEncoder
from bs4 import BeautifulSoup
from py3pin.BookmarkManager import BookmarkManager
from py3pin.Registry import Registry
from py3pin.RequestBuilder import RequestBuilder
from requests.structures import CaseInsensitiveDict

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
CONVERSATION_RESOURCE = 'https://www.pinterest.com/resource/ConversationsResource/get/'
CONVERSATION_RESOURCE_CREATE = 'https://www.pinterest.com/resource/ConversationsResource/create/'
LOAD_CONVERSATION = 'https://www.pinterest.com/resource/ConversationMessagesResource/get/'
SEND_MESSAGE = 'https://www.pinterest.com/resource/ConversationMessagesResource/create/'
BOARD_SECTION_RESOURCE = 'https://www.pinterest.com/resource/BoardSectionResource/create/'
GET_BOARD_SECTIONS = 'https://www.pinterest.com/resource/BoardSectionsResource/get/'
BOARD_SECTION_EDIT_RESOURCE = 'https://www.pinterest.com/resource/BoardSectionEditResource/delete/'
UPLOAD_IMAGE = 'https://www.pinterest.com/upload-image/'


class Pinterest:

    def __init__(self, password='', proxies=None, username='', email='', cred_root='data'):
        self.email = email
        self.username = username
        self.password = password
        self.req_builder = RequestBuilder()
        self.bookmark_manager = BookmarkManager()
        self.http = requests.session()
        self.proxies = proxies

        data_path = os.path.join(cred_root, self.email) + os.sep
        if not os.path.isdir(data_path):
            os.makedirs(data_path)

        self.registry = Registry('{}registry.dat'.format(data_path))

        cookies = self.registry.get(Registry.Key.COOKIES)
        if cookies is not None:
            self.http.cookies.update(cookies)

    def request(self, method, url, data=None, files=None, extra_headers=None):
        headers = CaseInsensitiveDict([
            ('Referer', HOME_PAGE),
            ('X-Requested-With', 'XMLHttpRequest'),
            ('Accept', 'application/json'),
            ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
            ('User-Agent', AGENT_STRING)])
        csrftoken = self.http.cookies.get('csrftoken')
        if csrftoken:
            headers.update([('X-CSRFToken', csrftoken)])

        if extra_headers is not None:
            for h in extra_headers:
                headers.update([(h, extra_headers[h])])

        response = self.http.request(method, url, data=data, headers=headers, files=files, proxies=self.proxies)
        response.raise_for_status()
        self.registry.update(Registry.Key.COOKIES, response.cookies)
        return response

    def get(self, url):
        return self.request('GET', url=url)

    def post(self, url, data=None, files=None, headers=None):
        return self.request('POST', url=url, data=data, files=files, extra_headers=headers)

    def login(self):
        self.get(HOME_PAGE)
        self.get(LOGIN_PAGE)

        options = {
            'username_or_email': self.email,
            'password': self.password
        }

        data = self.req_builder.buildPost(options=options, source_url='/login/?referrer=home_page')
        return self.post(url=CREATE_USER_SESSION, data=data)

    def get_user_overview(self, username=None):
        if username is None:
            username = self.username

        options = {
            "isPrefetch": 'false',
            "username": username,
            "field_set_key": "profile"
        }
        url = self.req_builder.buildGet(url=USER_RESOURCE, options=options)
        result = self.get(url=url).json()

        return result['resource_response']['data']

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
        source_url = '/{}/boards/'.format(username)
        url = self.req_builder.buildGet(url=BOARDS_RESOURCE, options=options, source_url=source_url)

        result = self.get(url=url).json()
        bookmark = result['resource']['options']['bookmarks'][0]

        self.bookmark_manager.add_bookmark(primary='boards', secondary=username, bookmark=bookmark)
        return result['resource_response']['data']

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
        return self.post(url=CREATE_BOARD_RESOURCE, data=data)

    def follow_board(self, board_id):
        options = {"board_id": board_id}
        data = self.req_builder.buildPost(options=options)
        return self.post(url=FOLLOW_BOARD_RESOURCE, data=data)

    def unfollow_board(self, board_id):
        options = {"board_id": board_id}
        data = self.req_builder.buildPost(options=options)
        return self.post(url=UNFOLLOW_BOARD_RESOURCE, data=data)

    def follow_user(self, user_id):
        options = {"user_id": user_id}
        data = self.req_builder.buildPost(options=options)
        return self.post(url=FOLLOW_USER_RESOURCE, data=data)

    def unfollow_user(self, user_id):
        options = {"user_id": user_id}
        data = self.req_builder.buildPost(options=options)
        return self.post(url=UNFOLLOW_USER_RESOURCE, data=data)

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

        return result['data']

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

        return result['data']

    def pin(self, board_id, image_url, description='', link='', title='', section_id=None):
        options = {
            "board_id": board_id,
            "image_url": image_url,
            "description": description,
            "link": link if link else image_url,
            "scrape_metric": {"source": "www_url_scrape"},
            "method": "scraped",
            "title": title,
            "section": section_id
        }
        source_url = '/pin/find/?url={}'.format(self.req_builder.url_encode(image_url))
        data = self.req_builder.buildPost(options=options, source_url=source_url)

        return self.post(url=PIN_RESOURCE_CREATE, data=data)

    def upload_pin(self, board_id, image_file, description='', link='', title='', section_id=None):
        image_url = self._upload_image(image_file=image_file).json()['image_url']
        return self.pin(board_id=board_id, description=description, image_url=image_url, link=link, title=title,
                 section_id=section_id)

    def repin(self, board_id, pin_id, section_id=None):
        options = {
            "board_id": board_id,
            "pin_id": pin_id,
            "section": section_id,
            "is_buyable_pin": False
        }
        source_url = '/pin/{}/'.format(pin_id)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        return self.post(url=REPIN_RESOURCE_CREATE, data=data)

    def _upload_image(self, image_file):
        file_name = os.path.basename(image_file)
        mime_type = mimetypes.guess_type(image_file)[0]

        form_data = MultipartEncoder(fields={
            'img': ('%s' % file_name, open(image_file, 'rb'), mime_type)
        })

        headers = {
            'Content-Length': '%s' % form_data.len,
            'Content-Type': form_data.content_type,
            'X-UPLOAD-SOURCE': 'pinner_uploader'
        }

        return self.post(url=UPLOAD_IMAGE, data=form_data, headers=headers)

    def delete_pin(self, pin_id):
        options = {"id": pin_id}
        source_url = '/{}/'.format(self.username)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        return self.post(url=DELETE_PIN_RESOURCE, data=data)

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
        resp = self.get(url=LOAD_PIN_URL_FORMAT.format(pin_id))
        soup = BeautifulSoup(resp.text, 'html.parser')
        scripts = soup.findAll('script')
        pin_data = {}
        for s in scripts:
            if 'pins' in s.text and 'aggregated_pin_data' in s.text:
                pin_data = json.loads(s.text)
        return pin_data['resourceResponses'][0]['response']['data']

    def get_comments(self, pin_id, page_size=50):
        pin_data = self.load_pin(pin_id=pin_id)

        next_bookmark = self.bookmark_manager.get_bookmark(primary='pin_comments', secondary=pin_id)

        if next_bookmark == '-end-':
            return []

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

        return resp['data']

    def delete_comment(self, pin_id, comment_id):
        options = {"commentId": comment_id}
        source_url = "/pin/{}/".format(pin_id)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        return self.post(url=DELETE_COMMENT, data=data)

    def invite(self, board_id, user_id):
        options = {"board_id": board_id, "invited_user_ids": [user_id]}
        data = self.req_builder.buildPost(options=options)
        return self.post(url=BOARD_INVITE_RESOURCE, data=data)

    def get_board_invites(self, board_id, page_size=100):
        options = {
            "isPrefetch": False,
            "board_id": board_id,
            "sort": "viewer_first",
            "field_set_key": "boardEdit",
            "status_filters": "new,accepted,contact_request_not_approved,pending_approval",
            "include_inactive": True,
            "page_size": page_size
        }
        url = self.req_builder.buildGet(url=BOARD_INVITES_RESOURCE, options=options)

        resp = self.get(url=url).json()

        return resp['resource_response']['data']

    def delete_invite(self, board_id, invited_user_id, also_block=False):
        options = {
            "ban": also_block,
            "board_id": board_id,
            "field_set_key": "boardEdit",
            "invited_user_id": invited_user_id
        }
        data = self.req_builder.buildPost(options=options)
        return self.post(url=BOARD_DELETE_INVITE_RESOURCE, data=data)

    def search(self, scope, query, page_size=250):

        next_bookmark = self.bookmark_manager.get_bookmark(primary='search', secondary=query)

        if next_bookmark == '-end-':
            return []

        terms = query.split(' ')
        escaped_query = "%20".join(terms)
        term_meta_arr = []
        for t in terms:
            term_meta_arr.append('term_meta[]=' + t)
        term_arg = "%7Ctyped&".join(term_meta_arr)
        source_url = '/search/{}/?q={}&rs=typed&{}%7Ctyped'.format(scope, escaped_query, term_arg)
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

    def board_recommendations(self, board_id='', page_size=50):
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
        url = self.req_builder.buildGet(url=BOARD_RECOMMEND_RESOURCE, options=options)

        response = self.get(url=url).json()
        bookmark = response['resource']['options']['bookmarks'][0]
        self.bookmark_manager.add_bookmark(primary='boards', secondary=board_id, bookmark=bookmark)

        return response['resource_response']['data']

    def get_pinnable_images(self, url):
        options = {"isPrefetch": 'false',
                   "url": url,
                   "source": "pin_create",
                   "appendItems": 'false',
                   "followRedirects": 'true'
                   }
        url = self.req_builder.buildGet(url=PINNABLE_IMAGES_RESOURCE, source_url='/pin-builder/', options=options)

        res = self.get(url=url).json()
        res = res['resource_response']['data']['items']
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
        url = self.req_builder.buildGet(url=USER_HOME_FEED_RESOURCE, options=options)

        response = self.get(url=url).json()

        bookmark = '-end-'

        if 'bookmark' in response['resource_response']:
            bookmark = response['resource_response']['bookmark']

        self.bookmark_manager.add_bookmark(primary='home_feed', bookmark=bookmark)

        return response['resource_response']['data']

    def board_feed(self, board_id='', page_size=250):
        next_bookmark = self.bookmark_manager.get_bookmark(primary='board_feed', secondary=board_id)

        if next_bookmark == '-end-':
            return []

        options = {
            "isPrefetch": False,
            "board_id": board_id,
            "field_set_key": "partner_react_grid_pin",
            "filter_section_pins": True,
            "layout": "default",
            "page_size": page_size,
            "redux_normalize_feed": True,
            "bookmarks": [next_bookmark]
        }

        url = self.req_builder.buildGet(url=BOARD_FEED_RESOURCE, options=options)
        response = self.get(url=url).json()
        bookmark = response['resource']['options']['bookmarks'][0]
        self.bookmark_manager.add_bookmark(primary='board_feed', secondary=board_id, bookmark=bookmark)

        return response['resource_response']['data']

    def initiate_conversation(self, user_ids=None, message='hi'):
        options = {
            "user_ids": user_ids,
            "text": message
        }
        data = self.req_builder.buildPost(options=options)
        return self.post(url=CONVERSATION_RESOURCE_CREATE, data=data)

    def send_message(self, message='', conversation_id='', pin_id=''):
        options = {
            "conversation_id": conversation_id,
            "text": message,
            "pin": pin_id
        }

        data = self.req_builder.buildPost(options=options)
        return self.post(url=SEND_MESSAGE, data=data)

    def load_conversation(self, conversation_id=''):
        messages = []

        message_batch = self._load_conversation_batch(conversation_id=conversation_id)
        while len(message_batch) > 0:
            messages += message_batch
            message_batch = self._load_conversation_batch(conversation_id=conversation_id)

        return messages

    def _load_conversation_batch(self, conversation_id='', page_size=25):
        next_bookmark = self.bookmark_manager.get_bookmark(primary='conversations', secondary=conversation_id)

        if next_bookmark == '-end-':
            return []

        options = {
            "isPrefetch": False,
            "page_size": page_size,
            "conversation_id": conversation_id,
            "bookmarks": [next_bookmark]
        }

        url = self.req_builder.buildGet(url=LOAD_CONVERSATION, options=options)
        response = self.get(url=url).json()

        bookmark = response['resource']['options']['bookmarks'][0]
        self.bookmark_manager.add_bookmark(primary='conversations', secondary=conversation_id, bookmark=bookmark)

        return response['resource_response']['data']

    def get_conversations(self):
        conversations = []
        conv_batch = self._get_conversation_batch()
        while len(conv_batch) > 0:
            conversations += conv_batch
            conv_batch = self._get_conversation_batch()

        return conversations

    def _get_conversation_batch(self):
        next_bookmark = self.bookmark_manager.get_bookmark(primary='conversations')

        if next_bookmark == '-end-':
            return []

        options = {
            "isPrefetch": False,
            "field_set_key": "default",
            "bookmarks": [next_bookmark]
        }

        url = self.req_builder.buildGet(url=CONVERSATION_RESOURCE, options=options)
        response = self.get(url=url).json()

        next_bookmark = response['resource']['options']['bookmarks'][0]
        self.bookmark_manager.add_bookmark(primary='conversations', bookmark=next_bookmark)

        return response['resource_response']['data']

    def create_board_section(self, board_id='', section_name=''):
        options = {
            "board_id": board_id,
            "initial_pins": [],
            "name": section_name,
            "name_source": 0
        }

        data = self.req_builder.buildPost(options=options)
        return self.post(url=BOARD_SECTION_RESOURCE, data=data)

    def get_board_sections(self, board_id=''):
        options = {
            "isPrefetch": False,
            "board_id": board_id,
            "redux_normalize_feed": True
        }

        url = self.req_builder.buildGet(url=GET_BOARD_SECTIONS, options=options)
        response = self.get(url=url).json()
        return response['resource_response']['data']['ReactBoardFeedResource']

    def get_section_pins(self, username='', board_name='', section_name=''):

        url = 'https://www.pinterest.com/{}/{}/{}/'.format(username, board_name, section_name)
        data = self.get(url=url)

        soup = BeautifulSoup(data.text, 'html.parser')
        script = soup.find("script", {"id": "initial-state"})
        data = json.loads(script.text)['resources']['data']['ReactBoardFeedResource']
        first_entry = next(iter(data.values()))
        return first_entry['data']['section_pin_feed']

    def delete_board_section(self, section_id=''):
        options = {
            "section_id": section_id
        }
        data = self.req_builder.buildPost(options=options)
        return self.post(url=BOARD_SECTION_EDIT_RESOURCE, data=data)
