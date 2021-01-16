from py3pin.Pinterest import Pinterest
import time
import requests
from requests.exceptions import ConnectionError
import os

countrSkip = 0
countrDnld = 0
download_dir = './pinterest_images/'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

pinterest = Pinterest(email='your_email',
                      password='your_password',
                      username='your_username',
                      cred_root='cred_root')

# your boards, pick one
boards = pinterest.boards()

# delme
for board in boards:
    target_board = board
    print(target_board['name'])
    if not os.path.exists(download_dir + target_board['name']):
        os.makedirs(download_dir + target_board['name'])

    # get all pins for the board
    board_pins = []
    pin_batch = pinterest.board_feed(board_id=target_board['id'])

    while len(pin_batch) > 0:
        board_pins += pin_batch
        pin_batch = pinterest.board_feed(board_id=target_board['id'])


    # this can download images by url
    def download_image(url, path):
        global countrSkip
        global countrDnld
        if os.path.isfile(path):
            countrSkip += 1
        else:
            nb_tries = 10
            while True:
                nb_tries -= 1
                try:
                    # Request url
                    r = requests.get(url=url, stream=True)
                    break
                except ConnectionError as err:
                    if nb_tries == 0:
                        raise err
                    else:
                        time.sleep(1)
            if r.status_code == 200:
                countrDnld += 1
                print("Downloading " + url)
                with open(path, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)


    # download each pin image in the specified directory
    for pin in board_pins:
        if 'images' in pin:
            url = pin['images']['orig']['url']
            download_image(url, download_dir + target_board['name'] + '/' + url.rsplit('/', 1)[-1])
print("Existing files:" + str(countrSkip))
print("New files:" + str(countrDnld))