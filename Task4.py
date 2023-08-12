import requests

class WeatherApp:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.favorites = {}
        self.load_favorites()

    def fetch_weather_data(self, location):
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

    def fetch_forecast_data(self, location):
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric",
            "cnt": 40  # Fetch 8 forecasts per day for 5 days (3-hour intervals)
        }
        response = requests.get(self.forecast_url, params=params)
        return response.json()
    
    def load_favorites(self):
        try:
            with open("favorites.txt", "r") as file:
                for line in file:
                    location = line.strip()
                    self.favorites[location] = self.fetch_weather_data(location)
        except FileNotFoundError:
            pass

    def display_weather(self, data):
        print("\nCurrent Weather Data:")
        print(f"Temperature: {data['main']['temp']}°C")
        print(f"Humidity: {data['main']['humidity']}%")
        print(f"Wind Speed: {data['wind']['speed']} m/s")
        print(f"Weather Condition: {data['weather'][0]['description']}")

    def display_forecast(self, data):
        print("\n5-Day Weather Forecast:")
        day_forecasts = {}  # Dictionary to store forecasts for each day

        for forecast in data['list']:
            timestamp = forecast['dt']
            temperature = forecast['main']['temp']
            weather_description = forecast['weather'][0]['description']
            
            # Convert timestamp to human-readable date and time
            from datetime import datetime
            date_time = datetime.fromtimestamp(timestamp)
            day = date_time.strftime("%A")
            
            if day not in day_forecasts:
                day_forecasts[day] = []

            day_forecasts[day].append((date_time.strftime("%H:%M"), temperature, weather_description))

        for day, forecasts in day_forecasts.items():
            print(f"\n{day}'s Forecast:")
            for time, temp, weather in forecasts:
                print(f"{time}: Temperature: {temp}°C, Weather: {weather}")

    def add_favorite(self, location):
        data = self.fetch_weather_data(location)
        self.favorites[location] = data
        with open("favorites.txt", "a") as file:
            file.write(location + "\n")

    def view_favorites(self):
        print("\nFavorite Locations:")
        for location in self.favorites:
            print(location)

    def view_favorite_weather(self):
        if not self.favorites:
            print("No favorite locations added yet.")
            return

        print("\nFavorite Locations:")
        for idx, location in enumerate(self.favorites, start=1):
            print(f"{idx}. {location}")

        choice = input("Enter the number of the favorite location to view its weather: ")
        try:
            idx = int(choice)
            if 1 <= idx <= len(self.favorites):
                selected_location = list(self.favorites.keys())[idx - 1]
                self.display_weather(self.favorites[selected_location])
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    api_key = "797de563d864ebc9170d0fc34de4ea63"
    weather_app = WeatherApp(api_key)

    weather_app.load_favorites()

    while True:
        print("\nWeather App Menu:")
        print("1. Fetch Current Weather")
        print("2. Fetch Forecast")
        print("3. Add Favorite Location")
        print("4. View Favorite Locations")
        print("5. View Weather for Favorite Location")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            city = input("Enter city name: ")
            weather_data = weather_app.fetch_weather_data(city)
            weather_app.display_weather(weather_data)

        elif choice == '2':
            city = input("Enter city name: ")
            forecast_data = weather_app.fetch_forecast_data(city)
            weather_app.display_forecast(forecast_data)

        elif choice == '3':
            location = input("Enter location: ")
            weather_app.add_favorite(location)
            print(f"{location} added to favorites.")

        elif choice == '4':
            weather_app.view_favorites()

        elif choice == '5':
            weather_app.view_favorite_weather()

        elif choice == '6':
            print("Exiting.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()