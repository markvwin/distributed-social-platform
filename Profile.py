"""
Mark Nguyen
markvn@uci.edu
84257566
"""

import json
import time
from pathlib import Path

CURRENT_PROFILE = None
PROFILE_DIRECTORY = None
LOGGED_IN = False
TOKEN = ''


class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should catch in your
    own
    code. It is raised when attempting to load or save Profile objects to file
    the system.
    """


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch in your
    own code. It
    is raised when attempting to deserialize a dsu file to a Profile object.
    """


class Post(dict):
    """

    The Post class is responsible for working with individual user posts. It
    currently
    supports two features: A timestamp property that is set upon instantiation
    and
    when the entry object is set and an entry property that stores the post
    message.

    """

    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        """Sets entry"""
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        """Gets entry"""
        return self._entry

    def set_time(self, timestamp: float):
        """Sets time for entry"""
        self._timestamp = timestamp
        dict.__setitem__(self, 'timestamp', timestamp)

    def get_time(self):
        """Gets timestamp for entry"""
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """

    The Profile class exposes the properties required to join an ICS 32 DSU
    server. You
    will need to use this class to manage the information provided by each new
    user
    created within your program for a3. Pay close attention to the properties
    and
    functions in this class as you will need to make use of each of them in
    your program.
    When creating your program you will need to collect user input for the
    properties
    exposed by this class. A Profile class should ensure that a username and
    password
    are set, but contains no conventions to do so. You should make sure that
    your code
    verifies that required properties are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''  # OPTIONAL
        self._posts = []  # OPTIONAL
        self.messages = []
        self.my_messages = []
        self.friends = []

    def add_post(self, post: Post) -> None:
        """adds a post"""
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        """
        del_post removes a Post at a given index and returns True if successful
        and
        False if
        an invalid index was supplied.

        To determine which post to delete you must implement your own search
        operation on
        the posts returned from the get_posts function to find the correct
        index.
        """
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:
        """
        get_posts returns the list object containing all posts that have been
        added to the Profile object
        """
        return self._posts

    def save_profile(self, path: str) -> None:
        """
        save_profile accepts an existing dsu file to save the current instance
        of Profile to the file system.

        Example usage:

        profile = Profile()
        profile.save_profile('/path/to/file.dsu')

        Raises DsuFileError
        """
        pat = Path(path)

        if pat.exists() and pat.suffix == '.dsu':
            try:
                with open(pat, 'w') as file:
                    json.dump(self.__dict__, file)
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the "
                                   "DSU file.", ex) from ex
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """

        load_profile will populate the current instance of Profile with data
        stored in a DSU file.

        Example usage:

        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError

        """
        pat = Path(path)

        if pat.exists() and pat.suffix == '.dsu':
            try:
                with open(pat, 'r') as file:
                    obj = json.load(file)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    self.bio = obj['bio']
                    self.messages = obj['messages']
                    self.my_messages = obj['my_messages']
                    self.friends = obj['friends']
                    for post_obj in obj['_posts']:
                        post = Post(post_obj['entry'], post_obj['timestamp'])
                        self._posts.append(post)
            except Exception as ex:
                raise DsuProfileError(ex) from ex
        else:
            raise DsuFileError()
