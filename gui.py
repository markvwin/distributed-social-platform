import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from typing import Text

import ds_messenger
import Profile
import ui
import time
from datetime import datetime
from pathlib import Path
import json


class Body(tk.Frame):
    """ The body generates the treeview on the left hand side of the GUI """
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        """
        node_select is correlated with clicking on any of the boxes in the tree
        view.
        """
        if self.posts_tree.selection():
            index = int(self.posts_tree.selection()[0])
            entry = self._contacts[index]
            if self._select_callback is not None:
                self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message: str):
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')
        self.entry_editor.configure(state='disabled')

    def insert_contact_message(self, message:str):
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')
        self.entry_editor.configure(state='disabled')

    def bottom_insert_user_message(self, message: str):
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')
        self.entry_editor.configure(state='disabled')

    def bottom_insert_contact_message(self, message:str):
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')
        self.entry_editor.configure(state='disabled')

    def clear_text_widget(self):
        self.entry_editor.configure(state='normal')
        self.entry_editor.delete('1.0', tk.END)
        self.entry_editor.configure(state='disabled')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

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
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20)
        save_button.bind("<Button-1>", self.send_click)
        self.root.bind('<Return>', self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def apply(self, *args):
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
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
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
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
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
        self.open = True
        self.destroy()

    def new_profile(self):
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
        self.after_running = True
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.


        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        close = self.start_up()
        # print(self.friends)
        if self.login:
            self.load_treeview()
            self.direct_messenger = ds_messenger.DirectMessenger(self.server, self.username, self.password)
        # if close is False:
        #     self.root.destroy()

            # self.body.insert_contact("SukmaD") # adding one example student.
        # self.body.insert_contact("hi")

    def send_message(self):
        # You must implement this!
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
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list

    def recipient_selected(self, recipient):
        self.recipient = recipient
        self.load_messages(recipient)
        self.body.entry_editor.yview_moveto(1)

    def load_new_messages(self, recipient):
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
        self.body.posts_tree.configure(selectmode='none')
        for item in self.body.posts_tree.get_children():
            self.body.posts_tree.delete(item)
        self.body.posts_tree.configure(selectmode='browse')
        self.current_profile.friends.sort()
        for i in range(len(self.current_profile.friends)):
            self.body.insert_contact(self.current_profile.friends[i])

    def configure_server(self):
        new_contact = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        if new_contact.pwd != self.password:
            ans = messagebox.askquestion('Are you sure?', 'You will lose all online data connected to your account.')
            if ans == 'yes':
                if self.username == new_contact.user:
                    messagebox.showerror('Change Username', 'If you change your password, you must also change your username. ')
                    return
                self.password = new_contact.pwd
            elif ans == 'no':
                return
        valid = self.validate_account_info(new_contact.server, new_contact.user, new_contact.pwd)
        if valid:
            self.username = new_contact.user
            self.password = new_contact.pwd
            self.server = new_contact.server

            self.direct_messenger = ds_messenger.DirectMessenger(self.server,
                                                                 self.username,
                                                                 self.password)
            self.current_profile.username = new_contact.user
            self.current_profile.password = new_contact.pwd
            self.current_profile.dsuserver = new_contact.server
            self.current_profile.save_profile(self.filepath)
        else:
            return

    def publish(self, message:str):
        # You must implement this!
        pass

    def check_new(self):
        if self.after_running:
            self.load_new_messages(self.recipient)
        self.root.after(1000, self.check_new)

    def retrieve_all(self):
        all_messages = self.direct_messenger.retrieve_all()
        self.current_profile.load_profile(self.filepath)

    def create_new_message_log(self, recipient):

        sorted_msg_log = sorted(self.new_messages, key=lambda x: list(x.keys())[0],
                                reverse=True)
        return sorted_msg_log

    def create_message_log(self, recipient):
        un_msgs = []
        for i in range(len(self.current_profile.my_messages)):
            recip = self.current_profile.my_messages[i]['recipient']
            if recip == recipient:
                msg = self.current_profile.my_messages[i]['message']
                timestamp = float(self.current_profile.my_messages[i]['timestamp'])
                temp_dict = {timestamp: ['me', msg]}
                un_msgs.append(temp_dict)

        for i in range(len(self.current_profile.messages)):
            recip = self.current_profile.messages[i]['recipient']
            if recip == recipient:
                msg = self.current_profile.messages[i]['message']
                timestamp = float(self.current_profile.messages[i]['timestamp'])
                temp_dict = {timestamp: [recipient, msg]}
                un_msgs.append(temp_dict)
        sorted_msg_log = sorted(un_msgs, key=lambda x: list(x.keys())[0], reverse=True)
        return sorted_msg_log

    def validate_account_info(self, ip, user, pwd):
        temp_msg = ds_messenger.DirectMessenger(ip, user, pwd)
        resp = temp_msg.check_response()
        if not resp:
            messagebox.showerror('Connection Error', 'Please check your connection.')
            return False
        elif resp:
            if resp.type == 'error':
                messagebox.showerror('Oops', resp.message)
                return False
            elif resp.type == 'ok':
                messagebox.showinfo('ICS 32 Distributed Social Messenger', resp.message)
                return True

    def new_profile(self):
        file = tk.filedialog.asksaveasfilename(defaultextension='.dsu', filetypes=[('DSU File', '.dsu')])
        if file:
            new_prof = NewProfileDialog(self.root, "Create A New Profile")

            if "" not in [new_prof.server, new_prof.user,
                          new_prof.pwd] and None not in [new_prof.server,
                                                         new_prof.user,
                                                         new_prof.pwd]:
                valid = self.validate_account_info(new_prof.server, new_prof.user, new_prof.pwd)
                if valid:
                    new_file = open(file, 'w')
                    new_file.close()

                    self.current_profile = Profile.Profile(new_prof.server, new_prof.user, new_prof.pwd)
                    if new_prof.bio is None:
                        new_prof.bio = ''
                    self.current_profile.bio = new_prof.bio
                    self.current_profile.save_profile(rf'{file}')

                    self.server = new_prof.server
                    self.username = new_prof.user
                    self.password = new_prof.pwd
                    self.filepath = file
                    ui.logged_in = True
                    ui.dire_prof = file  # loads filepath into G variable for
                                         # other modules

                    if self.login:
                        self.after_running = False
                    self.direct_messenger = ds_messenger.DirectMessenger(
                        self.server,
                        self.username,
                        self.password)

                    excess_msgs = self.direct_messenger.retrieve_new()

                    self.retrieve_all()
                    self.load_treeview()
                    self.body.clear_text_widget()
                    self.login = True
                    self.after_running = True
                else:
                    return
            else:
                messagebox.showerror('Unable To Create A Profile',
                                     'A username, password, and server is required.')

    def open_profile(self):
        path = tk.filedialog.askopenfilename(filetypes=[("DSU Files", "*.dsu")])
        try:
            if path:
                temp = Profile.Profile()
                temp.load_profile(path)
                temp.save_profile(path)
                self.username = temp.username
                self.password = temp.password
                self.server = temp.dsuserver
                self.filepath = path
                ui.dire_prof = path
                ui.logged_in = True
                self.current_profile = temp

                if self.login:
                    self.after_running = False
                self.direct_messenger = ds_messenger.DirectMessenger(self.server,
                                                                     self.username,
                                                                     self.password)

                excess_msgs = self.direct_messenger.retrieve_new()

                self.retrieve_all()
                self.load_treeview()
                self.body.clear_text_widget()
                self.login = True
                self.after_running = True

        except Profile.DsuProfileError:
            messagebox.showerror('DSU File Error', 'Invalid DSU file formatting.')

    def start_up(self):
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
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    main.minsize(main.winfo_width(), main.winfo_height())
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()

    id = main.after(1000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()