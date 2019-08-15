from py3pin.Pinterest import Pinterest
import requests

username = 'your username'
password = 'your password'
email = 'login email'
cred_root = 'some dir'
download_dir = 'dir where images will be downloaded'

pinterest = Pinterest(email=email,
                      password=password,
                      username=username,
                      cred_root=cred_root)

# login if needed
# pinterest.login()

# your boards, pick one
boards = pinterest.boards()

# for example the first one
target_board = boards[0]

# get all pins for the board
board_pins = []
pin_batch = pinterest.board_feed(board_id=target_board['id'], board_url=target_board['url'])

while len(pin_batch) > 0:
    board_pins += pin_batch
    pin_batch = pinterest.board_feed(board_id=target_board['id'], board_url=target_board['url'])


# this can download images by url
def download_image(url, path):
    r = requests.get(url=url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


# download each pin image in the specified directory
for pin in board_pins:
    url = pin['image']
    indx = str(url).rfind('.')
    extension = str(url)[indx:]
    download_image(url, download_dir + pin['id'] + extension)
