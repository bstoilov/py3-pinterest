from py3pin.Pinterest import Pinterest
username = 'cocococoho'
password = 'makeMoney!'
email = 'boriostoilov@gmail.com'
cred_root = '/home/kashon/py3pin'

client = Pinterest(email=email, password=password, username=username, cred_root=cred_root)

followers_batch = client.get_user_followers()

for f in followers_batch:
    print(f)

# Call this only once and when needed
# client.login()

# boards = client.boards()
#
# for b in boards:
#     print(b)




