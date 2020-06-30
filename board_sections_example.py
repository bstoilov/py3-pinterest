from py3pin.Pinterest import Pinterest

pinterest = Pinterest(email='email',
                      password='password',
                      username='username',
                      cred_root='cred_root')


def print_all_section_pin_ids():
    boards = pinterest.boards()
    for board in boards:
        target_board = board
        sections = pinterest.get_board_sections(board_id=target_board['id'])

        print(target_board['name'])
        for section in sections:
            print(section['slug'])
            section_pins = pinterest.get_section_pins(section_id=section['id'])
            while section_pins:
                for sec_pin in section_pins:
                    print(sec_pin['id'])
                section_pins = pinterest.get_section_pins(section_id=section['id'])

        print('\n')


print_all_section_pin_ids()
