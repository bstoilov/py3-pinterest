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

results = []
max_results = 100
batch_size = 50
query = 'food'

# Due to recent changes in pinterest api we can't directly search for users.
# instead we search for something else and extract pinners, owners and the relevant data
search_batch = pinterest.search(scope='pins', query=query, page_size=batch_size)
while len(search_batch) > 0 and len(results) < max_results:
    results += search_batch
    pinterest.search(scope='pins', query=query, page_size=batch_size)

target_users = []
for s in results:
    target_users.append(s['owner'])

# at this point target_users contains list of the user we want to invite.

boards = []
board_batch = pinterest.boards()
while len(board_batch) > 0:
    boards += board_batch
    board_batch = pinterest.boards()

board = boards[0]
# we chose the first board but you can chose any board you like

for user in target_users:
    pinterest.invite(board_id=board['id'], user_id=user['id'])
    # Instead of break you need to implement some kind of pause mechanism in order not to get blocked by pinterest
    break
