#API Weather App

import sys
import requests
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name:",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.set_temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.set_temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.set_temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.set_temperature_label.setObjectName("set_temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.get_weather_button.setObjectName("get_weather_button")

        self.setStyleSheet("""
                           QPushButton, QLabel{
                                font-family: Arial;
                           }
                           QLabel#city_label{
                                font-size: 40px;
                                font-style: italic;
                           }
                           QLineEdit#city_input{
                                font-size: 40px;
                                padding: 10px 20px;
                           }
                           QPushButton#get_weather_button{
                                font-size: 30px;
                                font-weight: bold;
                           }
                           QLabel#set_temperature_label{
                                font-size: 75px;
                               
                           }
                           QLabel#emoji_label{
                                font-size: 100px;
                           }
                           QLabel#description_label{
                                font-size: 40px;
                           }""")
        
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "f135fd5560660bbf17c1d3f4b35fa52f"
        city = self.city_input.text()
        limit = 1

        if not city: # If city box is exmpty prompts user to enter a city
            self.display_error("Please enter a city")

        try:
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={api_key}"
            
            geo_response = requests.get(geo_url)
            geo_data = geo_response.json()
            
            
            lat = geo_data[0]["lat"]
            lon = geo_data[0]["lon"]

            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            weather_response.raise_for_status()
        
            if weather_data["cod"] == 200:
                self.display_weather(weather_data)
            else:
                self.display_error(weather_data["message"])
        except requests.exceptions.ConnectionError:
            self.display_error("ConnectionError \n Check your internet connection")
        except requests.exceptions.RequestException:
            match weather_response.status_code:
                case 400:
                    self.display_error("Bad request: \n please check input")
                case 401:
                    self.display_error("Unauthorized: \n unvalid API key")
                case 403:
                    self.display_error("Forbidden: \n Acess is denied")
                case 404:
                    self.display_error("Not found: \n City not found")
                case 500:
                    self.display_error("Internal Server Error: \n Please try again later")
                case 502:
                    self.display_error("Bad Gateway: \n Invalid response from the Server")
                case 503:
                    self.display_error("Service Unavailable: \n Server is down")
                case 504:
                    self.display_error("Gateway Timeout: \n No Response From The Server")
                case _:
                    self.display_error("Uknown error occured")
        except requests.exceptions.HTTPError:
            self.display_error("HTTP Error Occured")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Occured: \n The request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects: \n check the url")
        except IndexError:
            self.display_error(f"Index Error: City: \n {city} is not found")
        except Exception as e:
            self.display_error(f"Unexpected Error: {e}")


        

    def display_error(self,message):
        self.set_temperature_label.setStyleSheet("font-size: 20px")
        self.set_temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,weather_data):
        temp_k = weather_data["main"]["temp"]
        temp_f = (temp_k-273.15)*9/5 + 32
        weather_id = weather_data["weather"][0]["id"]
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.set_temperature_label.setStyleSheet("font-size: 75px")
        self.set_temperature_label.setText(f"{temp_f:.0f}℉")
        weather_description = weather_data["weather"][0]["description"]
        self.description_label.setText(f"{weather_description}")
        

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "☁︎"
        elif 500 <= weather_id <= 531:
            return "⛆"
        elif 600 <= weather_id <= 622:
            return "❅"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☼"
        elif 801 <= weather_id <= 804:
            return "⛅︎"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
