"""
Mark Nguyen
markvn@uci.edu
84257566
"""
import sys
from pathlib import Path
import ipaddress
import regex as re

import a4
import user_interface

current_profile = None
dire_prof = None
o_c_commands = False
e_p_menu = False
logged_in = False
token = ''


def fetch_command_list():
    """Fetch command list takes a admin's input and splits the options/data."""
    command_input = input()
    if command_input == 'Q':
        sys.exit(0)
    elif len(command_input) == 1:
        print('ERROR')
        return None
    elif command_input[0] not in 'LEPCODRU':
        print('ERROR')
        return None

    if command_input[0] == 'L':
        if re.match(r"^(L) (.+) (-r) (-e) (.+)",
                    command_input) is not None:
            temp = re.split(r"^(L) (.+) (-r) (-e) (.+)", command_input)
            command_list = list(filter(None, temp))
        elif re.match(r"^(L) (.+) (-r) (-s) (.+)",
                      command_input) is not None:
            temp = re.split(r"^(L) (.+) (-r) (-s) (.+)", command_input)
            command_list = list(filter(None, temp))
        elif re.match(r"^(L) (.+) (-r) (-f)", command_input) is not None:
            temp = re.split(r"^(L) (.+) (-r) (-f)", command_input)
            command_list = list(filter(None, temp))
        elif re.match(r"^(L) (.+) (-r)", command_input) is not None:
            temp = re.split(r"^(L) (.+) (-r)", command_input)
            command_list = list(filter(None, temp))
        elif re.match(r"^(L) (.+) (-e) (.+)", command_input) is not None:
            temp = re.split(r"^(L) (.+) (-e) (.+)", command_input)
            command_list = list(filter(None, temp))
        elif re.match(r"^(L) (.+) (-s) (.+)", command_input) is not None:
            temp = re.split(r"^(L) (.+) (-s) (.+)", command_input)
            command_list = list(filter(None, temp))
        elif re.match(r"^(L) (.+) (-f)", command_input) is not None:
            temp = re.split(r"^(L) (.+) (-f)", command_input)
            command_list = list(filter(None, temp))
        else:
            command_list = re.split(r"^(L)|(?<=L\s)(.*)", command_input)
            command_list = list(filter(None, command_list))
            command_list = list(filter(str.strip, command_list))

    elif command_input[0] == 'E':
        options = ['E', '-usr', '-bio', '-addpost', '-delpost', '-pwd', '-dsu']
        command_list = re.split(r"(E|-usr|-bio|-addpost|-delpost|-pwd|-dsu"
                                r")|("
                                r"?<=\s-usr\s|\s-bio\s|\s-addpost\s|\s"
                                r"-delpost\s|\s-pwd\s|\s-dsu\s)(.*?)("
                                r"?=\s-usr\s|\s-bio\s|\s-addpost\s|\s"
                                r"-delpost\s|\s-pwd\s|\s-dsu\s|$)",
                                command_input)
        command_list = list(filter(None, command_list))
        command_list = list(filter(str.strip, command_list))
        if command_list[1] not in options:
            print('ERROR')
            return None

    elif command_input[0] == 'P':
        options = ['P', '-usr', '-bio', '-all', '-post', '-posts', '-pwd']
        check = []
        invalid_options = 0
        command_list = re.split(r"(P|-usr|-bio|-pwd|-posts|-post|-all)|("
                                r"?<=\s-usr\s|\s-bio\s|\s-pwd\s|\s-posts"
                                r"\s|\s-post\s|\s-all\s)(\d*?)("
                                r"?=\s-usr|\s-bio|\s-pwd|\s-posts|\s"
                                r"-post|\s-all\s|$)", command_input)
        command_list = list(filter(None, command_list))
        command_list = list(filter(str.strip, command_list))

        # prints ERROR for any invalid command
        if command_list[1] not in options:
            print('ERROR')
            return None
        for option in command_list:
            if option in options or option.isnumeric():
                check.append(option)
            elif option not in options:
                invalid_options += 1
        if invalid_options > 0:
            for option in check:
                if command_list[command_list.index(option) + 1] not in (
                        options or '0123456789'):
                    print('ERROR')
                    return None

    elif command_input[0] == 'C':
        command_list = re.split(r"(C|-n)|(?<=[C\s]|\s-n\s)(.*?)(?=\s-n\s|$)",
                                command_input)
        command_list = list(filter(None, command_list))
        command_list = list(filter(str.strip, command_list))
        try:
            command_list[1] = command_list[1][1:]
        except IndexError:
            return command_list

    elif command_input[0] == 'O':
        command_list = re.split(r"(O)|(?<=O\s)(.*)", command_input)
        command_list = list(filter(None, command_list))
        command_list = list(filter(str.strip, command_list))

    elif command_input[0] == 'D':
        command_list = re.split(r"(D)|(?<=D\s)(.*)", command_input)
        command_list = list(filter(None, command_list))
        command_list = list(filter(str.strip, command_list))

    elif command_input[0] == 'U':
        command_list = re.split(
            r'(U|-bio|-post)|(?<=\s-bio\s|\s-post\s)(\d*?)('
            r'?=\s-bio|\s-post\s|$)',
            command_input)
        command_list = list(filter(None, command_list))
        command_list = list(filter(str.strip, command_list))

    elif command_input[0] == 'R':
        command_list = re.split(r"(R)|(?<=R\s)(.*)$", command_input)
        command_list = list(filter(None, command_list))
        command_list = list(filter(str.strip, command_list))

    else:
        print('ERROR')
        command_list = None

    for i, v in enumerate(command_list):
        if v[0].isspace() or v[-1].isspace():
            print('ERROR')
            return None

    return command_list


def existence(directory_path, file_path=False):
    """Check if a file is a file_path or if it exists."""
    if not file_path:
        if Path.is_dir(directory_path):
            return True
        else:
            print('ERROR')
    elif file_path:
        if Path.is_file(directory_path):
            return True
        else:
            print('ERROR')


def commands(command_list):
    """
    commands() calls the respective command based on the command list that is
    created from admin's input.
    """
    try:
        if command_list is not None:
            dirpath = Path(command_list[1])
            if command_list[0] == 'L':
                if existence(dirpath):
                    a4.l_command(command_list)
            elif command_list[0] == 'C':
                if existence(dirpath):
                    a4.c_command(command_list)
            elif command_list[0] == 'D':
                if existence(dirpath, file_path=True):
                    a4.d_command(command_list)
            elif command_list[0] == 'R':
                if existence(dirpath, file_path=True):
                    a4.r_command(command_list)
            elif command_list[0] == 'O':
                if existence(dirpath, file_path=True):
                    a4.o_command(command_list)
            if command_list[0] == 'E' or command_list[0] == 'P':
                if not o_c_commands:
                    if user_interface.admin_mode:
                        print('ERROR')
            if o_c_commands:
                if command_list[0] == 'E':
                    if check_e_option_validity(command_list):
                        a4.e_command(command_list)
                elif command_list[0] == 'P':
                    if check_p_option_validity(command_list):
                        a4.p_command(command_list)
                elif command_list[0] == 'U':
                    a4.u_command(command_list)
    except IndexError:
        print('ERROR')


def check_u_option_validity(command_list):
    """Ensures that options are not used twice in the U-command."""
    if '-bio' in command_list:
        if command_list.count('-bio') > 1:
            print('ERROR')
            return False
    if '-post' in command_list:
        if command_list.count('-post') > 1:
            print('ERROR')
            return False


def check_p_option_validity(command_list):
    """Ensures that options are not used twice in the P-command."""
    if '-usr' in command_list:
        if command_list.count('-usr') > 1:
            print('ERROR')
            return False
    if '-pwd' in command_list:
        if command_list.count('-pwd') > 1:
            print('ERROR')
            return False
    if '-bio' in command_list:
        if command_list.count('-bio') > 1:
            print('ERROR')
            return False
    if '-post' in command_list:
        if command_list.count('-post') > 1:
            print('ERROR')
            return False
    if '-posts' in command_list:
        if command_list.count('-posts') > 1:
            print('ERROR')
            return False
    if '-all' in command_list:
        if command_list.count('-all') > 1:
            print('ERROR')
            return False
    return True


def check_e_option_validity(command_list):
    """Ensures that edits are valid."""
    try:
        if '-usr' in command_list:
            new_username = command_list[command_list.index('-usr') + 1]
            if ' ' in new_username:
                print('ERROR')
                return False
            elif new_username[0] + new_username[-1] not in ['""', "''"]:
                print(new_username[0] + new_username[-1])
                print('ERROR')
                return False
            elif command_list.count('-usr') > 1:
                print('ERROR')
                return False
            else:
                new_username = new_username[1:-1]
                command_list[command_list.index('-usr') + 1] = new_username
        if '-pwd' in command_list:
            new_pass = command_list[command_list.index('-pwd') + 1]
            if ' ' in new_pass:
                print('ERROR')
                return False
            elif new_pass[0] + new_pass[-1] not in ['""', "''"]:
                print('ERROR')
                return False
            elif command_list.count('-pwd') > 1:
                print('ERROR')
                return False
            else:
                new_pass = new_pass[1:-1]
                command_list[command_list.index('-pwd') + 1] = new_pass
        if '-bio' in command_list:
            new_bio = command_list[command_list.index('-bio') + 1]
            if new_bio[0] + new_bio[-1] not in ['""', "''"]:
                print('ERROR')
                return False
            elif new_bio.isspace():
                print('ERROR')
                return False
            elif command_list.count('-bio') > 1:
                print('ERROR')
                return False
            else:
                new_bio = new_bio[1:-1]
                command_list[command_list.index('-bio') + 1] = new_bio
        if '-addpost' in command_list:
            post_entry = command_list[command_list.index('-addpost') + 1]
            if post_entry[0] + post_entry[-1] not in ['""', "''"]:
                print('ERROR')
                return False
            elif post_entry[1:-1].isspace():
                print('ERROR')
                return False
            elif command_list.count('-addpost') > 1:
                print('ERROR')
                return False
            else:
                post_entry = post_entry[1:-1]
                command_list[command_list.index('-addpost') + 1] = post_entry
        if '-delpost' in command_list:
            post_id = command_list[command_list.index('-delpost') + 1]
            if not post_id.isnumeric():
                print('ERROR')
                return False
            elif command_list.count('-delpost') > 1:
                print('ERROR')
                return False
            elif int(post_id) >= len(current_profile.get_posts()):
                print('ERROR')
        if '-dsu' in command_list:
            ip_ad = command_list[command_list.index('-dsu') + 1]
            if ip_ad[0] + ip_ad[-1] not in ['""', "''"]:
                print('ERROR')
                return False
            else:
                ip_ad = ip_ad[1:-1]
                command_list[command_list.index('-dsu')+1] = ip_ad
            try:
                ipaddress.ip_address(ip_ad)
            except ValueError:
                print('ERROR')
                return False
    except IndexError:
        if user_interface.admin_mode:
            print('ERROR')
        elif not user_interface.admin_mode:
            print('IndexError')
        return None

    return True
