from py3pin.Pinterest import Pinterest

username = 'username'
password = 'password'
email = 'email'
cred_root = 'cred_root'

pinterest = Pinterest(email=email,
                      password=password,
                      username=username,
                      cred_root=cred_root)

followers = pinterest.get_board_followers(213428538529906246)
print(followers[:10])
