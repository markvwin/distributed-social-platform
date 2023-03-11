import OpenWeather as op
import LastFM as fm
import WebAPI
import pytest


def nottest(obj):
    obj.__test__ = False
    return obj

@nottest
def test_api(message:str, apikey:str, webapi:WebAPI):
    webapi.set_apikey(apikey)
    webapi.load_data()


def test_download_url_and_transclude():
    open_weather = op.OpenWeather()
    lastfm = fm.LastFM()
    o_key = '857a6b008fb4dc3d4496517d7514a4b0'
    f_key = '4b4aed6a43a67671b28e3af38ba07edc'
    o_message = "Testing the weather: @weather"
    f_message = "Testing lastFM: @lastfm"
    test_api(o_message, o_key, open_weather)
    test_api(f_message, f_key, lastfm)
    o_result = open_weather.transclude(o_message)
    f_result = lastfm.transclude(f_message)
    assert o_result != o_message
    assert f_result != f_message


def test_web_api_401_error():
    with pytest.raises(WebAPI.Error401):
        open_weather = op.OpenWeather()
        o_key = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        o_result = test_api('@weather', o_key, open_weather)


def test_web_api_403_error():
    with pytest.raises(WebAPI.Error403):
        last_fm = fm.LastFM()
        ccode = 'united+states'
        api_key = 'InvalidKey'
        url = f"http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists" \
              f"&country={ccode}&ap" \
              f"i_key={api_key}&format=json&limit=5"
        last_fm._download_url(url)


def test_webapi_404_error():
    with pytest.raises(WebAPI.Error404):
        open_weather = op.OpenWeather()
        zipcode = '92617'
        ccode = 'US'
        api_key = '857a6b008fb4dc3d4496517d7514a4b0'
        url = f"http://api.openweathermap.org/data/INVALIDPAGE/weather?={zipcode},{ccode}&appid={api_key}"
        open_weather._download_url(url)


def test_webapi_http_client_invalid_url():
    with pytest.raises(WebAPI.InvalidURLError):
        open_weather = op.OpenWeather()
        zipcode = '92617'
        ccode = 'US'
        api_key = '857a6b008fb4dc3d44 96517d7514a4b0'
        url = f"http://api.openweathermap.org/data/INVALIDPAGE/weather?={zipcode},{ccode}&appid={api_key}"
        open_weather._download_url(url)


def test_webapi_value_error():
    with pytest.raises(WebAPI.InvalidURLError):
        open_weather = op.OpenWeather()
        url = f"a"
        open_weather._download_url(url)


def test_invalid_data_format():
    with pytest.raises(WebAPI.InvalidDataFormatError):
        open_weather = op.OpenWeather()
        url = f'http://api.openweathermap.org/'
        open_weather._download_url(url)

