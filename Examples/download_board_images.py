from py3pin.Pinterest import Pinterest
import time
import requests
from requests.exceptions import ConnectionError
import os

count_skip = 0
count_download = 0
download_dir = './pinterest_images/'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

pinterest = Pinterest(email='your_email',
                      password='your_password',
                      username='your_username',
                      cred_root='cred_root')

boards = pinterest.boards_all()

for board in boards:
    print(board['name'])
    board_dir = os.path.join(download_dir, board['name'])
    if not os.path.exists(board_dir):
        os.makedirs(board_dir)

    board_pins = []
    pin_batch = pinterest.board_feed(board_id=board['id'], reset_bookmark=True)
    while len(pin_batch) > 0:
        board_pins += pin_batch
        pin_batch = pinterest.board_feed(board_id=board['id'])

    def download_image(url, path):
        global count_skip
        global count_download
        if os.path.isfile(path):
            count_skip += 1
        else:
            nb_tries = 10
            while True:
                nb_tries -= 1
                try:
                    r = requests.get(url=url, stream=True)
                    break
                except ConnectionError as err:
                    if nb_tries == 0:
                        raise err
                    else:
                        time.sleep(1)
            if r.status_code == 200:
                count_download += 1
                print("Downloading " + url)
                with open(path, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)

    for pin in board_pins:
        if 'images' in pin:
            url = pin['images']['orig']['url']
            filename = url.rsplit('/', 1)[-1]
            download_image(url, os.path.join(board_dir, filename))

print("Existing files: " + str(count_skip))
print("New files: " + str(count_download))
