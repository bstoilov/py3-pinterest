from py3pin.Pinterest import Pinterest

username = 'username'
password = 'password!'
email = 'email'
# cred_root is the place the user sessions and cookies will be stored you should specify this to avoid permission issues
cred_root = 'cred_root'

pinterest = Pinterest(email=email,
                      password=password,
                      username=username,
                      cred_root=cred_root)


# get the user id by username
def get_user_id(username):
    return pinterest.get_user_overview(username=username)['id']


# Pinterest conversations are stored in a list of conversation object on their side.
# Each converastion has id and last message they use to display on the initial drop down once you click the message button
def get_all_conversations():
    return pinterest.get_conversations()


# Once you obtain a conversation id, only then you can see all the messages and participants in it.
def load_conversation(conversation_id):
    return pinterest.load_conversation(conversation_id=conversation_id)


# in order to have conversation with some one, it needs to be initialized once with some initial message
# this is called once per user (or group of users)
# the method receives array of users, this way grop conversations are started
# calling this method multiple times for the same user does nothing
def initiate_conversation(username, message):
    usernames = [username]

    # get the user id by username
    user_ids = []
    for u in usernames:
        user_ids.append(get_user_id(u))

    pinterest.initiate_conversation(user_ids=user_ids, message=message)


# search for conversation with specific user
# NOTE: he might be part of multiple conversations (group conversations)
def find_conversation_by_username(username):
    conversations = pinterest.get_conversations()
    conversation_ids = []

    # get all conversations in which username is found
    for c in conversations:
        conv_usernames = []
        for usr in c['users']:
            conv_usernames.append(usr['username'])
        if username in conv_usernames:
            conversation_ids.append(c['id'])

    return conversation_ids


# send message to user
# if this is the first time new conversation will be created
def send_message(username, message):
    conversations_ids = find_conversation_by_username(username)

    if len(conversations_ids) == 0:
        initiate_conversation(username=username, message=message)
    else:
        # add logic to chose conversation if needed
        conversation_id = conversations_ids[0]

        # you can send 3 types of messages

        # Only text message
        pinterest.send_message(conversation_id=conversation_id, pin_id=None, message=message)

        # Send pin by id
        # pinterest.send_message(conversation_id=conversation_id, pin_id="(pin_id)")

        # Message followed by pin
        # pinterest.send_message(conversation_id=conversation_id, pin_id="(pin_id)", message="hey")


send_message(username='username', message='Hi')