# Mark Nguyen
# markvn@uci.edu
# 84257566

from pathlib import Path

import WebAPI
import ui
import Profile
from datetime import datetime

import user_interface
import ds_client
import json
import OpenWeather as op
import LastFM as fm

signal = 0


def print_directory_and_sub(directory, files_only=False):
    dirpath = Path(directory)
    dirs = []
    fs = []
    for x in dirpath.iterdir():
        if x.is_file():
            fs.append(x)
        elif x.is_dir():
            dirs.append(x)
    if not files_only:
        for f in fs:
            print(f)
        for d in dirs:
            print(d)
            print_directory_and_sub(d)
    elif files_only:
        for f in fs:
            print(f)
        for d in dirs:
            print_directory_and_sub(d, files_only=True)


def print_directory(directory, files_only=False):
    dirpath = Path(directory)
    dirs = []
    fs = []
    for item in dirpath.iterdir():
        if item.is_file():
            fs.append(item)
        elif item.is_dir():
            dirs.append(item)
    if not files_only:
        for f in fs:
            print(f)
        for d in dirs:
            print(d)
    elif files_only:
        for f in fs:
            print(f)


def search_directory(directory, file_searched, recur=False):
    global signal
    dirpath = Path(directory)
    dirs = []
    fs = []
    for item in dirpath.iterdir():
        if item.is_file():
            fs.append(item)
        elif item.is_dir():
            dirs.append(item)
    if not recur:
        for f in fs:
            if f == Path(directory) / file_searched:
                print(f)
        for d in dirs:
            if d == Path(directory) / file_searched:
                print(d)
    elif recur:
        for f in fs:
            if f == Path(directory) / file_searched:
                print(f)
                signal += 1
        for d in dirs:
            if d == Path(directory) / file_searched:
                print(d)
                signal += 1
            search_directory(d, file_searched, recur=True)


def search_directory_ext(directory, ext, recur=False):
    global signal
    dirpath = Path(directory)
    dirs = []
    fs = []
    for item in dirpath.iterdir():
        if item.is_file():
            fs.append(item)
        elif item.is_dir():
            dirs.append(item)
    if not recur:
        for f in fs:
            if Path(f).suffix == ext:
                print(f)
                signal += 1
    elif recur:
        for f in fs:
            if Path(f).suffix == ext:
                print(f)
                signal += 1
        for d in dirs:
            search_directory_ext(d, ext, recur=True)


def l_command(command_list):
    global signal
    signal = 0

    if len(command_list) == 2:
        print_directory(command_list[1])

    elif len(command_list) == 3:
        if command_list[2] == '-r':
            root_dir = command_list[1]
            print_directory_and_sub(root_dir)
        elif command_list[2] == '-f':
            print_directory(command_list[1], files_only=True)
        else:
            print('ERROR')

    elif len(command_list) == 4:
        if command_list[2] == '-r' and command_list[3] == '-f':
            print_directory_and_sub(command_list[1], files_only=True)
        elif command_list[2] == '-s':
            if Path.exists(Path(command_list[1]) / command_list[3]):
                search_directory(command_list[1], command_list[3], recur=False)
            else:
                if user_interface.admin_mode:
                    print('ERROR')
                elif not user_interface.admin_mode:
                    print(f'No files or directories with the name "'
                          f'{command_list[3]}" were found in the given '
                          f'directory.')
                    return False
        elif command_list[2] == '-e':
            ext = command_list[3]
            if '.' not in ext:
                ext = '.' + ext
            search_directory_ext(command_list[1], ext, recur=False)
            if signal == 0:
                if user_interface.admin_mode:
                    print('ERROR')
                elif not user_interface.admin_mode:
                    print(f'No files with the extension "{ext}" were found '
                          f'in the given directory.')
                    return False
        else:
            print('ERROR')

    elif len(command_list) == 5:
        ext = command_list[4]
        if command_list[2] == '-r' and command_list[3] == '-s':
            search_directory(command_list[1], ext, recur=True)
            if signal == 0:
                if user_interface.admin_mode:
                    print('ERROR')
                if not user_interface.admin_mode:
                    print(f'No files or directories with the name "{ext}" '
                          f'were found in the given directory and its '
                          f'subdirectories.')
                    return False
        elif command_list[2] == '-r' and command_list[3] == '-e':
            if '.' not in ext:
                ext = '.' + ext
            search_directory_ext(command_list[1], ext, recur=True)
            if signal == 0:
                if user_interface.admin_mode:
                    print('ERROR')
                elif not user_interface.admin_mode:
                    print(f'No files with the extension "{ext}" were found '
                          f'in the given directory and its subdirectory.')
                    return False
        else:
            print('ERROR')
    else:
        print('ERROR')


def c_command(command_list, usr=None, pwd=None, bio=None, ip='168.235.86.101'):
    filename = command_list[3] + '.dsu'
    filepath = Path(command_list[1]) / filename
    if filepath.exists():
        if user_interface.admin_mode:
            command_list[1] = filepath
            o_command(command_list)
        elif not user_interface.admin_mode:
            print("\nProfile already exists. Loading instead.")
            command_list[1] = filepath
            o_command(command_list)
    else:
        if not user_interface.admin_mode:
            new_profile = Profile.Profile(ip, usr, pwd)
            new_profile.bio = bio
            f = open(filepath, 'w')
            f.close()
            new_profile.save_profile(str(filepath))
            print('\nA file has been created and loaded in the following '
                  'path:')
            print(f'{filepath}')
            ui.current_profile = new_profile
            ui.dire_prof = str(filepath)
            ui.o_c_commands = True
            ui.e_p_menu = True
        elif user_interface.admin_mode:
            f = open(filepath, 'w')
            f.close()
            new_profile = Profile.Profile()
            new_profile.save_profile(str(filepath))
            ui.current_profile = new_profile
            ui.dire_prof = str(filepath)
            ui.o_c_commands = True


def o_command(command_list):
    filepath = command_list[1]
    try:
        if user_interface.admin_mode:
            temp_prof = Profile.Profile()
            temp_prof.load_profile(filepath)
            ui.current_profile = temp_prof
            ui.dire_prof = filepath
            ui.o_c_commands = True
            ui.e_p_menu = True
        elif not user_interface.admin_mode:
            temp_prof = Profile.Profile()
            temp_prof.load_profile(filepath)
            ui.current_profile = temp_prof
            ui.dire_prof = filepath
            print("\nProfile has been loaded.")
            print("\nACCOUNT DETAILS:")
            print(f'Username: {temp_prof.username}\nPassword: '
                  f'{temp_prof.password}')
            ui.o_c_commands = True
            ui.e_p_menu = True
    except Profile.DsuFileError:
        if user_interface.admin_mode:
            print('ERROR')
        elif not user_interface.admin_mode:
            print('DsuFileError')
    except Profile.DsuProfileError:
        if user_interface.admin_mode:
            print('ERROR')
        elif not user_interface.admin_mode:
            print('DsuProfileError')


def e_command(command_list):
    if '-usr' in command_list:
        new_username = command_list[command_list.index('-usr') + 1]
        ui.current_profile.username = new_username
        if user_interface.admin_mode:
            ui.current_profile.save_profile(ui.dire_prof)
        elif not user_interface.admin_mode:
            ui.current_profile.save_profile(ui.dire_prof)
            print(f'\nUsername has been changed to: "{new_username}"')
    if '-pwd' in command_list:
        new_pass = command_list[command_list.index('-pwd') + 1]
        ui.current_profile.password = new_pass
        if user_interface.admin_mode:
            ui.current_profile.save_profile(ui.dire_prof)
        elif not user_interface.admin_mode:
            ui.current_profile.save_profile(ui.dire_prof)
            print(f'\nPassword has been changed to: "{new_pass}"')
    if '-bio' in command_list:
        new_bio = command_list[command_list.index('-bio') + 1]
        ui.current_profile.bio = new_bio
        if user_interface.admin_mode:
            ui.current_profile.save_profile(ui.dire_prof)
        elif not user_interface.admin_mode:
            ui.current_profile.save_profile(ui.dire_prof)
            print(f'\nBio has been changed to: "{new_bio}"')
    if '-addpost' in command_list:
        u_post = command_list[command_list.index('-addpost') + 1]
        try:
            if "@weather" in u_post:
                api_key = input('Please enter your OpenWeather API key (or hit enter to use the default key):\n')
                while True:
                    if not api_key or len(api_key) >= 32:
                        break
                    if len(api_key) < 32:
                        api_key = input('Please enter a valid api key:\n')
                        if api_key == '\n':
                            api_key = ''

                country_code = input('Please enter a country code:\n')
                zip_code = input('Please enter a ZIP code:\n')
                weather_instance = op.OpenWeather(zip_code, country_code)
                weather_instance.load_data()
                if api_key:
                    weather_instance.set_apikey(api_key)
                u_post = weather_instance.transclude(u_post)

            if "@lastfm" in u_post:
                api_key = input(
                    'Please enter your LastFM API key (or hit enter to use the default key):\n')
                while True:
                    if not api_key or len(api_key) >= 32:
                        break
                    if len(api_key) < 32:
                        api_key = input('Please enter a valid api key:\n')
                        if api_key == '\n':
                            api_key = ''

                country = input('Please enter a country:\n')
                country = country.replace(" ", '+')
                print(country)
                fm_instance = fm.LastFM(country)
                fm_instance.load_data()
                if api_key:
                    fm_instance.set_apikey(api_key)
                u_post = fm_instance.transclude(u_post)

            new_post = Profile.Post(u_post)
            ui.current_profile.add_post(new_post)
            if user_interface.admin_mode:
                ui.current_profile.save_profile(ui.dire_prof)
            elif not user_interface.admin_mode:
                print(f'\nThe following post has been added:\n"{u_post}"')
                ui.current_profile.save_profile(ui.dire_prof)

        except WebAPI.Error403:
            print('Invalid Access Key')
        except WebAPI.Error404:
            print('The page you are looking for does not exist')
        except WebAPI.Error503:
            print('Unavailable server. The server is not ready to handle '
                  'your request')
        except Exception:
            print('Invalid API request')

    if '-delpost' in command_list:
        try:
            post_id = int(command_list[command_list.index('-delpost')+1])
            if user_interface.admin_mode:
                ui.current_profile.del_post(post_id)
                ui.current_profile.save_profile(ui.dire_prof)
            elif not user_interface.admin_mode:
                post_dict = ui.current_profile.get_posts()[post_id]
                t = post_dict['timestamp']
                time = datetime.fromtimestamp(t).strftime("%d/%m/%Y %I:%M %p")
                user_post = post_dict['entry']
                print(f'\nThe following post has been deleted:\n')
                print(f'{time}: {user_post}')
                print()
                ui.current_profile.del_post(post_id)
                ui.current_profile.save_profile(ui.dire_prof)
        except IndexError:
            print('ERROR')
    if '-dsu' in command_list:
        ip_ad = command_list[command_list.index('-dsu')+1]
        ui.current_profile.dsuserver = ip_ad
        if user_interface.admin_mode:
            ui.current_profile.save_profile(ui.dire_prof)
        elif not user_interface.admin_mode:
            ui.current_profile.save_profile(ui.dire_prof)
            print(f'\nServer IP address has been changed to: "{ip_ad}"')


def p_command(command_list):
    if '-usr' in command_list:
        print(f'Username: {ui.current_profile.username}')
    if '-pwd' in command_list:
        print(f'Password: {ui.current_profile.password}')
    if '-bio' in command_list:
        print(f'Bio: {ui.current_profile.bio}')
    if '-posts' in command_list:
        if user_interface.admin_mode:
            list_posts = ui.current_profile.get_posts()
            for i in range(len(list_posts)):
                post_i = list_posts[i]
                post_entry = post_i['entry']
                time = datetime.fromtimestamp(post_i['timestamp']).strftime(
                    "%d/%m/%Y %I:%M %p")
                print(f'{time}: {post_entry}')
        elif not user_interface.admin_mode:
            list_posts = ui.current_profile.get_posts()
            for i in range(len(list_posts)):
                post_i = list_posts[i]
                post_entry = post_i['entry']
                time = datetime.fromtimestamp(post_i['timestamp']).strftime(
                    "%d/%m/%Y %I:%M %p")
                print(f'({i}) {time}: {post_entry}')
        elif not user_interface.admin_mode:
            list_posts = ui.current_profile.get_posts()
            for i in range(len(list_posts)):
                post_i = list_posts[i]
                post_entry = post_i['entry']
                time = datetime.fromtimestamp(post_i['timestamp']).strftime(
                    "%d/%m/%Y %I:%M %p")
                print(f'{time}: {post_entry}')
    if '-post' in command_list:
        try:
            if int(command_list[command_list.index('-post') + 1]) >= 0:
                posts = ui.current_profile.get_posts()
                post_id = int(command_list[command_list.index('-post') + 1])
                post = posts[post_id]
                if user_interface.admin_mode:
                    print(post)
                elif not user_interface.admin_mode:
                    x = post['timestamp']
                    time = datetime.fromtimestamp(x).strftime("%d/%m/%Y "
                                                              "%I:%M %p")
                    user_post = post['entry']
                    print(f'{time}: {user_post}')
        except IndexError:
            print('ERROR')
    if '-all' in command_list:
        if user_interface.admin_mode:
            list_posts = ui.current_profile.get_posts()
            print(f'Username: {ui.current_profile.username}')
            print(f'Password: {ui.current_profile.password}')
            print(f'Bio: {ui.current_profile.bio}')
            for i in range(len(list_posts)):
                post_i = list_posts[i]
                post_entry = post_i['entry']
                time = datetime.fromtimestamp(post_i['timestamp']).strftime(
                    "%d/%m/%Y %I:%M %p")
                print(f'{time}: {post_entry}')
        elif not user_interface.admin_mode:
            list_posts = ui.current_profile.get_posts()
            print(f'Username: {ui.current_profile.username}')
            print(f'Password: {ui.current_profile.password}')
            print(f'Bio: {ui.current_profile.bio}')
            for i in range(len(list_posts)):
                post_i = list_posts[i]
                post_entry = post_i['entry']
                time = datetime.fromtimestamp(post_i['timestamp']).strftime(
                    "%d/%m/%Y %I:%M %p")
                print(f'{time}: {post_entry}')


def u_command(command_list):
    usr = ui.current_profile.username
    pwd = ui.current_profile.password
    ip_ad = ui.current_profile.dsuserver
    if '-bio' in command_list:
        bio = ui.current_profile.bio
        ds_client.send(ip_ad, 3021, usr, pwd, '', bio)
    if '-post' in command_list:
        try:
            if int(command_list[command_list.index('-post') + 1]) >= 0:
                posts = ui.current_profile.get_posts()
                post_id = int(command_list[command_list.index('-post') + 1])
                post = posts[post_id]
                post = post['entry']
                x = ds_client.send('168.235.86.101', 3021, usr, pwd, post)
                if not user_interface.admin_mode:
                    if not x:
                        print('Error while processing request.')
        except IndexError:
            print('ERROR')


def r_command(command_list):
    pathname = command_list[1]
    if user_interface.admin_mode:
        if pathname[-3:] == 'dsu':
            f = Path(pathname).open('r')
            if Path(pathname).stat().st_size != 0:
                for line in f:
                    temp = line[:-1]
                    print(temp)
            else:
                print('EMPTY')
            f.close()
        else:
            print('ERROR')
    elif not user_interface.admin_mode:
        if pathname[-3:] == 'dsu':
            f = Path(pathname).open('r')
            if Path(pathname).stat().st_size != 0:
                print('\nDSU FILE CONTENTS:\n')
                for line in f:
                    temp = line[:-1]
                    print(temp)
                print()
            else:
                print('EMPTY')
            f.close()
        else:
            print('The R-command can only read DSU files.')


def d_command(command_list):
    if user_interface.admin_mode:
        pathname = command_list[1]
        if pathname[-3:] == 'dsu':
            Path(pathname).unlink()
            print(pathname)
        else:
            print('ERROR')
    elif not user_interface.admin_mode:
        pathname = command_list[1]
        if pathname[-3:] == 'dsu':
            Path(pathname).unlink()
            print("\nThe following path has been DELETED:\n")
            print(pathname)
            print()
        else:
            print('\nThe following path has NOT been DELETED becuase it '
                  'leads to a file that is not a DSU file:\n')
            print(pathname)
            print()


if __name__ == "__main__":
    command_list_1 = ''
    if not user_interface.admin_mode:
        user_interface.user_mode()
    if user_interface.admin_mode:
        while command_list_1 != 'Q':
            command_list_1 = ui.fetch_command_list()
            ui.commands(command_list_1)

    # def test_api(message: str, apikey: str, webapi: WebAPI):
    #     webapi.set_apikey(apikey)
    #     webapi.load_data()
    #     result = webapi.transclude(message)
    #     print(result)
    #
    # open_weather = op.OpenWeather()  # notice there are no params here...HINT: be sure to use parameter defaults!!!
    # lastfm = fm.LastFM()
    #
    # test_api("Testing the weather: @weather", '857a6b008fb4dc3d4496517d7514a4b0', open_weather)
    # # expected output should include the original message transcluded with the default weather value for the @weather keyword.
    #
    # test_api("Testing lastFM: @lastfm", '4b4aed6a43a67671b28e3af38ba07edc', lastfm)
    # # # expected output include the original message transcluded with the default music data assigned to the @lastfm keyword
