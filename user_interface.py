import a4
import ui
import sys
from pathlib import Path
import ipaddress

admin_mode = False


def menu():
    """main menu"""
    if not ui.e_p_menu:
        print(f'\n{"MAIN MENU":-^62}\n')
        print(
            '(L) : Lists all directories and files in the given directory.')
        print('(C) : Creates a new DSU file in the specified directory.')
        print('(O) : Loads a DSU file given the path to that file.')
        print('(R) : Reads the DSU file in the specified directory.')
        print('(D) : Deletes a DSU file in the specified directory.')
        print('(Q) : Quit the program.')
        print()
    elif ui.e_p_menu:
        print(f'\n{"MAIN MENU":-^62}\n')
        print(
            '(L) : Lists all directories and files in the given directory.')
        print('(C) : Creates a new DSU file in the specified directory.')
        print('(O) : Loads a DSU file given the path to that file.')
        print(
            '-------------------------------------------------------------')
        print('(E) : Make an edit to the loaded DSU file.')
        print('(P) : Print data stored in the loaded DSU file.')
        print(
            '-------------------------------------------------------------')
        print('(U) : Upload a change to the ICS32 Distributed Social Webpage.')
        print('(R) : Reads the DSU file in the specified directory.')
        print('(D) : Deletes a DSU file in the specified directory.')
        print('(Q) : Quit the program.')
        print()


def user_mode():
    """Determines which mode: admin or user."""
    output = ''
    while output != 'admin':
        menu()
        command = input('Please select a command from the options above: ')
        if command == 'admin':
            global admin_mode
            admin_mode = True
            output = 'admin'
        elif command == 'L':
            l_menu()
        elif command == 'C':
            c_menu()
        elif command == 'O':
            o_menu()
        elif command == 'E':
            if ui.e_p_menu:
                e_menu()
            else:
                print('\nA profile must be loaded before using the E command.')
        elif command == 'P':
            if ui.e_p_menu:
                p_menu()
            else:
                print('\nA profile must be loaded before using the P command.')
        elif command == 'U':
            if ui.e_p_menu:
                u_menu()
            else:
                print('\nA profile must be loaded before using the U command.')
        elif command == 'R':
            r_menu()
        elif command == 'D':
            d_menu()
        elif command == 'Q':
            sys.exit(0)


def l_menu():
    """L command menu"""
    print()
    print(f'{"L COMMAND SUBMENU":-^118}')
    print()
    print('(0) : Lists all directories and files in the given directory.')
    print('(1) : Lists all directories and files in the given directory and '
          'all its subdirectories.')
    print('(2) : Lists all files in the given directory.')
    print('(3) : Lists all files in the current directory and all its '
          'subdirectories.')
    print('(4) : Lists all directories or files in the given directory with '
          'respect to the given name.')
    print('(5) : Lists all directories or files in the given directory and '
          'all its subdirectories with respect to the given name.')
    print('(6) : Lists all files with the given file extension in the given '
          'directory.')
    print('(7) : Lists all files with the given file extension name in the '
          'given directory and all its subdirectories.')
    print()
    up = input('Please make a selection from the above options (or enter "m" '
               'to return to the main menu): ')
    if up == '0':
        up = l_sub_menu()
    elif up == '1':
        up = l_sub_menu(recur=True)
    elif up == '2':
        up = l_sub_menu(files_only=True)
    elif up == '3':
        up = l_sub_menu(files_only=True, recur=True)
    elif up == '4':
        up = l_sub_menu(file_s=True)
    elif up == '5':
        up = l_sub_menu(file_s=True, recur=True)
    elif up == '6':
        up = l_sub_menu(file_e=True)
    elif up == '7':
        up = l_sub_menu(file_e=True, recur=True)
    if up == 'm':
        return
    else:
        l_menu()


def l_sub_menu(files_only=False, file_s=False, file_e=False, recur=False):
    """L command submenu"""
    dire = input('Please enter a path (or enter "m" to return to the '
                 'previous menu):\n')
    while True:
        if dire == 'm':
            return
        if Path(dire).is_dir():
            break
        else:
            dire = input(
                'Please enter a valid directory path (or enter "m" to return '
                'to the previous menu):\n')

    while True:
        if dire == 'm':
            return
        if not files_only and not file_s and not file_e and not recur:  # (0)
            print('\nRESULTS:')
            a4.l_command(['L', dire])
            break

        elif recur and not files_only and not file_s and not file_e:  # (1)
            print('\nRESULTS:')
            a4.l_command(['L', dire, '-r'])
            break

        elif files_only and not file_s and not file_e and not recur:  # (2)
            print('\nRESULTS:')
            a4.l_command(['L', dire, '-f'])
            break

        elif files_only and recur and not file_s and not file_e:  # (3)
            print('\nRESULTS:')
            a4.l_command(['L', dire, '-r', '-f'])
            break

        elif file_s and not files_only and not file_e and not recur:  # (4)
            filename = input(
                'Please enter a file name or a directory name (or enter "m" '
                'to return to the previous menu):\n')
            if filename == 'm':
                return
            print('\nRESULTS:')
            status = a4.l_command(['L', dire, '-s', filename])
            if not status:
                break

        elif file_s and recur and not files_only and not file_e:  # (5)
            filename = input(
                'Please enter a file name or a directory name (or enter "m" '
                'to return to the previous menu):\n')
            if filename == 'm':
                return
            print('\nRESULTS:')
            status = a4.l_command(['L', dire, '-r', '-s', filename])
            if not status:
                break

        elif file_e and not files_only and not file_s and not recur:  # (6)
            ext = input(
                'Please enter an file extension (or enter "m" to return to '
                'the previous menu):\n')
            if ext == 'm':
                return
            print('\nRESULTS:')
            status = a4.l_command(['L', dire, '-e', ext])
            if not status:
                break

        elif file_e and recur and not files_only and not file_s:  # (7)
            ext = input(
                'Please enter an file extension (or enter "m" to return to '
                'the previous menu):\n')
            if ext == 'm':
                return
            print('\nRESULTS:')
            status = a4.l_command(['L', dire, '-r', '-e', ext])
            if not status:
                break


def e_menu():
    """E command menu"""
    print()
    print(f'{"E COMMAND SUBMENU":-^38}')
    print()
    print('(0) : Edit your username.')
    print('(1) : Edit your password.')
    print('(2) : Edit your profile biography.')
    print('(3) : Add a post to your profile.')
    print('(4) : Delete a post from your profile.')
    print('(5) : Edit IP address.')
    print()
    up = input('Please make a selection from the above options (or enter "m" '
               'to return to the main menu): ')
    if up == '0':
        up = es(usr=True)
    elif up == '1':
        up = es(pwd=True)
    elif up == '2':
        up = es(bio=True)
    elif up == '3':
        up = es(addpo=True)
    elif up == '4':
        up = es(delpo=True)
    elif up == '5':
        up = es(ip=True)
    if up == 'm':
        return
    else:
        e_menu()


def es(usr=False, pwd=False, bio=False, addpo=False, delpo=False, ip=False):
    """E command submenu"""
    inp = ''
    while True:
        if inp == 'm':
            return 'm'
        if usr:  # (0)
            inp = input('Please enter your new username (or enter "m" to '
                        'return to the previous menu):\n')
            while True:
                if inp == 'm':
                    print('\nNo changes were made.')
                    return
                if ' ' not in inp:
                    a4.e_command(['E', '-usr', inp])
                    return
                else:
                    print('\nUsernames cannot contain spaces.')
                    inp = input('Please enter a valid username (or enter "m" '
                                'to return to the previous menu):\n')
        elif pwd:  # (1)
            inp = input(
                'Please enter your new password (or enter "m" to return to '
                'the previous menu):\n')
            while True:
                if inp == 'm':
                    print('\nNo changes were made.')
                    return
                if ' ' not in inp:
                    a4.e_command(['E', '-pwd', inp])
                    return
                else:
                    print('\nPasswords cannot contain spaces.')
                    inp = input('Please enter a valid password (or enter "m" '
                                'to return to the previous menu):\n')
        elif bio:  # (2)
            inp = input(
                'Please enter your profile\'s new biography (or enter "m" to '
                'return to the previous menu):\n')
            while True:
                if inp == 'm':
                    print('\nNo changes were made.')
                    return
                if not inp.isspace():
                    a4.e_command(['E', '-bio', inp])
                    return
                else:
                    print('\nYour profile biography cannot only be whitespace')
                    inp = input('Please enter a valid biography (or enter '
                                '"m" to return to the previous menu):\n')
        elif addpo:  # (3)
            inp = input('Please enter a new post for your profile (or enter '
                        '"m" to return to the previous menu):\n')
            while True:
                if inp == 'm':
                    print('\nNo changes were made.')
                    return
                if not inp.isspace() or ' ' not in inp:
                    a4.e_command(['E', '-addpost', inp])
                    return
                else:
                    print('\nYour post cannot be empty or composed of only '
                          'whitespace.')
                    inp = input('Please enter a valid post (or enter "m" to '
                                'return to the previous menu):\n')
        elif delpo:  # (4)
            print()
            print('Posts:')
            a4.p_command(['P', '-posts'])
            inp = input('\nPlease select a post to delete (or enter "m" to '
                        'return to the previous menu):\n')
            while True:
                if inp == 'm':
                    print('\nNo changes were made.')
                    return
                try:
                    if 0 <= int(inp) <= len(ui.current_profile._posts) - 1:
                        a4.e_command(['E', '-delpost', inp])
                        return
                    else:
                        print()
                        a4.p_command(['P', '-posts'])
                        print('\nThe number you entered was not listed above.')
                        inp = input('Please enter a valid post ID to delete '
                                    '(or enter "m" to return to the previous'
                                    ' menu):\n')
                except ValueError:
                    print()
                    print('The value you entered was not a number.\n')
                    inp = input('Please enter a valid post ID (or enter "m" '
                                'to return to the previous menu):\n')
        elif ip:  # (5)
            print('\nTo use the default DSU server, simply hit enter.')
            inp = input('Enter the server\'s IP address'
                        ' (or enter "m" to return to the '
                        'main menu):\n')
            while True:
                if inp == 'm':
                    return
                elif inp == '':
                    a4.e_command(['E', '-dsu', '168.235.86.101'])
                    return
                try:
                    ipaddress.ip_address(inp)
                    a4.e_command(['E', '-dsu', inp])
                    return inp
                except ValueError:
                    print('\nThe IP address you entered was invalid.\n')
                    print('To use the default DSU server, simply hit enter.')
                    inp = input('Enter a valid IP address (or enter "m" to '
                                'return to the main menu):\n')


def p_menu():
    """P command menu"""
    print()
    print(f'{"P COMMAND SUBMENU":-^47}')
    print()
    print('(0) : Print your username.')
    print('(1) : Print your password.')
    print('(2) : Print your profile\'s biography.')
    print('(3) : Print a post from your profile.')
    print('(4) : Print all posts from your profile.')
    print('(5) : Print all content stored in your profile.')
    print()
    up = input(
        'Please make a selection from the above options (or enter "m" to '
        'return to the main menu): ')
    if up == '0':
        up = ps(usr=True)
    elif up == '1':
        up = ps(pwd=True)
    elif up == '2':
        up = ps(bio=True)
    elif up == '3':
        up = ps(post_id=True)
    elif up == '4':
        up = ps(posts=True)
    elif up == '5':
        up = ps(all=True)
    if up == 'm':
        return
    else:
        p_menu()


def ps(usr=False, pwd=False, bio=False, post_id=False, posts=False, all=False):
    """P command submenu"""
    inp = ''
    while True:
        if inp == 'm':
            return 'm'
        if usr:  # (0)
            print()
            a4.p_command(['P', '-usr'])
            return

        elif pwd:  # (1)
            print()
            a4.p_command(['P', '-pwd'])
            return

        elif bio:  # (2)
            print()
            a4.p_command(['P', '-bio'])
            return

        elif post_id:  # (3)
            inp = input(
                '\nPlease enter the ID to the post you want to view (or '
                'enter "m" to return to the previous menu):\n')
            while True:
                if inp == 'm':
                    return
                try:
                    if 0 <= int(inp) <= len(ui.current_profile._posts) - 1:
                        print()
                        print(f'Post #{inp}:')
                        a4.p_command(['P', '-post', inp])
                        return
                    else:
                        print()
                        print('\nThe number you entered was not associated '
                              'with any post.')
                        inp = input(
                            'Please enter a valid ID (or enter "m" to return '
                            'to the previous menu):\n')
                except ValueError:
                    print()
                    print('The value you entered was not a number.\n')
                    inp = input('Please enter a valid ID (or enter "m" to '
                                'return to the previous menu):\n')

        elif posts:  # (4)
            print('\nPOSTS:')
            a4.p_command(['P', '-posts'])
            return

        elif all:  # (5)
            print('\nALL:')
            a4.p_command(['P', '-all'])
            return


def u_menu():
    """U command menu"""
    print()
    print(f'{"U COMMAND SUBMENU":-^59}')
    print()
    print('(0) : Upload your current biography.')
    print('(1) : Upload a post.')
    print('(2) : Upload a post and a change of your profile biography.')
    print('(m) : Return to the main menu.')
    print()
    up = input(
        'Please make a selection from the above options (or enter "m" to '
        'return to the main menu): ')
    if up == '0':
        up = u_sub_menu(bio=True)
    elif up == '1':
        up = u_sub_menu(post=True)
    elif up == '2':
        up = u_sub_menu(both=True)
    if up == 'm':
        return
    else:
        u_menu()


def u_sub_menu(bio=False, post=False, both=False):
    """U command submenu"""
    inp = ''
    while True:
        if inp == 'm':
            return 'm'
        if bio or both:  # (0)
            a4.u_command(['U', '-bio'])
            if bio:
                return

        if post or both:  # (1)
            print('\nPOSTS:')
            a4.p_command(['P', '-posts'])
            inp = input(
                '\nPlease enter the ID of the post you want to upload (or '
                'enter "m" to return to the previous menu):\n')
            while True:
                if inp == 'm':
                    return
                try:
                    if 0 <= int(inp) <= len(ui.current_profile._posts) - 1:
                        a4.u_command(['U', '-post', inp])
                        return
                    else:
                        print('\nPOSTS:')
                        a4.p_command(['P', '-posts'])
                        print('\nThe number you entered was not associated '
                              'with any post.')
                        inp = input(
                            'Please enter a valid ID (or enter "m" to return '
                            'to the previous menu):\n')
                except ValueError:
                    print('\nPOSTS:')
                    a4.p_command(['P', '-posts'])
                    print('\nThe value you entered was not a number.')
                    inp = input('Please enter a valid ID (or enter "m" to '
                                'return to the previous menu):\n')


def c_menu():
    """C command menu"""
    dire = input(
        'Please enter a path (or enter "m" to return to the main menu):\n')
    while True:
        if dire == 'm':
            return
        if Path(dire).is_dir():
            break
        else:
            dire = input(
                'Please enter a valid directory path (or enter "m" to return '
                'to the main menu):\n')

    filename = input('Please select a name for your file (or enter "m" to '
                     'return to the main menu): ')
    if filename == 'm':
        return
    dirpath = Path(dire) / (filename + '.dsu')
    if dirpath.exists():
        a4.c_command(['C', dire, '-n', filename])
        return
    u_usr = check_for_space(usr=True)
    if u_usr == 'm':
        return
    u_pwd = check_for_space(pwd=True)
    if u_pwd == 'm':
        return
    u_bio = check_for_space(bio=True)
    if u_bio == 'm':
        return
    u_dsu = check_for_space(dsu=True)
    if u_dsu == 'm':
        return

    a4.c_command(['C', dire, '-n', filename], usr=u_usr, pwd=u_pwd, bio=u_bio,
                 ip=u_dsu)


def o_menu():
    """O command menu"""
    dire = input(
        'Please enter the path to your DSU file (or enter "m" to return to '
        'the main menu):\n')
    while True:
        if dire == 'm':
            return
        if Path(dire).is_file():
            break
        else:
            dire = input(
                'Please enter a valid path to your DSU file (or enter "m" to '
                'return to the main menu):\n')
    a4.o_command(['O', dire])


def r_menu():
    """R command menu"""
    dire = input(
        'Please enter a path to a DSU file (or enter "m" to return to the '
        'main menu):\n')
    while True:
        if dire == 'm':
            return
        if Path(dire).is_file():
            break
        else:
            dire = input(
                'Please enter a valid path to a DSU file (or enter "m" to '
                'return to the main menu):\n')
    a4.r_command(['R', dire])


def d_menu():
    """D command menu"""
    dire = input(
        'Please enter a path to a DSU file that you want to delete (or enter '
        '"m" to return to the main menu):\n')
    while True:
        if dire == 'm':
            return
        if Path(dire).is_file():
            break
        else:
            dire = input(
                'Please enter a valid path to a DSU file that you want to '
                'delete (or enter "m" to return to the main menu):\n')
    a4.d_command(['D', dire])


def check_for_space(usr=False, pwd=False, bio=False, dsu=False):
    """Checks for spaces in user inputs."""
    while True:
        if usr:
            valid = input('Enter a username (or enter "m" to return to the '
                          'main menu):\n')
            if valid == 'm':
                return 'm'
            elif ' ' in valid:
                print('Your username cannot contain any spaces.')
            elif ' ' not in valid:
                return valid
        elif pwd:
            valid = input('Enter a password (or enter "m" to return to the '
                          'main menu):\n')
            if valid == 'm':
                return 'm'
            elif ' ' in valid:
                print('Your password cannot contain any spaces.')
            elif ' ' not in valid:
                return valid
        elif bio:
            valid = input(
                'Enter a bio (or enter "m" to return to the main menu):\n')
            if valid == 'm':
                return 'm'
            return valid
        elif dsu:
            print('To use the default DSU server, simply hit enter.')
            valid = input('Enter the IP address to a DSU server '
                          '(or enter "m" to return to the '
                          'main menu):')
            if valid == 'm':
                return 'm'
            elif valid == '':
                return '168.235.86.101'
            try:
                ipaddress.ip_address(valid)
                return valid
            except ValueError:
                print('The IP address you entered was invalid.')
