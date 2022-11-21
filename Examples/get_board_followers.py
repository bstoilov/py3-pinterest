from py3pin.Pinterest import Pinterest

username = "username"
password = "password!"
email = "email"
# cred_root is the place the user sessions and cookies will be stored you should specify this to avoid permission issues
cred_root = "cred_root"


pinterest = Pinterest(
    email=email, password=password, username=username, cred_root=cred_root
)
pinterest.login()
followers = pinterest.get_board_followers(213428538529906246)

print(followers[:10])
