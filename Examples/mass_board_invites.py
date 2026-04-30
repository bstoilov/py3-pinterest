from py3pin.Pinterest import Pinterest

username = 'username'
password = 'password'
email = 'email'
cred_root = 'cred_root'

pinterest = Pinterest(email=email,
                      password=password,
                      username=username,
                      cred_root=cred_root)

results = []
max_results = 100
batch_size = 50
query = 'food'

search_batch = pinterest.search(scope='pins', query=query, page_size=batch_size, reset_bookmark=True)
while len(search_batch) > 0 and len(results) < max_results:
    results += search_batch
    search_batch = pinterest.search(scope='pins', query=query, page_size=batch_size)

target_users = []
for s in results:
    target_users.append(s['owner'])

boards = pinterest.boards_all()
board = boards[0]

for user in target_users:
    pinterest.invite(board_id=board['id'], user_id=user['id'])
    break
