import json
import urllib.request
import urllib.parse


class Weather:

    LOCATION_NAME = "Quezon City, Philippines"

    LATITUDE = 14.6760
    LONGITUDE = 121.0437

    API_URL = (
        "https://api.open-meteo.com/v1/forecast"
    )

    def __init__(self, state):

        self.state = state

        self.temperature = None

        self.weather_code = None

        self.description = "Unknown"

        self.last_updated = "Not updated"

    # ==========================================
    # WEATHER DESCRIPTION
    # ==========================================

    def get_weather_description(self, code):

        if code == 0:
            return "Clear"

        elif code in (1, 2):
            return "Cloudy"

        elif code == 3:
            return "Overcast"

        elif code in (45, 48):
            return "Fog"

        elif code in (
            51,
            53,
            55,
            56,
            57
        ):
            return "Drizzle"

        elif code in (
            61,
            63,
            65,
            66,
            67
        ):
            return "Rain"

        elif code in (
            71,
            73,
            75,
            77
        ):
            return "Snow"

        elif code in (
            80,
            81,
            82
        ):
            return "Rain"

        elif code in (
            85,
            86
        ):
            return "Snow"

        elif code in (
            95,
            96,
            99
        ):
            return "Storm"

        return "Cloudy"

    # ==========================================
    # UPDATE WEATHER
    # ==========================================

    def update_weather(self):

        try:

            params = {

                "latitude": self.LATITUDE,

                "longitude": self.LONGITUDE,

                "current": (
                    "temperature_2m,"
                    "weather_code,"
                    "is_day,"
                    "precipitation"
                ),

                "timezone": "Asia/Manila"
            }

            url = (
                self.API_URL
                + "?"
                + urllib.parse.urlencode(params)
            )

            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent":
                    "Tofu-Naptime/1.0"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=10
            ) as response:

                data = json.loads(
                    response.read().decode(
                        "utf-8"
                    )
                )

            current = data.get(
                "current",
                {}
            )

            self.temperature = current.get(
                "temperature_2m"
            )

            self.weather_code = current.get(
                "weather_code"
            )

            self.description = (
                self.get_weather_description(
                    self.weather_code
                )
            )

            self.state.set_weather(
                self.description
            )

            self.state.temperature = (
                self.temperature
            )

            self.state.weather_description = (
                self.description
            )

            self.last_updated = current.get(
                "time",
                "Unknown"
            )

            if self.temperature is not None:

                self.state.action_text = (
                    f"Real weather: "
                    f"{self.description} "
                    f"({self.temperature:.0f}°C)"
                )

            else:

                self.state.action_text = (
                    f"Real weather: "
                    f"{self.description}"
                )

            return True

        except Exception as error:

            print(
                "Weather update failed:",
                error
            )

            self.state.action_text = (
                "Unable to get real weather."
            )

            return False

    def random_weather(self):

        return self.update_weather()

    def get_temperature(self):

        return self.temperature

    def get_description(self):

        return self.description