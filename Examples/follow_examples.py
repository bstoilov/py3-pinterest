from py3pin.Pinterest import Pinterest

username = 'username'
password = 'password'
email = 'email'
cred_root = 'cred_root'

pinterest = Pinterest(email=email,
                      password=password,
                      username=username,
                      cred_root=cred_root)


def search_boards():
    results = []
    max_results = 100
    batch_size = 50
    query = 'food'
    scope = 'boards'

    search_batch = pinterest.search(scope=scope, query=query, page_size=batch_size, reset_bookmark=True)
    while len(search_batch) > 0 and len(results) < max_results:
        results += search_batch
        search_batch = pinterest.search(scope=scope, query=query, page_size=batch_size)

    return results


def search_users():
    results = []
    max_results = 100
    batch_size = 50
    query = 'food'
    scope = 'pins'

    search_batch = pinterest.search(scope=scope, query=query, page_size=batch_size, reset_bookmark=True)
    while len(search_batch) > 0 and len(results) < max_results:
        for res in search_batch:
            if 'pinner' in res:
                results.append(res['pinner'])
        search_batch = pinterest.search(scope=scope, query=query, page_size=batch_size)

    return results


boards = search_boards()

for b in boards:
    print(b['url'])
    pinterest.follow_board(board_id=b['id'])
    break

users = search_users()

for u in users:
    pinterest.follow_user(user_id=u['id'])
    break
