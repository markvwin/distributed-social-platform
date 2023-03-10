from abc import ABC, abstractmethod
import urllib, json
from urllib import request, error


class Error403(Exception):
    pass


class Error404(Exception):
    pass


class Error503(Exception):
    pass


class WebAPI(ABC):

    def __init__(self):
        pass
        # self.api_key = None

    def _download_url(self, url: str) -> dict:
        # TODO: Implement web api request code in a way that supports ALL types of web APIs

        response = None
        r_obj = None

        try:
            response = urllib.request.urlopen(url)
            json_results = response.read()
            r_obj = json.loads(json_results)

        except urllib.error.HTTPError as He:
            print('Failed to download contents of URL')
            print('Status code: {}'.format(He.code))
            if He.code == 403:
                raise Error403('Invalid Access Key', He)
            elif He.code == 404:
                raise Error404(
                    'The page you are looking for does not exist', He)
            elif He.code == 503:
                raise Error503(
                    'Unavailable server. The server is not ready to '
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

    def set_apikey(self, apikey: str) -> None:
        """
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service
        """
        self.api_key = apikey


    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def transclude(self, message: str) -> str:
        pass