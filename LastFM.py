"""
Mark Nguyen
markvn&uci.edu
84257566
"""

# 4b4aed6a43a67671b28e3af38ba07edc

import urllib, json
from urllib import request, error


class Error403(Exception):
    pass


class Error404(Exception):
    pass


class Error503(Exception):
    pass


class LastFM:
    def __init__(self, ccode):
        self.ccode = ccode
        self.api_key = None
        self.top_artist = None

    def set_apikey(self, apikey: str) -> None:
        """
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service
        """
        self.api_key = apikey

    def load_data(self) -> None:
        """
        Calls the web api using the required values and stores the response in
        class data attributes.
        """

        url = f"/2.0/?method=tag.gettoptracks&tag=disco&api_key={self.api_key}&format=json&limit=1"

        lastfm_obj = _download_url(url)
        if lastfm_obj is not None:
            try:
                self.top_artist = lastfm_obj['topartists'][0]['name']
            except (IndexError, KeyError):
                print('KeyError: Invalid data format')


def _download_url(url_to_download: str) -> dict:
    response = None
    r_obj = None

    try:
        response = urllib.request.urlopen(url_to_download)
        json_results = response.read()
        r_obj = json.loads(json_results)

    except urllib.error.HTTPError as He:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(He.code))
        if He.code == 403:
            raise Error403('Invalid Access Key', He)
        elif He.code == 404:
            raise Error404('The page you are looking for does not exist', He)
        elif He.code == 503:
            raise Error503('Unavailable server. The server is not ready to '
                           'handle your request', He)

    except urllib.error.URLError as Ue:
        print('Failed to download contents of URL')
        print('Reason: {}'.format(Ue.reason))

    except json.JSONDecodeError as Je:
        print('JSONDecodeError: Invalid data format')

    except ValueError as Ve:
        print('Failed to download contents of URL')
        print('ValueError: Invalid URL')

    finally:
        if response is not None:
            response.close()

    return r_obj


def main() -> None:
    apikey = "4b4aed6a43a67671b28e3af38ba07edc"
    ccode = 'united+states'
    url = f"http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country={ccode}&api_key={apikey}&format=json&limit=5"

    weather_obj = _download_url(url)
    if weather_obj is not None:
        print(weather_obj)
        print(weather_obj.top_artist)




if __name__ == '__main__':
    main()
