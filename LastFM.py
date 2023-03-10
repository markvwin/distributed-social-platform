"""
Mark Nguyen
markvn&uci.edu
84257566
"""

# 4b4aed6a43a67671b28e3af38ba07edc

import urllib, json
from urllib import request, error
from WebAPI import WebAPI


class LastFM(WebAPI):
    def __init__(self, ccode: str='united+states'):
        super().__init__()
        self.ccode = ccode
        self.api_key = "4b4aed6a43a67671b28e3af38ba07edc"  # Default key
        self.top_artist = None

    def load_data(self) -> None:
        """
        Calls the web api using the required values and stores the response in
        class data attributes.
        """

        url = f"http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists" \
              f"&country={self.ccode}&ap" \
              f"i_key={self.api_key}&format=json&limit=5"

        lastfm_obj = super()._download_url(url)
        if lastfm_obj is not None:
            try:
                self.top_artist = lastfm_obj['topartists']['artist'][0]['name']
            except (IndexError, KeyError):
                print('KeyError: Invalid data format')

    def transclude(self, message: str) -> str:
        """
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude

        :returns: The transcluded message
        """
        if "@lastfm" in message:
            t_message = message.replace('@lastfm', self.top_artist)
            return t_message


def main() -> None:
    apikey = "4b4aed6a43a67671b28e3af38ba07edc"
    ccode = 'united+states'

    last_fm = LastFM(ccode)
    last_fm.set_apikey(apikey)
    last_fm.load_data()

    print(f'\\\\*{last_fm.top_artist}*//')


if __name__ == '__main__':
    main()
