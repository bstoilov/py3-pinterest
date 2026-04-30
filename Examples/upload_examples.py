from py3pin.Pinterest import Pinterest

pinterest = Pinterest(email='email',
                      password='password',
                      username='username',
                      cred_root='cred_root')

board_id = 'your_board_id'


def upload_image_pin():
    return pinterest.upload_pin(
        board_id=board_id,
        image_file='path/to/image.jpg',
        title='My Image Pin',
        description='Uploaded with py3-pinterest',
        link='https://example.com',
    )


def upload_video_pin():
    # Requires ffmpeg and ffprobe on PATH for automatic
    # video duration/dimension detection and cover image extraction.
    return pinterest.upload_video_pin(
        board_id=board_id,
        video_file='path/to/video.mov',
        title='My Video Pin',
        description='Uploaded with py3-pinterest',
        link='https://example.com',
    )


def upload_video_pin_manual():
    # If you don't have ffmpeg, provide video metadata manually.
    return pinterest.upload_video_pin(
        board_id=board_id,
        video_file='path/to/video.mov',
        title='My Video Pin',
        description='Uploaded with py3-pinterest',
        duration_ms=15000,
        width=1080,
        height=1920,
        cover_image_file='path/to/cover.jpg',
    )


def upload_pin_to_section(section_id=''):
    return pinterest.upload_pin(
        board_id=board_id,
        section_id=section_id,
        image_file='path/to/image.jpg',
        title='Section Pin',
        description='Pinned to a specific section',
    )


def pin_from_url():
    return pinterest.pin(
        board_id=board_id,
        image_url='https://i.pinimg.com/170x/32/78/bd/3278bd27073e1ec9c8a708409279768b.jpg',
        title='Pin from URL',
        description='Pinned from an image URL',
        link='https://example.com',
    )
