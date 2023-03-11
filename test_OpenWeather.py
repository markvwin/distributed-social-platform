"""
Mark Nguyen
markvn@uci.edu
84257566
"""

import OpenWeather as op


def test_api_request_success():
    weather_instance = op.OpenWeather()
    weather_instance.load_data()


def test_open_weather_transclusion():
    weather_instance = op.OpenWeather()
    weather_instance.load_data()
    message = 'Weather test: @weather'
    transcluded_message = weather_instance.transclude(message)
    assert transcluded_message != message


def test_open_weather_attributes_are_loaded():
    weather_instance = op.OpenWeather()
    weather_instance.load_data()
    assert weather_instance.temperature is not None
    assert weather_instance.high_temperature is not None
    assert weather_instance.low_temperature is not None
    assert weather_instance.longitude is not None
    assert weather_instance.latitude is not None
    assert weather_instance.description is not None
    assert weather_instance.humidity is not None
    assert weather_instance.city is not None
    assert weather_instance.sunset is not None
