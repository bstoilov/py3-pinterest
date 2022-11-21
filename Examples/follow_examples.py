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


def search_boards():
    results = []
    max_results = 100
    batch_size = 50
    query = 'food'
    scope = 'boards'

    # Obtain a list of boards we want to follow
    search_batch = pinterest.search(scope=scope, query=query, page_size=batch_size)
    while len(search_batch) > 0 and len(results) < max_results:
        results += search_batch
        pinterest.search(scope=scope, query=query, page_size=batch_size)

    return results

def search_users():
    # pinterest no longer allows to search for users, we will search for pins and extract the pinners
    results = []
    max_results = 100
    batch_size = 50
    query = 'food'
    scope = 'pins'

    # Obtain a list of boards we want to follow
    search_batch = pinterest.search(scope=scope, query=query, page_size=batch_size)
    while len(search_batch) > 0 and len(results) < max_results:
        for res in search_batch:
            if 'pinner' in res:
                results.append(res['pinner'])
        search_batch = pinterest.search(scope=scope, query=query, page_size=batch_size)

    return results


boards = search_boards()

# Follow boards
for b in boards:
    print(b['url'])
    pinterest.follow_board(board_id=b['id'])
    # Instead of break you need a way to pause for some time in order to not get banned from pinterest.
    break

users = search_users()

for u in users:
    pinterest.follow_user(user_id=u['id'])
    # Instead of break you need a way to pause for some time in order to not get banned from pinterest.
    break
