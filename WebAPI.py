"""
Mark Nguyen
84257566
markvn@uci.edu
"""

from abc import ABC, abstractmethod
import urllib
import json
from urllib import request
from urllib import error
import http.client


class Error401(Exception):
    """Error401 Exception caused by Invalid Key"""
    def __init__(self, *args: object):
        super().__init__(args)
        self.message = args[0]


class Error403(Exception):
    """Error403 Exception caused by Invalid Key"""
    def __init__(self, *args: object):
        super().__init__(args)
        self.message = args[0]


class Error404(Exception):
    """Error404 Exception caused by Invalid URL"""
    def __init__(self, *args: object):
        super().__init__(args)
        self.message = args[0]


class Error503(Exception):
    """Error503 Exception caused if a server is down"""
    def __init__(self, *args: object):
        super().__init__(args)
        self.message = args[0]


class LossConnectionError(Exception):
    """Exception caused if network disconnects during request or before"""
    def __init__(self, *args: object):
        super().__init__(args)
        self.message = args[0]


class InvalidURLError(Exception):
    """Exception caused by an InvalidURL"""
    def __init__(self, *args: object):
        super().__init__(args)
        self.message = args[0]


class InvalidDataFormatError(Exception):
    """Exception caused if receiving an invalid data format"""
    def __init__(self, *args: object):
        super().__init__(args)
        self.message = args[0]


class WebAPI(ABC):
    """Abstract class that API modules inherit from"""
    def __init__(self):
        pass

    def _download_url(self, url: str) -> dict:

        response = None
        r_obj = None

        try:
            response = urllib.request.urlopen(url)
            json_results = response.read()
            r_obj = json.loads(json_results)

        except urllib.error.HTTPError as h_e:
            print('Failed to download contents of URL')
            print(f'Status code: {h_e.code}')
            if h_e.code == 401:
                raise Error401('Invalid Access Key', h_e) from h_e
            if h_e.code == 403:
                raise Error403('Invalid Access', h_e) from h_e
            if h_e.code == 404:
                raise Error404(
                    'The page you are looking for does not exist', h_e) from\
                    h_e
            if h_e.code == 503:
                raise Error503(
                    'Unavailable server. The server is not ready to '
                    'handle your request', h_e) from h_e

        except urllib.error.URLError as u_e:
            print('Failed to download contents of URL')
            print(f'Reason: {u_e.reason}')
            raise LossConnectionError('Connection Error', u_e) from u_e

        except http.client.InvalidURL as i_u:
            print('Failed to download contents of URL')
            raise InvalidURLError('Invalid URL', i_u) from i_u

        except json.JSONDecodeError as d_e:
            raise InvalidDataFormatError('JSONDecodeError: Invalid data '
                                         'format', d_e) from d_e

        except ValueError as v_e:
            print('Failed to download contents of URL')
            raise InvalidURLError('Invalid URL', v_e) from v_e

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
        """Requires child classes to have a load_data method"""

    @abstractmethod
    def transclude(self, message: str) -> str:
        """Requires child classes to have a transclude method"""
