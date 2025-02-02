"""
Mark Nguyen
markvn@uci.edu
84257566
"""

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox

import ds_messenger
import Profile
import time
from datetime import datetime


class Body(tk.Frame):
    """ The body generates the treeview on the left hand side of the GUI """

    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        """selects a node"""
        if self.posts_tree.selection():
            index = int(self.posts_tree.selection()[0])
            entry = self._contacts[index]
            if self._select_callback is not None:
                self._select_callback(entry)

    def insert_contact(self, contact: str):
        """inserts a contact into the treeview"""
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        """helps the above method insert a contact into the treeview"""
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message: str):
        """inserts a user message in the message log"""
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')
        self.entry_editor.configure(state='disabled')

    def insert_contact_message(self, message: str):
        """inserts the contact's message in the message log"""
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')
        self.entry_editor.configure(state='disabled')

    def bottom_insert_user_message(self, message: str):
        """inserts the user's message at the bottom of the log"""
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')
        self.entry_editor.configure(state='disabled')

    def bottom_insert_contact_message(self, message: str):
        """inserts the contact's message at the bottom of the log"""
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')
        self.entry_editor.configure(state='disabled')

    def clear_text_widget(self):
        """Clears the text widget"""
        self.entry_editor.configure(state='normal')
        self.entry_editor.delete('1.0', tk.END)
        self.entry_editor.configure(state='disabled')

    def get_text_entry(self) -> str:
        """Gets the text entry"""
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """Sets the text entry"""
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=0)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.configure(state="disabled")
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self, event):
        """Sends a click to the callback function"""
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20,
                                bg='#ADD8E6')
        save_button.bind("<Button-1>", self.send_click)
        self.root.bind('<Return>', self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def apply(self, *args):
        """gets the entries from the dialog boxes"""
        self.server = self.server_entry.get().rstrip()
        self.user = self.username_entry.get().rstrip()
        self.pwd = self.password_entry.get().rstrip()

    def body(self, frame):
        server_label = tk.Label(frame, width=30, text="DS Server Address")
        server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        username_label = tk.Label(frame, width=30, text="Username")
        username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        password_label = tk.Label(frame, width=30, text="Password")
        password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def buttonbox(self):
        """the button box"""
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok,
                      default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()


class NewProfileDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None):
        self.root = root
        self.server = None
        self.user = None
        self.pwd = None
        self.bio = None
        super().__init__(root, title)

    def apply(self, *args):
        """gets the entries from the dialog boxes"""
        self.server = self.server_entry.get().rstrip()
        self.user = self.username_entry.get().rstrip()
        self.pwd = self.password_entry.get().rstrip()
        self.bio = self.bio_entry.get().rstrip()

    def body(self, frame):
        server_label = tk.Label(frame, width=30, text="DS Server Address")
        server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, "168.235.86.101")
        self.server_entry.pack()

        username_label = tk.Label(frame, width=30, text="Username")
        username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.pack()

        password_label = tk.Label(frame, width=30, text="Password")
        password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry.pack()

        bio_label = tk.Label(frame, width=30, text="Bio (optional)")
        bio_label.pack()
        self.bio_entry = tk.Entry(frame, width=30)
        self.bio_entry.pack()

    def buttonbox(self):
        """this is a buttonbox method"""
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok,
                      default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()


class CreateOrOpenFileDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None):
        self.root = root
        self.open = False
        self.new = False
        super().__init__(root, title)

    def open_profile(self):
        """opens the user's profile"""
        self.open = True
        self.destroy()

    def new_profile(self):
        """creates a new profile for the user"""
        self.new = True
        self.destroy()

    def body(self, frame):
        server_label = tk.Label(frame, width=30,
                                text="Please select an option")
        server_label.pack()

    def buttonbox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="Open existing profile", width=20,
                      command=self.open_profile, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Create a new profile", width=20,
                      command=self.new_profile)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.open_profile)
        self.bind("<Escape>", self.cancel)

        box.pack()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.filepath = None
        self.current_profile = None
        self.login = False
        self.new_messages = []
        self.status = tk.StringVar(self.root, value="OFFLINE")
        self.check_val = tk.IntVar(self.root, value=0)

        self._draw()
        self.start_up()

        if self.login:
            self.load_treeview()
            self.direct_messenger = ds_messenger.DirectMessenger(self.server,
                                                                 self.username,
                                                                 self.password)

    def online_switch(self):
        """function that turns works with online/offline functionality"""
        try:
            if self.status.get() == "OFFLINE":
                server = self.server
                user = self.username
                pwd = self.password
                eligible = self.validate_online_eligibility(server, user, pwd)
                if eligible:
                    self.go_online()
                    self.status.set('ONLINE')
                    self.label.config(fg='green')
                    self.check_val.set(1)
                else:
                    self.check_val.set(0)
                    self.status.set('OFFLINE')
                    self.label.config(fg='red')
            elif self.status.get() == 'ONLINE':
                self.status.set('OFFLINE')
                self.label.config(fg='red')
                self.check_val.set(0)
        except OSError:
            messagebox.showerror('Meow',
                                 'It seems like your cat has been messing '
                                 'with the router again. Please check your '
                                 'connection before going online.')
            self.status.set('OFFLINE')
            self.label.config(fg='red')
            self.check_val.set(0)

    def go_online(self):
        """procedure for going online"""
        excess_msgs = self.direct_messenger.retrieve_new()
        self.retrieve_all()
        self.load_treeview()

    def send_message(self):
        """method for sending a message"""
        if self.recipient and self.status.get() == 'ONLINE':

            if self.recipient not in self.current_profile.friends:
                self.current_profile.friends.append(self.recipient)
                self.current_profile.save_profile(self.filepath)

            entry = self.body.get_text_entry()
            self.body.set_text_entry('')
            self.direct_messenger.send(entry, self.recipient)
            temp_msg = ds_messenger.DirectMessage()
            temp_msg.message = entry
            temp_msg.recipient = self.recipient
            temp_msg.timestamp = float(time.time())
            msg_dict = {temp_msg.timestamp: ['me', temp_msg.message]}
            self.new_messages.append(msg_dict)

    def add_contact(self):
        """method for adding a contact"""
        name = tk.simpledialog.askstring('New Contact', 'Username')
        if name:
            if name not in self.current_profile.friends:
                self.current_profile.friends.append(name)
                self.current_profile.save_profile(self.filepath)
                self.body.insert_contact(name)
            else:
                return
        else:
            return

    def recipient_selected(self, recipient):
        """method for selecting a recipient"""
        self.recipient = recipient
        self.load_messages(recipient)
        self.body.entry_editor.yview_moveto(1)

    def load_new_messages(self, recipient):
        """method for loading new messages"""
        new_messages = self.direct_messenger.retrieve_new()
        if not new_messages and not self.new_messages:
            return
        else:
            self.current_profile.load_profile(self.filepath)
            if new_messages:
                for i in range(len(new_messages)):
                    msg = new_messages[i].message
                    recip = new_messages[i].recipient
                    ti_me = float(new_messages[i].timestamp)
                    msg_dict = {ti_me: [recip, msg]}
                    self.new_messages.append(msg_dict)

                    if recip not in self.body._contacts:
                        self.new_messages = []
                        self.body.insert_contact(recip)

            msg_log = self.create_new_message_log(recipient)
            for i, val in enumerate(msg_log):
                if msg_log[i][list(msg_log[i].keys())[0]][0] == 'me':
                    timestamp = list(msg_log[i].keys())[0]
                    msg = msg_log[i][list(msg_log[i].keys())[0]][1]
                    msg_time = datetime.fromtimestamp(timestamp).strftime(
                        "%m/%d/%Y %I:%M %p")
                    self.body.bottom_insert_user_message(msg_time)
                    self.body.bottom_insert_user_message(msg)
                    msg_log.pop(i)
                    self.new_messages.pop(self.new_messages.index(val))

                elif msg_log[i][list(msg_log[i].keys())[0]][0] == recipient:
                    timestamp = list(msg_log[i].keys())[0]
                    msg = msg_log[i][list(msg_log[i].keys())[0]][1]
                    msg_time = datetime.fromtimestamp(timestamp).strftime(
                        "%m/%d/%Y %I:%M %p")
                    self.body.bottom_insert_contact_message(msg_time)
                    self.body.bottom_insert_contact_message(msg)
                    msg_log.pop(i)
                    self.new_messages.pop(self.new_messages.index(val))
                self.body.entry_editor.yview_moveto(1)

    def load_messages(self, recipient):
        """method for loading all messages"""
        self.body.clear_text_widget()
        msg_log = self.create_message_log(recipient)

        for i in range(len(msg_log)):
            if msg_log[i][list(msg_log[i].keys())[0]][0] == 'me':
                timestamp = list(msg_log[i].keys())[0]
                msg = msg_log[i][list(msg_log[i].keys())[0]][1]
                msg_time = datetime.fromtimestamp(timestamp).strftime(
                    "%m/%d/%Y %I:%M %p")
                self.body.insert_user_message(msg)
                self.body.insert_user_message(msg_time)
            elif msg_log[i][list(msg_log[i].keys())[0]][0] == recipient:
                timestamp = list(msg_log[i].keys())[0]
                msg = msg_log[i][list(msg_log[i].keys())[0]][1]
                msg_time = datetime.fromtimestamp(timestamp).strftime(
                    "%m/%d/%Y %I:%M %p")
                self.body.insert_contact_message(msg)
                self.body.insert_contact_message(msg_time)

    def load_treeview(self):
        """method for loading treeview"""
        self.body.posts_tree.configure(selectmode='none')
        for item in self.body.posts_tree.get_children():
            self.body.posts_tree.delete(item)
        self.body.posts_tree.configure(selectmode='browse')
        self.current_profile.friends.sort()
        for i in range(len(self.current_profile.friends)):
            self.body.insert_contact(self.current_profile.friends[i])

    def configure_account(self):
        """method for configuring account details"""
        new_contact = NewContactDialog(self.root, "Configure Account",
                                       self.username, self.password,
                                       self.server)
        if new_contact.pwd != self.password:
            ans = messagebox.askquestion('Are you sure?', 'You will lose all '
                                                          'online data '
                                                          'connected to your '
                                                          'account.')
            if ans == 'yes':
                if self.username == new_contact.user:
                    messagebox.showerror('Change Username',
                                         'If you change your password, you '
                                         'must also change your username. ')
                    return
                self.password = new_contact.pwd
            elif ans == 'no':
                return
        valid = False
        server = new_contact.server
        user = new_contact.user
        pwd = new_contact.pwd
        if self.status.get() == 'OFFLINE':
            valid = self.validate_account_info(server, user, pwd)
        elif self.status.get() == 'ONLINE':
            valid = self.validate_online_eligibility(server, user, pwd)
        if valid:
            self.new_messages = []
            self.username = user
            self.password = pwd
            self.server = server

            self.direct_messenger = ds_messenger.DirectMessenger(server, user,
                                                                 pwd)
            self.current_profile.username = user
            self.current_profile.password = pwd
            self.current_profile.dsuserver = server
            self.current_profile.save_profile(self.filepath)
        else:
            if self.status.get() == 'ONLINE':
                self.check_val.set(0)
                self.status.set('OFFLINE')
                self.label.config(fg='red')
            return

    def check_new(self):
        """method for checking new messages and refreshing program"""
        if self.status.get() == 'ONLINE':
            try:
                self.load_new_messages(self.recipient)
            except OSError:
                messagebox.showerror('Meow', 'It seems like your cat has '
                                             'been messing with the router '
                                             'again. Please check your '
                                             'connection before going online.')
                self.online_switch()
        self.root.after(1000, self.check_new)

    def retrieve_all(self):
        """method for retrieving all messages"""
        all_messages = self.direct_messenger.retrieve_all()
        self.current_profile.load_profile(self.filepath)

    def create_new_message_log(self, recipient):
        """method for creating a new messages log"""
        sorted_msg_log = sorted(self.new_messages,
                                key=lambda x: list(x.keys())[0], reverse=True)
        return sorted_msg_log

    def create_message_log(self, recipient):
        """method for creating all messages log"""
        un_msgs = []
        for i in range(len(self.current_profile.my_messages)):
            recip = self.current_profile.my_messages[i]['recipient']
            if recip == recipient:
                msg = self.current_profile.my_messages[i]['message']
                timestamp = float(
                    self.current_profile.my_messages[i]['timestamp'])
                temp_dict = {timestamp: ['me', msg]}
                un_msgs.append(temp_dict)

        for i in range(len(self.current_profile.messages)):
            recip = self.current_profile.messages[i]['recipient']
            if recip == recipient:
                msg = self.current_profile.messages[i]['message']
                timestamp = float(
                    self.current_profile.messages[i]['timestamp'])
                temp_dict = {timestamp: [recipient, msg]}
                un_msgs.append(temp_dict)
        sorted_msg_log = sorted(un_msgs, key=lambda x: list(x.keys())[0],
                                reverse=True)
        return sorted_msg_log

    def validate_account_info(self, server, user, pwd):
        """method for validating account information"""
        if ' ' in [server, user, pwd]:
            messagebox.showerror('Oops',
                                 'Your entries cannot contain whitespace.')
            return False
        if not server or not user or not pwd:
            messagebox.showerror('Oops', 'You you seem to be missing a spot!')
            return False
        return True

    def validate_online_eligibility(self, server, user, pwd):
        """method for validating online eligibility"""
        temp_msg = ds_messenger.DirectMessenger(server, user, pwd)
        resp = temp_msg.check_response()
        if not resp:
            messagebox.showerror('Oops', 'Unable to connect to the DSU server')
            return False
        elif resp:
            if resp.type == 'error':
                messagebox.showerror('Oops', resp.message)
                return False
            elif resp.type == 'ok':
                messagebox.showinfo('ICS 32 Distributed Social Messenger',
                                    resp.message)
                return True

    def new_profile(self):
        """method for creating a new profile"""
        file = tk.filedialog.asksaveasfilename(defaultextension='.dsu',
                                               filetypes=[
                                                   ('DSU File', '.dsu')])
        if file:
            new_prof = NewProfileDialog(self.root, "Create A New Profile")

            server = new_prof.server
            user = new_prof.user
            pwd = new_prof.pwd

            if "" not in [server, user, pwd] and None not in [server, user,
                                                              pwd]:
                valid = self.validate_account_info(server, user, pwd)
                if valid:
                    new_file = open(file, 'w')
                    new_file.close()
                    self.current_profile = Profile.Profile(server, user, pwd)
                    if new_prof.bio is None:
                        new_prof.bio = ''
                    self.current_profile.bio = new_prof.bio
                    self.current_profile.save_profile(rf'{file}')
                    self.server = server
                    self.username = user
                    self.password = pwd
                    self.filepath = file
                    Profile.LOGGED_IN = True
                    Profile.PROFILE_DIRECTORY = file

                    if self.status.get() == 'ONLINE':
                        self.online_switch()  # going offline
                        self.body._contacts = [str]

                    dm_obj = ds_messenger.DirectMessenger(server, user, pwd)
                    self.direct_messenger = dm_obj

                    self.load_treeview()
                    self.body.clear_text_widget()

                    self.login = True  # Responsible on loading data on startup
                else:
                    return
            else:
                messagebox.showerror('Unable To Create A Profile',
                                     'A username, password, and server is '
                                     'required.')

    def open_profile(self):
        """method for opening a existing profile"""
        path = tk.filedialog.askopenfilename(
            filetypes=[("DSU Files", "*.dsu")])
        try:
            if path:
                temp = Profile.Profile()
                temp.load_profile(path)
                temp.save_profile(path)
                self.username = temp.username
                self.password = temp.password
                self.server = temp.dsuserver
                self.filepath = path
                Profile.LOGGED_IN = True
                Profile.PROFILE_DIRECTORY = path
                self.current_profile = temp

                if self.status.get() == 'ONLINE':
                    self.online_switch()  # going offline
                    self.body._contacts = [str]
                self.direct_messenger = ds_messenger.DirectMessenger(
                    self.server, self.username, self.password)

                self.load_treeview()
                self.body.clear_text_widget()
                self.login = True

        except Profile.DsuProfileError:
            messagebox.showerror('DSU File Error', 'Invalid DSU file '
                                                   'formatting.')

    def start_up(self):
        """method for starting up dialog boxes at the begining of program"""
        option = CreateOrOpenFileDialog(self.root, 'Welcome to DS Messenger!')
        if option.new:
            self.new_profile()
        elif option.open:
            self.open_profile()
        else:
            self.root.destroy()
            return False

        if not self.login:  # if user selects an option but closes the
            self.start_up()  # window, then the menu will pop up again.
        else:
            return True

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure Account',
                                  command=self.configure_account)

        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.check_button = tk.Checkbutton(self.root, variable=self.check_val,
                                           command=self.online_switch)
        self.check_button.pack(anchor='w', fill='none', side=tk.LEFT, padx=5,
                               pady=0)

        self.label = tk.Label(master=self.root, textvariable=self.status,
                              fg='red')
        self.label.pack(fill=tk.NONE, side=tk.LEFT, padx=0)

        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


def center(win):
    """
    centers a tkinter window
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


if __name__ == "__main__":

    main = tk.Tk()

    main.title("ICS 32 Distributed Social Messenger")

    main.geometry("720x480")
    center(main)

    main.option_add('*tearOff', False)

    main.minsize(main.winfo_width(), main.winfo_height())
    app = MainApp(main)

    main.update()
    id = main.after(1000, app.check_new)

    main.mainloop()
