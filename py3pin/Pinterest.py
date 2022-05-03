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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType

AGENT_STRING = (
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
)

# Pinterest endpoints
HOME_PAGE = "https://www.pinterest.com/"
LOGIN_PAGE = "https://www.pinterest.com/login/?referrer=home_page"
CREATE_USER_SESSION = "https://www.pinterest.com/resource/UserSessionResource/create/"
DELETE_USER_SESSION = "https://www.pinterest.com/resource/UserSessionResource/delete/"
USER_RESOURCE = "https://www.pinterest.com/_ngjs/resource/UserResource/get/"
BOARD_PICKER_RESOURCE = (
    "https://www.pinterest.com/resource/BoardPickerBoardsResource/get/"
)
BOARDS_RESOURCE = "https://www.pinterest.com/_ngjs/resource/BoardsResource/get/"
CREATE_BOARD_RESOURCE = "https://www.pinterest.com/resource/BoardResource/create/"
FOLLOW_BOARD_RESOURCE = "https://www.pinterest.com/resource/BoardFollowResource/create/"
UNFOLLOW_BOARD_RESOURCE = (
    "https://www.pinterest.com/resource/BoardFollowResource/delete/"
)
FOLLOW_USER_RESOURCE = "https://www.pinterest.com/resource/UserFollowResource/create/"
UNFOLLOW_USER_RESOURCE = "https://www.pinterest.com/resource/UserFollowResource/delete/"
USER_FOLLOWING_RESOURCE = (
    "https://www.pinterest.com/_ngjs/resource/UserFollowingResource/get/"
)
USER_FOLLOWERS_RESOURCE = (
    "https://www.pinterest.com/resource/UserFollowersResource/get/"
)
PIN_RESOURCE_CREATE = "https://www.pinterest.com/resource/PinResource/create/"
REPIN_RESOURCE_CREATE = "https://www.pinterest.com/resource/RepinResource/create/"
PIN_LIKE_RESOURCE = "https://www.pinterest.com/resource/PinLikeResource/create/"
PIN_UNLIKE_RESOURCE = "https://www.pinterest.com/resource/PinLikeResource/delete/"
DELETE_PIN_RESOURCE = "https://www.pinterest.com/resource/PinResource/delete/"
PIN_COMMENT_RESOURCE = "https://www.pinterest.com/resource/PinCommentResource/create/"
BOARD_INVITE_RESOURCE = (
    "https://www.pinterest.com/_ngjs/resource/BoardInviteResource/create/"
)
BOARD_DELETE_INVITE_RESOURCE = (
    "https://www.pinterest.com/_ngjs/resource/BoardCollaboratorResource/delete/"
)
VISUAL_LIVE_SEARCH_RESOURCE = (
    "https://www.pinterest.com/resource/VisualLiveSearchResource/get/"
)
SEARCH_RESOURCE = "https://www.pinterest.com/resource/SearchResource/get/"
TYPE_AHEAD_RESOURCE = (
    "https://www.pinterest.com/resource/AdvancedTypeaheadResource/get/"
)
BOARD_RECOMMEND_RESOURCE = (
    "https://www.pinterest.com/_ngjs/resource/BoardContentRecommendationResource/get/"
)
PINNABLE_IMAGES_RESOURCE = (
    "https://www.pinterest.com/_ngjs/resource/FindPinImagesResource/get/"
)
BOARD_FEED_RESOURCE = "https://www.pinterest.com/resource/BoardFeedResource/get/"
USER_HOME_FEED_RESOURCE = (
    "https://www.pinterest.com/_ngjs/resource/UserHomefeedResource/get/"
)
USER_PIN_RESOURCE = "https://www.pinterest.com/resource/UserPinsResource/get/"
BASE_SEARCH_RESOURCE = "https://www.pinterest.com/resource/BaseSearchResource/get/"
BOARD_INVITES_RESOURCE = (
    "https://www.pinterest.com/_ngjs/resource/BoardInvitesResource/get/"
)
CREATE_COMMENT_RESOURCE = (
    "https://www.pinterest.com/_ngjs/resource/AggregatedCommentResource/create/"
)
GET_PIN_COMMENTS_RESOURCE = (
    "https://www.pinterest.com/_ngjs/resource/AggregatedCommentFeedResource/get/"
)
LOAD_PIN_URL_FORMAT = "https://www.pinterest.com/pin/{}/"
DELETE_COMMENT = (
    "https://www.pinterest.com/_ngjs/resource/AggregatedCommentResource/delete/"
)
CONVERSATION_RESOURCE = "https://www.pinterest.com/resource/ConversationsResource/get/"
CONVERSATION_RESOURCE_CREATE = (
    "https://www.pinterest.com/resource/ConversationsResource/create/"
)
LOAD_CONVERSATION = (
    "https://www.pinterest.com/resource/ConversationMessagesResource/get/"
)
SEND_MESSAGE = "https://www.pinterest.com/resource/ConversationMessagesResource/create/"
BOARD_SECTION_RESOURCE = (
    "https://www.pinterest.com/resource/BoardSectionResource/create/"
)
GET_BOARD_SECTIONS = "https://www.pinterest.com/resource/BoardSectionsResource/get/"
BOARD_SECTION_EDIT_RESOURCE = (
    "https://www.pinterest.com/resource/BoardSectionEditResource/delete/"
)
GET_BOARD_SECTION_PINS = (
    "https://www.pinterest.com/resource/BoardSectionPinsResource/get/"
)
UPLOAD_IMAGE = "https://www.pinterest.com/upload-image/"
BOARD_FOLLOWERS = "https://pinterest.com/resource/BoardFollowersResource/get/"
ADD_PIN_NOTE = "https://www.pinterest.com/resource/ApiResource/create/"


class Pinterest:
    def __init__(
        self,
        password="",
        proxies=None,
        username="",
        email="",
        cred_root="data",
        user_agent=None,
    ):
        self.email = email
        self.username = username
        self.password = password
        self.req_builder = RequestBuilder()
        self.bookmark_manager = BookmarkManager()
        self.http = requests.session()
        self.proxies = proxies
        self.user_agent = user_agent

        self.registry = Registry(cred_root, email)

        cookies = self.registry.get_all()
        for key in cookies.keys():
            self.http.cookies.set(key, cookies[key])

        if self.user_agent is None:
            self.user_agent = AGENT_STRING

    def request(self, method, url, data=None, files=None, extra_headers=None):
        headers = CaseInsensitiveDict(
            [
                ("Referer", HOME_PAGE),
                ("X-Requested-With", "XMLHttpRequest"),
                ("Accept", "application/json"),
                ("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"),
                ("User-Agent", self.user_agent),
            ]
        )
        csrftoken = self.http.cookies.get("csrftoken")
        if csrftoken:
            headers.update([("X-CSRFToken", csrftoken)])

        if extra_headers is not None:
            for h in extra_headers:
                headers.update([(h, extra_headers[h])])

        response = self.http.request(
            method, url, data=data, headers=headers, files=files, proxies=self.proxies
        )
        response.raise_for_status()

        return response

    def get(self, url):
        return self.request("GET", url=url)

    def post(self, url, data=None, files=None, headers=None):
        return self.request(
            "POST", url=url, data=data, files=files, extra_headers=headers
        )

    def login(self, headless=True, wait_time=15, proxy=None, lang="en"):
        """
        Logs user in with the provided credentials
        User session is stored in the 'cred_root' folder
        and reused so there is no need to login every time.
        Pinterest sessions lasts for about 15 days
        Ideally you need to call this method 3-4 times a month at most.
        :return python dict object describing the pinterest response
        """
        chrome_options = Options()
        chrome_options.add_argument("--lang=%s" % lang)
        if headless:
            chrome_options.add_argument("--headless")

        if proxy is not None:
            http_proxy = Proxy()
            http_proxy.proxy_type = ProxyType.MANUAL
            http_proxy.http_proxy = proxy
            http_proxy.socks_proxy = proxy
            http_proxy.ssl_proxy = proxy
            http_proxy.add_to_capabilities(chrome_options)

        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options
        )
        driver.get("https://pinterest.com/login")

        try:
            WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((By.ID, "email"))
            )

            driver.find_element_by_id("email").send_keys(self.email)
            driver.find_element_by_id("password").send_keys(self.password)

            logins = driver.find_elements_by_xpath("//*[contains(text(), 'Log in')]")

            for login in logins:
                login.click()

            WebDriverWait(driver, wait_time).until(
                EC.invisibility_of_element((By.ID, "email"))
            )

            cookies = driver.get_cookies()

            self.http.cookies.clear()
            for cookie in cookies:
                self.http.cookies.set(cookie["name"], cookie["value"])

            self.registry.update_all(self.http.cookies.get_dict())
        except Exception as e:
            print("Failed to login", e)

        print("Successfully logged in with account " + self.email)
        driver.close()

    def logout(self):
        """
        Logs current user out. Takes few seconds for the session to be invalidated on pinterest's side
        """
        options = {"disable_auth_failure_redirect": True}

        data = self.req_builder.buildPost(options=options)
        return self.post(url=DELETE_USER_SESSION, data=data)

    def get_board_followers(self, board_id, page_size=50, source_url=None):
        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="board_followers", secondary=board_id
        )
        if next_bookmark == "-end-":
            return []

        options = {
            "isPrefetch": False,
            "board_id": board_id,
            "page_size": page_size,
            "no_fetch_context_on_resource": False,
        }
        url = self.req_builder.buildGet(
            url=BOARD_FOLLOWERS, options=options, source_url=source_url
        )

        resp = self.get(url=url).json()

        bookmark = resp["resource"]["options"]["bookmarks"][0]
        self.bookmark_manager.add_bookmark(
            primary="board_followers", secondary=board_id, bookmark=bookmark
        )
        return resp["resource_response"]["data"]

    def get_user_overview(self, username=None):
        """
        :param username target username, if left blank current user is assumed
        :return python dict describing the pinterest user profile response
        """
        if username is None:
            username = self.username

        options = {
            "isPrefetch": "false",
            "username": username,
            "field_set_key": "profile",
        }
        url = self.req_builder.buildGet(url=USER_RESOURCE, options=options)
        result = self.get(url=url).json()

        return result["resource_response"]["data"]

    def boards(self, username=None, page_size=50):
        """
        The data returned is chunked, this comes from pinterest's rest api.
        Some users might have huge number of boards that is why it make sense to chunk the data.
        In order to obtain all boards this method needs to be called until it returns empty list
        :param username: target username, if left blank current user is assumed
        :param page_size: controls the batch size for each request
        :return python dict describing all the boards of a user.
        """
        if username is None:
            username = self.username

        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="boards", secondary=username
        )
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
            "bookmarks": [next_bookmark],
        }
        source_url = "/{}/boards/".format(username)
        url = self.req_builder.buildGet(
            url=BOARDS_RESOURCE, options=options, source_url=source_url
        )

        result = self.get(url=url).json()
        bookmark = result["resource"]["options"]["bookmarks"][0]

        self.bookmark_manager.add_bookmark(
            primary="boards", secondary=username, bookmark=bookmark
        )
        return result["resource_response"]["data"]

    def boards_all(self, username=None):
        """
        Obtains all boards of a user.
        NOTE: some users might have huge number of boards.
        In such cases 'boards' method (which is batched) should be used in order to avoid memory issues
        :param username: target user, if left blank current user is assumed
        :return all boards of a user
        """
        boards = []
        board_batch = self.boards(username=username)
        while len(board_batch) > 0:
            boards += board_batch
            board_batch = self.boards(username=username)

        return boards

    def get_user_pins(self, username=None, page_size=250):
        """
        Obtains all the pins of a user.
        This method is batched, meaning in order to obtain all pins you need
        to call it until empty list is returned.
        :return all pins under all pins board
        :param username: target user, if left blank current user is assumed
        """
        if username is None:
            username = self.username
            own_profile = True 
        else:
            own_profile = False

        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="pins", secondary=username
        )

        if next_bookmark == "-end-":
            return []

        options = {
            "username": username,
            "is_own_profile_pins": own_profile,
            "field_set_key": "grid_item",
            "pin_filter": None,  
            "bookmarks": [next_bookmark],
            "page_size": page_size,
        }
        url = self.req_builder.buildGet(url=USER_PIN_RESOURCE, options=options)

        response = self.get(url=url).json()
        bookmark = response["resource"]["options"]["bookmarks"][0]
        self.bookmark_manager.add_bookmark(
            primary="board_feed", secondary=username, bookmark=bookmark
        )

        return response["resource_response"]["data"]

    def create_board(
        self, name, description="", category="other", privacy="public", layout="default"
    ):
        """
        Creates a new board and returns the response from pinterest.
        :param name: board name (should be unique per user)
        :param description: board description
        :param category: if you have defined categories (it is not visible to external users)
        :param privace: can be public or private
        :param layout: looks like a legacy parameter but it is mandatory (can be left as default)
        """
        options = {
            "name": name,
            "description": description,
            "category": category,
            "privacy": privacy,
            "layout": layout,
            "collab_board_email": "true",
            "collaborator_invites_enabled": "true",
        }

        source_url = "/{}/boards/".format(self.email)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        return self.post(url=CREATE_BOARD_RESOURCE, data=data)

    def follow_board(self, board_id):
        """
        Follows a board with current user.
        :param board_id: the id of the board to follow
        :return python dict with the pinterest response
        """
        options = {"board_id": board_id}
        data = self.req_builder.buildPost(options=options)
        return self.post(url=FOLLOW_BOARD_RESOURCE, data=data)

    def unfollow_board(self, board_id):
        """
        UnFollows a board with current user.
        :param board_id: the id of the board to follow
        :return python dict with the pinterest response
        """
        options = {"board_id": board_id}
        data = self.req_builder.buildPost(options=options)
        return self.post(url=UNFOLLOW_BOARD_RESOURCE, data=data)

    def follow_user(self, user_id):
        """
        Follows a user with current user.
        :param user_id: the id of the user to follow
        :return python dict with the pinterest response
        """
        options = {"user_id": user_id}
        data = self.req_builder.buildPost(options=options)
        return self.post(url=FOLLOW_USER_RESOURCE, data=data)

    def unfollow_user(self, user_id):
        """
        UnFollows a user with current user.
        :param user_id: the id of the user to follow
        :return python dict with the pinterest response
        """
        options = {"user_id": user_id}
        data = self.req_builder.buildPost(options=options)
        return self.post(url=UNFOLLOW_USER_RESOURCE, data=data)

    def get_following(self, username=None, page_size=250):
        """
        Get all users following this particular user.
        The response of this method is batched, meaning it needs to be called
        until empty list is returned
        :param username: target user, if left blank current user is assumed
        :param page_size:
        :return: python dict describing the 'following' list
        """
        if username is None:
            username = self.username

        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="following", secondary=username
        )
        if next_bookmark == "-end-":
            return []

        source_url = "/{}/_following/".format(self.email)
        options = {
            "isPrefetch": "false",
            "hide_find_friends_rep": "false",
            "username": username,
            "page_size": page_size,
            "bookmarks": [next_bookmark],
        }

        url = self.req_builder.buildGet(
            url=USER_FOLLOWING_RESOURCE, options=options, source_url=source_url
        )

        result = self.get(url=url).json()
        result = result["resource_response"]

        bookmark = "-end-"
        if "bookmark" in result:
            bookmark = result["bookmark"]

        self.bookmark_manager.add_bookmark(
            primary="following", secondary=username, bookmark=bookmark
        )

        return result["data"]

    def get_following_all(self, username=None):
        """
        Obtains list of all users that the specified user follows.
        NOTE: Some users might have huge following lists.
        In such cases using 'get_following' (which is batched) is preferred.
        :param username: target username
        :return: python dict containing all following
        """
        following = []
        following_batch = self.get_following(username=username)
        while len(following_batch) > 0:
            following += following_batch
            following_batch = self.get_following(username=username)

        return following

    def get_user_followers(self, username=None, page_size=250):
        """
        Obtains a list of user's followers.
        The response from this method is batched, meaning it needs to be called until empty list is returned.
        :param username: target username, is left blank current user is assumed
        :param page_size: batch size
        :return: python dict describing user followers
        """
        if username is None:
            username = self.username

        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="followers", secondary=username
        )

        if next_bookmark == "-end-":
            return []

        options = {
            "isPrefetch": False,
            "hide_find_friends_rep": True,
            "username": username,
            "page_size": page_size,
            "bookmarks": [next_bookmark],
        }
        source_url = "/{}/_followers/".format(self.username)

        url = self.req_builder.buildGet(
            url=USER_FOLLOWERS_RESOURCE, options=options, source_url=source_url
        )
        result = self.get(url=url).json()
        result = result["resource_response"]

        bookmark = "-end-"

        if "bookmark" in result:
            bookmark = result["bookmark"]

        self.bookmark_manager.add_bookmark(
            primary="followers", secondary=username, bookmark=bookmark
        )

        return result["data"]

    def get_user_followers_all(self, username=None):
        """
        Obtains a list of all the followers a user has.
        NOTE: Some users might have huge followers lists.
        In such cases 'get_user_followers' should be used to avoid memory errors
        :param username: target user, is left blank current user is assumed
        :return: list of follower objects
        """
        followers = []
        followers_batch = self.get_user_followers(username=username)
        while len(followers_batch) > 0:
            followers += followers_batch
            followers_batch = self.get_user_followers(username=username)

        return followers

    def pin(
        self, board_id, image_url, description="", link="", title="", alt_text="", section_id=None
    ):
        """
        Perfoms a pin operation. If you want to upload local image use 'upload_pin'
        :param board_id: id of the target board (current user should have rights to pin to it)
        :param image_url: web url of an image (not local one)
        :param description: pin description (can be blank)
        :param link: link to include (can be blank)
        :param title: title can be blank
        :param section_id: board section should be previously defined and its optional
        :return: python dict describing the pinterest response
        """
        options = {
            "board_id": board_id,
            "image_url": image_url,
            "description": description,
            "link": link if link else image_url,
            "scrape_metric": {"source": "www_url_scrape"},
            "method": "uploaded",
            "title": title,
            "alt_text": alt_text,
            "section": section_id,
        }
        source_url = "/pin/find/?url={}".format(self.req_builder.url_encode(image_url))
        data = self.req_builder.buildPost(options=options, source_url=source_url)

        return self.post(url=PIN_RESOURCE_CREATE, data=data)

    def upload_pin(
        self, board_id, image_file, description="", link="", title="", section_id=None
    ):
        """
        This method is simmilar to 'pin' except the image for the pin is local file.
        """
        image_url = self._upload_image(image_file=image_file).json()["image_url"]
        return self.pin(
            board_id=board_id,
            description=description,
            image_url=image_url,
            link=link,
            title=title,
            section_id=section_id,
        )

    def repin(self, board_id, pin_id, section_id=None):
        """
        Repin/Save action
        :param board_id: board id, current user should have right to pin to this board
        :param pin_id: pin id to repin
        :param section_id:  board section should be previously defined and its optional
        :return: python dict describing the pinterest response
        """
        options = {
            "board_id": board_id,
            "pin_id": pin_id,
            "section": section_id,
            "is_buyable_pin": False,
        }
        source_url = "/pin/{}/".format(pin_id)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        return self.post(url=REPIN_RESOURCE_CREATE, data=data)

    def _upload_image(self, image_file):
        file_name = os.path.basename(image_file)
        mime_type = mimetypes.guess_type(image_file)[0]

        form_data = MultipartEncoder(
            fields={"img": ("%s" % file_name, open(image_file, "rb"), mime_type)}
        )

        headers = {
            "Content-Length": "%s" % form_data.len,
            "Content-Type": form_data.content_type,
            "X-UPLOAD-SOURCE": "pinner_uploader",
        }

        return self.post(url=UPLOAD_IMAGE, data=form_data, headers=headers)

    def delete_pin(self, pin_id):
        """
        Deletes a pint the user owns
        :param pin_id: pin id to delete
        :return: python dict describing the pinterest response
        """
        options = {"id": pin_id}
        source_url = "/{}/".format(self.username)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        return self.post(url=DELETE_PIN_RESOURCE, data=data)

    def comment(self, pin_id, text):
        """
        Put comment on a pin
        :param pin_id: pin id to comment on
        :param text: text of the comment
        :return: python dict describing the pinterest response
        """
        pin_data = self.load_pin(pin_id=pin_id)
        options = {
            "objectId": pin_data["aggregated_pin_data"]["id"],
            "pinId": pin_id,
            "tags": "[]",
            "text": text,
        }
        data = self.req_builder.buildPost(options=options, source_url=pin_id)

        return self.post(url=CREATE_COMMENT_RESOURCE, data=data)

    def load_pin(self, pin_id):
        """
        Loads full information about a pin
        :param pin_id: pin id to load
        :return: python dict describing the pinterest response
        """
        resp = self.get(url=LOAD_PIN_URL_FORMAT.format(pin_id))
        soup = BeautifulSoup(resp.text, "html.parser")
        scripts = soup.findAll("script")
        pin_data = {}
        for s in scripts:
            if 'id' in s.attrs and s.attrs['id'] == '__PWS_DATA__':
                pinJsonData = json.loads(s.contents[0])['props']['initialReduxState']['resources']['PinResource']
                pinJsonData = pinJsonData[list(pinJsonData.keys())[0]]['data']
                return pinJsonData

        raise Exception("Pin data not found. Probably pintereset chagned their API")

    def get_comments(self, pin_id, page_size=50):
        """
        Get comments on a pin.
        The response is batched, meaning this method should be called util empty list is returned
        :param pin_id: target pin id
        :param page_size:  batch size
        :return: list of comment objects
        """
        pin_data = self.load_pin(pin_id=pin_id)

        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="pin_comments", secondary=pin_id
        )

        if next_bookmark == "-end-":
            return []

        options = {
            "isPrefetch": False,
            "objectId": pin_data["aggregated_pin_data"]["id"],
            "page_size": page_size,
            "redux_normalize_feed": True,
            "bookmarks": [next_bookmark],
        }
        source_url = "/pin/{}/".format(pin_id)
        url = self.req_builder.buildGet(
            url=GET_PIN_COMMENTS_RESOURCE, options=options, source_url=source_url
        )
        resp = self.get(url=url).json()
        resp = resp["resource_response"]

        bookmark = "-end-"
        if "bookmark" in resp:
            bookmark = resp["bookmark"]

        self.bookmark_manager.add_bookmark(
            primary="pin_comments", secondary=pin_id, bookmark=bookmark
        )

        return resp["data"]

    def get_comments_all(self, pin_id):
        """
        Obtains all comments of a pin.
        NOTE: IF pin has too many comments this might cause memory issues.
        In such cases use 'get_comments' which is batched
        :param pin_id:
        :return: list of comment objects
        """
        results = []
        search_batch = self.get_comments(pin_id=pin_id)
        while len(search_batch) > 0:
            results += search_batch
            search_batch = self.get_comments(pin_id=pin_id)

        return results

    def delete_comment(self, pin_id, comment_id):
        """
        Deletes a comment
        :param pin_id: pin id to search the comment in
        :param comment_id: comment id
        :return:
        """
        options = {"commentId": comment_id}
        source_url = "/pin/{}/".format(pin_id)
        data = self.req_builder.buildPost(options=options, source_url=source_url)
        return self.post(url=DELETE_COMMENT, data=data)

    def invite(self, board_id, user_id):
        """
        Invite a user to one of the current user's boards
        :param board_id: board to invite to
        :param user_id: user to invite
        :return: python dict describing the pinterest response
        """
        options = {"board_id": board_id, "invited_user_ids": [user_id]}
        data = self.req_builder.buildPost(options=options)
        return self.post(url=BOARD_INVITE_RESOURCE, data=data)

    def get_board_invites(self, board_id, page_size=100):
        """
        Returns a list of users invited to the specified board.
        This method is batched and needs to be called until empty list is returned.
        :param board_id: id of target board
        :param page_size: batch size
        :return: list of board objects
        """
        options = {
            "isPrefetch": False,
            "board_id": board_id,
            "sort": "viewer_first",
            "field_set_key": "boardEdit",
            "status_filters": "new,accepted,contact_request_not_approved,pending_approval",
            "include_inactive": True,
            "page_size": page_size,
        }
        url = self.req_builder.buildGet(url=BOARD_INVITES_RESOURCE, options=options)

        resp = self.get(url=url).json()

        return resp["resource_response"]["data"]

    def get_board_invites_all(self, board_id):
        """
        Obtains all invites of a board.
        NOTE: If board has too many invites this might cause memory issues.
        In such cases use 'get_board_invites' which is batched
        :param board_id:
        :return: list of board invite objects
        """
        results = []
        search_batch = self.get_board_invites(board_id=board_id)
        while len(search_batch) > 0:
            results += search_batch
            search_batch = self.get_board_invites(board_id=board_id)

        return results

    def delete_invite(self, board_id, invited_user_id, also_block=False):
        """
        Deletes invite for a board
        :param board_id: board id
        :param invited_user_id: invited user id
        :param also_block: you can also block the user (default false)
        :return: python dict describing the pinterest response
        """
        options = {
            "ban": also_block,
            "board_id": board_id,
            "field_set_key": "boardEdit",
            "invited_user_id": invited_user_id,
        }
        data = self.req_builder.buildPost(options=options)
        return self.post(url=BOARD_DELETE_INVITE_RESOURCE, data=data)

    def visual_search(self, pin_data, x=None, y=None, w=None, h=None, padding=10):
        """
        Gives access to pinterest search api
        This method is batched, meaning is needs to be called until empty list is returned.
        :param pin_data: pin data
        :param x: x position of the cropped part of the image used for searching
        :param y: y position of the cropped part of the image used for searching
        :param w: width of the cropped part of the image used for searching
        :param h: height of the cropped part of the image used for searching
        :param padding: Default padding for cropped image.

        :return: python dict describing the pinterest response
        """

        orig = pin_data["images"]["orig"]
        width = orig["width"]
        height = orig["height"]
        image_signature = pin_data["image_signature"]
        pin_id = pin_data["id"]

        x = padding if x is None else x
        y = padding if y is None else y
        w = width - padding * 2 if w is None else w
        h = height - padding * 2 if h is None else h

        source_url = "/pin/{}/visual-search/?x={}&y={}&w={}&h={}".format(
            pin_id, x, y, w, h
        )

        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="visual_search", secondary=source_url
        )
        if next_bookmark == "-end-":
            return []

        options = {
            "isPrefetch": False,
            "pin_id": pin_id,
            "image_signature": image_signature,
            "crop": {"x": x / width, "y": y / height, "w": w / width, "h": h / height},
            "bookmarks": [next_bookmark],
            "no_fetch_context_on_resource": False,
        }
        url = self.req_builder.buildGet(
            url=VISUAL_LIVE_SEARCH_RESOURCE, options=options, source_url=source_url
        )
        resp = self.get(url=url).json()

        bookmark = resp["resource"]["options"]["bookmarks"][0]

        self.bookmark_manager.add_bookmark(
            primary="visual_search", secondary=source_url, bookmark=bookmark
        )

        return resp["resource_response"]["data"]["results"]

    def search(self, scope, query, page_size=250):
        """
        Gives access to pinterest search api
        This method is batched, meaning is needs to be called until empty list is returned.
        NOTE: there is a max number of results set by Pinterest -> 1000
        :param scope: can be pins, buyable_pins, my_pins, videos, boards
        :param query: search phrase
        :param page_size: batch size
        :return: list of search results
        """

        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="search", secondary=query
        )

        if next_bookmark == "-end-":
            return []

        terms = query.split(" ")
        escaped_query = "%20".join(terms)
        term_meta_arr = []
        for t in terms:
            term_meta_arr.append("term_meta[]=" + t)
        term_arg = "%7Ctyped&".join(term_meta_arr)
        source_url = "/search/{}/?q={}&rs=typed&{}%7Ctyped".format(
            scope, escaped_query, term_arg
        )
        options = {
            "isPrefetch": False,
            "auto_correction_disabled": False,
            "query": query,
            "redux_normalize_feed": True,
            "rs": "typed",
            "scope": scope,
            "page_size": page_size,
            "bookmarks": [next_bookmark],
        }
        url = self.req_builder.buildGet(
            url=BASE_SEARCH_RESOURCE, options=options, source_url=source_url
        )
        resp = self.get(url=url).json()

        bookmark = resp["resource"]["options"]["bookmarks"][0]

        self.bookmark_manager.add_bookmark(
            primary="search", secondary=query, bookmark=bookmark
        )
        return resp["resource_response"]["data"]["results"]

    def board_recommendations(self, board_id="", page_size=50):
        """
        This gives the list of pins you see when you open a board and click on 'More Ideas'
        This method is batched and needs to be called until empty list is returned in order to obtain all
        of the results.
        :param board_id: target board id
        :param page_size: batch size
        :return:
        """
        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="boards", secondary=board_id
        )

        if next_bookmark == "-end-":
            return []

        options = {
            "isPrefetch": False,
            "type": "board",
            "id": board_id,
            "page_size": page_size,
            "bookmarks": [next_bookmark],
        }
        url = self.req_builder.buildGet(url=BOARD_RECOMMEND_RESOURCE, options=options)

        response = self.get(url=url).json()
        bookmark = response["resource"]["options"]["bookmarks"][0]
        self.bookmark_manager.add_bookmark(
            primary="boards", secondary=board_id, bookmark=bookmark
        )

        return response["resource_response"]["data"]

    def get_pinnable_images(self, url):
        """
        Simple API pinterest uses to suggest images from site.
        """
        options = {
            "isPrefetch": "false",
            "url": url,
            "source": "pin_create",
            "appendItems": "false",
            "followRedirects": "true",
        }
        url = self.req_builder.buildGet(
            url=PINNABLE_IMAGES_RESOURCE, source_url="/pin-builder/", options=options
        )

        res = self.get(url=url).json()
        res = res["resource_response"]["data"]["items"]
        urls = []
        for item in res:
            if "url" in item:
                urls.append(item["url"])
        return urls

    def home_feed(self, page_size=100):
        """
        This gives the list of pins you see when you open the pinterest home page.
        This method is batched, in order to obtain all home feed items
        it needs to be called until empty list is returned
        :param page_size:
        :return:
        """
        next_bookmark = self.bookmark_manager.get_bookmark(primary="home_feed")
        if next_bookmark == "-end-":
            return []

        options = {
            "bookmarks": [next_bookmark],
            "isPrefetch": False,
            "field_set_key": "hf_grid_partner",
            "in_nux": False,
            "prependPartner": True,
            "prependUserNews": False,
            "static_feed": False,
            "page_size": page_size,
        }
        url = self.req_builder.buildGet(url=USER_HOME_FEED_RESOURCE, options=options)

        response = self.get(url=url).json()

        bookmark = "-end-"

        if "bookmark" in response["resource_response"]:
            bookmark = response["resource_response"]["bookmark"]

        self.bookmark_manager.add_bookmark(primary="home_feed", bookmark=bookmark)

        return response["resource_response"]["data"]

    def board_feed(self, board_id="", page_size=250):
        """
        Gives a list of all pins in a board.
        This method is batched, meaning in order to obtain all pins in a board you need
        to call it until empty list is returned.
        """
        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="board_feed", secondary=board_id
        )

        if next_bookmark == "-end-":
            return []

        options = {
            "isPrefetch": False,
            "board_id": board_id,
            "field_set_key": "partner_react_grid_pin",
            "filter_section_pins": True,
            "layout": "default",
            "page_size": page_size,
            "redux_normalize_feed": True,
            "bookmarks": [next_bookmark],
        }

        url = self.req_builder.buildGet(url=BOARD_FEED_RESOURCE, options=options)
        response = self.get(url=url).json()
        bookmark = response["resource"]["options"]["bookmarks"][0]
        self.bookmark_manager.add_bookmark(
            primary="board_feed", secondary=board_id, bookmark=bookmark
        )

        return response["resource_response"]["data"]

    def initiate_conversation(self, user_ids, message="hi"):
        """
        Initiates a new conversation with one or more users
        :return: python dict object describing the pinterest response
        """
        options = {"user_ids": user_ids, "text": message}
        data = self.req_builder.buildPost(options=options)
        return self.post(url=CONVERSATION_RESOURCE_CREATE, data=data)

    def send_message(self, message="", conversation_id="", pin_id=""):
        """
        Sends a new mesage to an already initiated conversation
        """
        options = {"conversation_id": conversation_id, "text": message, "pin": pin_id}

        data = self.req_builder.buildPost(options=options)
        return self.post(url=SEND_MESSAGE, data=data)

    def load_conversation(self, conversation_id=""):
        """
        Loads a list of all messages in a conversation
        """
        messages = []

        message_batch = self._load_conversation_batch(conversation_id=conversation_id)
        while len(message_batch) > 0:
            messages += message_batch
            message_batch = self._load_conversation_batch(
                conversation_id=conversation_id
            )

        return messages

    def _load_conversation_batch(self, conversation_id="", page_size=25):
        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="conversations", secondary=conversation_id
        )

        if next_bookmark == "-end-":
            return []

        options = {
            "isPrefetch": False,
            "page_size": page_size,
            "conversation_id": conversation_id,
            "bookmarks": [next_bookmark],
        }

        url = self.req_builder.buildGet(url=LOAD_CONVERSATION, options=options)
        response = self.get(url=url).json()

        bookmark = response["resource"]["options"]["bookmarks"][0]
        self.bookmark_manager.add_bookmark(
            primary="conversations", secondary=conversation_id, bookmark=bookmark
        )

        return response["resource_response"]["data"]

    def get_conversations(self):
        """
        Loads a list of all conversations the current user has
        """
        conversations = []
        conv_batch = self._get_conversation_batch()
        while len(conv_batch) > 0:
            conversations += conv_batch
            conv_batch = self._get_conversation_batch()

        return conversations

    def _get_conversation_batch(self):
        next_bookmark = self.bookmark_manager.get_bookmark(primary="conversations")

        if next_bookmark == "-end-":
            return []

        options = {
            "isPrefetch": False,
            "field_set_key": "default",
            "bookmarks": [next_bookmark],
        }

        url = self.req_builder.buildGet(url=CONVERSATION_RESOURCE, options=options)
        response = self.get(url=url).json()
        next_bookmark = response["resource"]["options"]["bookmarks"][0]
        self.bookmark_manager.add_bookmark(
            primary="conversations", bookmark=next_bookmark
        )

        return response["resource_response"]["data"]

    def create_board_section(self, board_id="", section_name=""):
        """
        Creates a new section in a board the current user owns
        """
        options = {
            "board_id": board_id,
            "initial_pins": [],
            "name": section_name,
            "name_source": 0,
        }

        data = self.req_builder.buildPost(options=options)
        return self.post(url=BOARD_SECTION_RESOURCE, data=data)

    def get_board_sections(self, board_id="", reset_bookmark=False):
        """
        Obtains a list of all sections of a board
        """
        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="board_sections", secondary=board_id
        )
        if next_bookmark == "-end-":
            if reset_bookmark:
                self.bookmark_manager.reset_bookmark(
                    primary="board_sections", secondary=board_id
                )
            return []

        options = {
            "isPrefetch": False,
            "board_id": board_id,
            "redux_normalize_feed": True,
            "bookmarks": [next_bookmark],
        }

        url = self.req_builder.buildGet(url=GET_BOARD_SECTIONS, options=options)
        response = self.get(url=url).json()
        bookmark = response["resource"]["options"]["bookmarks"][0]
        self.bookmark_manager.add_bookmark(
            primary="board_sections", secondary=board_id, bookmark=bookmark
        )

        return response["resource_response"]["data"]

    def get_section_pins(self, section_id="", page_size=250, reset_bookmark=False):
        """
        Returns a list of all pins in a board section.
        This method is batched meaning in order to obtain all pins in the section
        you need to call is until empty list is returned
        """
        next_bookmark = self.bookmark_manager.get_bookmark(
            primary="section_pins", secondary=section_id
        )
        if next_bookmark == "-end-":
            if reset_bookmark:
                self.bookmark_manager.reset_bookmark(
                    primary="section_pins", secondary=section_id
                )
            return []

        options = {
            "isPrefetch": False,
            "field_set_key": "react_grid_pin",
            "is_own_profile_pins": True,
            "page_size": page_size,
            "redux_normalize_feed": True,
            "section_id": section_id,
            "bookmarks": [next_bookmark],
        }

        url = self.req_builder.buildGet(url=GET_BOARD_SECTION_PINS, options=options)
        response = self.get(url=url).json()
        bookmark = response["resource"]["options"]["bookmarks"][0]
        self.bookmark_manager.add_bookmark(
            primary="section_pins", secondary=section_id, bookmark=bookmark
        )

        pins = [d for d in response["resource_response"]["data"] if "pinner" in d]
        return pins

    def delete_board_section(self, section_id=""):
        """
        Deletes a board section by id
        """
        options = {"section_id": section_id}
        data = self.req_builder.buildPost(options=options)
        return self.post(url=BOARD_SECTION_EDIT_RESOURCE, data=data)

    def type_ahead(self, scope="pins", count=5, term=""):
        """
        returns Pinterest predictions for given term.
        Response may include user profiles.
        Example term "dada" gives ["dadaism","dada art"] etc.
        :param scope:  always "pins"
        :param count: max guess number
        :param term: word to be typed ahead
        :return: response items
        """

        source_url = "/"
        options = {
            "pin_scope": scope,
            "count": count,
            "term": term,
            "no_fetch_context_on_resource": False,
        }
        url = self.req_builder.buildGet(TYPE_AHEAD_RESOURCE, options, source_url)

        resp = self.get(url=url).json()
        return resp["resource_response"]["data"]["items"]

    def add_pin_note(self, pin_id, note):
        """
          Adds a note to pin
        """
        options = {
            "url": "/v3/pins/{}/notes/".format(pin_id),
            "data": {
                "pin_note_content": note
            }
        }

        data = self.req_builder.buildPost(options=options, source_url="/pin/{}/".format(pin_id))
        return self.post(url=ADD_PIN_NOTE, data=data)

