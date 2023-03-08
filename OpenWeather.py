"""
Mark Nguyen
markvn&uci.edu
84257566
"""

# 857a6b008fb4dc3d4496517d7514a4b0

import urllib, json
from urllib import request, error


class Error403(Exception):
    pass


class Error404(Exception):
    pass


class Error503(Exception):
    pass


class OpenWeather:
    def __init__(self, zipcode, ccode):
        self.zipcode = zipcode
        self.ccode = ccode
        self.api_key = None
        self.temperature = None
        self.high_temperature = None
        self.low_temperature = None
        self.longitude = None
        self.latitude = None
        self.description = None
        self.humidity = None
        self.city = None
        self.sunset = None

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

        url = f"http://api.openweathermap.org/data/2.5/weather?zip=" \
              f"{self.zipcode},{self.ccode}&appid={self.api_key}"

        weather_obj = _download_url(url)
        if weather_obj is not None:
            try:
                self.temperature = weather_obj['main']['temp']
                self.high_temperature = weather_obj['main']['temp_max']
                self.low_temperature = weather_obj['main']['temp_min']
                self.longitude = weather_obj['coord']['lon']
                self.latitude = weather_obj['coord']['lat']
                self.description = weather_obj['weather'][0]['description']
                self.humidity = weather_obj['main']['humidity']
                self.city = weather_obj['name']
                self.sunset = weather_obj['sys']['sunset']
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
    zip = "92697"
    ccode = "US"
    apikey = "857a6b008fb4dc3d4496517d7514a4b0"
    url = f"http://api.openweathermap.org/data/2.5/1/weather?zip={zip}," \
          f"{ccode}&appid={apikey}"

    weather_obj = _download_url(url)
    if weather_obj is not None:
        print(weather_obj['weather'][0]['description'])


if __name__ == '__main__':
    main()
