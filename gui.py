import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from typing import Text

import ds_messenger
import Profile
from pathlib import Path


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

    def insert_user_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

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

    def body(self, frame):
        server_label = tk.Label(frame, width=30, text="DS Server Address")
        server_label.pack()
        server_entry = tk.Entry(frame, width=30)
        server_entry.insert(tk.END, self.server)
        server_entry.pack()
        self.server = server_entry.get()

        username_label = tk.Label(frame, width=30, text="Username")
        username_label.pack()
        username_entry = tk.Entry(frame, width=30)
        username_entry.insert(tk.END, self.user)
        username_entry.pack()
        self.user = username_entry.get()


class NewProfile(tk.simpledialog.Dialog):
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
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        self.direct_messenger = None


        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self.body.insert_contact("studentexw23") # adding one example student.
        self.body.insert_contact("hi")

    def send_message(self):
        # You must implement this!
        entry = self.body.get_text_entry()
        self.direct_messenger.send(entry, self.recipient)
        # pass

    def add_contact(self):
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        pass

    def recipient_selected(self, recipient):
        self.recipient = recipient

    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.
        self.direct_messenger = ds_messenger.DirectMessenger(self.server,
                                                             self.username,
                                                             self.password)

    def publish(self, message:str):
        # You must implement this!
        pass

    def check_new(self):
        # You must implement this!
        pass

    def new_profile(self):
        file = tk.filedialog.asksaveasfilename(defaultextension='.dsu', filetypes=[('DSU File', '.dsu')])
        if file:
            new_prof = NewProfile(self.root, "Create A New Profile")
            if None not in [new_prof.server, new_prof.user, new_prof.pwd]:
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

                self.login = True

    def open_profile(self):
        path = tk.filedialog.askopenfilename(filetypes=[("DSU Files", "*.dsu")])
        if path:
            temp = Profile.Profile()
            temp.load_profile(path)
            self.username = temp.username
            self.password = temp.password
            self.filepath = path

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
        settings_file.add_command(label='Configure DS Server',
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
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()