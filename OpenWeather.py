"""
Mark Nguyen
markvn&uci.edu
84257566
"""

# 857a6b008fb4dc3d4496517d7514a4b0

from WebAPI import WebAPI


class OpenWeather(WebAPI):
    """Child class of WebAPI that scrapes data from OpenWeather"""
    def __init__(self, zipcode: str = '92617', ccode: str = 'US'):
        super().__init__()
        self.zipcode = zipcode
        self.ccode = ccode
        self.api_key = "857a6b008fb4dc3d4496517d7514a4b0"
        self.temperature = None
        self.high_temperature = None
        self.low_temperature = None
        self.longitude = None
        self.latitude = None
        self.description = None
        self.humidity = None
        self.city = None
        self.sunset = None

    def load_data(self) -> None:
        """
        Calls the web api using the required values and stores the response in
        class data attributes.
        """

        url = f"http://api.openweathermap.org/data/2.5/weather?zip=" \
              f"{self.zipcode},{self.ccode}&appid={self.api_key}"
        try:
            weather_obj = super()._download_url(url)
            if weather_obj is not None:
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

    def transclude(self, message: str) -> str:
        """
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude

        :returns: The transcluded message
        """
        if "@weather" in message:
            t_message = message.replace('@weather', self.description)
            return t_message
