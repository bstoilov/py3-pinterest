from py3pin.Pinterest import Pinterest
import requests
import os
import time

download_dir = './pinterest_images/'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

pinterest = Pinterest(email='email',
                      password='password',
                      username='username',
                      cred_root='cred_root')


# this can download images by url
def download_image(url, path):
    if os.path.isfile(path):
        print("File exists")
    else:
        print("Downloading " + path)
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
            with open(path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)


def download_board_images(board):
    # get all pins for the board
    board_pins = []
    pin_batch = pinterest.board_feed(board_id=board['id'])

    while len(pin_batch) > 0:
        board_pins += pin_batch
        pin_batch = pinterest.board_feed(board_id=board['id'])

    # download each pin image in the specified directory
    for pin in board_pins:
        if 'images' in pin:
            url = pin['images']['orig']['url']
            indx = str(url).rfind('.')
            extension = str(url)[indx:]

            board_dir = os.path.join(download_dir, board['name'])
            if not os.path.exists(board_dir):
                os.makedirs(board_dir)

            download_path = os.path.join(board_dir, pin['id'] + extension)

            download_image(url, download_path)
        else:
            print("No images found for pin with id " + pin['id'])


# your boards, pick one
boards = pinterest.boards_all()

# for example the first one
target_board = boards[0]

download_board_images(target_board)
