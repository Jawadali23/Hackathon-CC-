import requests
import logging
from typing import Dict, Optional

class WeatherService:
   
    
    def __init__(self, api_key='5546b04a461e6fc93b42024301c7504a'):
        
        self.api_key = api_key
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'
        
        
        self.pakistan_provinces = {
            'Sindh': ['Karachi', 'Hyderabad', 'Sukkur', 'Larkana'],
            'Punjab': ['Lahore', 'Faisalabad', 'Rawalpindi', 'Multan'],
            'Khyber Pakhtunkhwa': ['Peshawar', 'Mardan', 'Abbottabad', 'Kohat'],
            'Balochistan': ['Quetta', 'Gwadar', 'Turbat', 'Khuzdar'],
            'Gilgit-Baltistan': ['Gilgit', 'Skardu', 'Hunza', 'Ghanche'],
            'Azad Jammu & Kashmir': ['Muzaffarabad', 'Mirpur', 'Kotli', 'Rawalakot']
        }
    
    def get_weather_for_province(self, province_name):
        """
        Get weather data for a Pakistani province using its major city.
        
        Args:
            province_name (str): Name of the Pakistani province
        
        Returns:
            Dict containing weather data or None if request fails
        """
        if province_name not in self.pakistan_provinces:
            
            return self.get_weather_data(province_name, 'PK')
        
        
        major_city = self.pakistan_provinces[province_name][0]
        weather_data = self.get_weather_data(major_city, 'PK')
        
        
        if weather_data:
            weather_data['province'] = province_name
            weather_data['major_city'] = major_city
        
        return weather_data
    
    def get_weather_data(self, location='Pakistan', country_code=None):
        """
        Fetch current weather data for a given location.
        
        Args:
            location (str): City or location name
            country_code (str): Optional country code (e.g., 'PK' for Pakistan)
        
        Returns:
            Dict containing weather data or None if request fails
        """
        try:
           
            query = location
            if country_code:
                query = f"{location},{country_code}"
            
            
            params = {
                'q': query,
                'appid': self.api_key,
                'units': 'metric'  
            }
            
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_weather_data(data)
            else:
                logging.error(f"Weather API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Weather API request failed: {e}")
            return None
        except Exception as e:
            logging.error(f"Error fetching weather data: {e}")
            return None
    
    def _parse_weather_data(self, raw_data: Dict) -> Dict:
        """
        Parse raw weather API response into a clean format.
        
        Args:
            raw_data (Dict): Raw response from OpenWeatherMap API
        
        Returns:
            Dict with parsed weather information
        """
        try:
            main = raw_data.get('main', {})
            weather = raw_data.get('weather', [{}])[0]
            wind = raw_data.get('wind', {})
            rain = raw_data.get('rain', {})
            
            return {
                'location': raw_data.get('name', 'Unknown'),
                'country': raw_data.get('sys', {}).get('country', ''),
                'temperature': round(main.get('temp', 0), 1),
                'feels_like': round(main.get('feels_like', 0), 1),
                'humidity': main.get('humidity', 0),
                'pressure': main.get('pressure', 0),
                'description': weather.get('description', '').title(),
                'main': weather.get('main', ''),
                'wind_speed': wind.get('speed', 0),
                'rainfall': rain.get('1h', 0),  
                'rainfall_3h': rain.get('3h', 0),  
                'visibility': raw_data.get('visibility', 0) / 1000,
                'timestamp': raw_data.get('dt', 0)
            }
        except Exception as e:
            logging.error(f"Error parsing weather data: {e}")
            return {}
    
    def get_weather_for_city(self, city_location):
        """
        Get weather data for a specific city location (e.g., "Quetta, Balochistan").
        
        Args:
            city_location (str): City and province/region (e.g., "Quetta, Balochistan")
        
        Returns:
            Dict containing weather data or None if request fails
        """
        try:
            
            if ',' in city_location:
                city, region = city_location.split(',', 1)
                city = city.strip()
                region = region.strip()
            else:
                city = city_location.strip()
                region = 'Pakistan'
            
           
            weather_data = self.get_weather_data(city, 'PK')
            
            if weather_data:
                weather_data['region'] = region
                weather_data['specified_city'] = city
                weather_data['full_location'] = city_location
            
            return weather_data
        except Exception as e:
            logging.error(f"Error getting weather for city {city_location}: {e}")
            return None
    
    def get_formatted_weather_for_city(self, city_location):
        """
        Get weather data for a specific city location in a format suitable for display.
        
        Args:
            city_location (str): City and province/region (e.g., "Quetta, Balochistan")
        
        Returns:
            Dict with formatted weather strings including specific city info
        """
        weather_data = self.get_weather_for_city(city_location)
        
        if not weather_data:
            return {
                'success': False,
                'error': f'Unable to fetch weather data for {city_location}',
                'temperature_str': 'N/A',
                'humidity_str': 'N/A',
                'rainfall_str': 'N/A',
                'description': 'Weather data unavailable',
                'location_display': city_location
            }
        
        
        temperature_str = f"{weather_data['temperature']}°C"
        humidity_str = f"{weather_data['humidity']}%"
        
        
        rainfall = weather_data.get('rainfall', 0)
        if rainfall > 0:
            rainfall_str = f"{rainfall}mm/h"
        else:
            rainfall_str = "No rainfall"
        
        
        location_display = weather_data.get('full_location', city_location)
        
        return {
            'success': True,
            'location': weather_data['location'],
            'location_display': location_display,
            'region': weather_data.get('region', ''),
            'specified_city': weather_data.get('specified_city', ''),
            'country': weather_data['country'],
            'temperature': weather_data['temperature'],
            'temperature_str': temperature_str,
            'humidity': weather_data['humidity'],
            'humidity_str': humidity_str,
            'rainfall': rainfall,
            'rainfall_str': rainfall_str,
            'description': weather_data['description'],
            'feels_like': weather_data['feels_like'],
            'wind_speed': weather_data['wind_speed'],
            'pressure': weather_data['pressure'],
            'raw_data': weather_data
        }
        """
        Get weather data for a Pakistani province in a format suitable for display.
        
        Args:
            province_name (str): Name of the Pakistani province
        
        Returns:
            Dict with formatted weather strings including province info
        """
        weather_data = self.get_weather_for_province(province_name)
        
        if not weather_data:
            return {
                'success': False,
                'error': f'Unable to fetch weather data for {province_name}',
                'temperature_str': 'N/A',
                'humidity_str': 'N/A',
                'rainfall_str': 'N/A',
                'description': 'Weather data unavailable',
                'province': province_name
            }
        
        
        temperature_str = f"{weather_data['temperature']}°C"
        humidity_str = f"{weather_data['humidity']}%"
        
        
        rainfall = weather_data.get('rainfall', 0)
        if rainfall > 0:
            rainfall_str = f"{rainfall}mm/h"
        else:
            rainfall_str = "No rainfall"
        
        
        location_display = f"{weather_data['location']}, {province_name}"
        
        return {
            'success': True,
            'location': weather_data['location'],
            'location_display': location_display,
            'province': weather_data.get('province', province_name),
            'major_city': weather_data.get('major_city', weather_data['location']),
            'country': weather_data['country'],
            'temperature': weather_data['temperature'],
            'temperature_str': temperature_str,
            'humidity': weather_data['humidity'],
            'humidity_str': humidity_str,
            'rainfall': rainfall,
            'rainfall_str': rainfall_str,
            'description': weather_data['description'],
            'feels_like': weather_data['feels_like'],
            'wind_speed': weather_data['wind_speed'],
            'pressure': weather_data['pressure'],
            'raw_data': weather_data
        }
    
    def get_formatted_weather(self, location='Pakistan', country_code=None):
        """
        Get weather data in a format suitable for display in templates.
        
        Args:
            location (str): City or location name
            country_code (str): Optional country code
        
        Returns:
            Dict with formatted weather strings
        """
        weather_data = self.get_weather_data(location, country_code)
        
        if not weather_data:
            return {
                'success': False,
                'error': 'Unable to fetch weather data',
                'temperature_str': 'N/A',
                'humidity_str': 'N/A',
                'rainfall_str': 'N/A',
                'description': 'Weather data unavailable'
            }
        
       
        temperature_str = f"{weather_data['temperature']}°C"
        humidity_str = f"{weather_data['humidity']}%"
        
        
        rainfall = weather_data.get('rainfall', 0)
        if rainfall > 0:
            rainfall_str = f"{rainfall}mm/h"
        else:
            rainfall_str = "No rainfall"
        
        return {
            'success': True,
            'location': weather_data['location'],
            'country': weather_data['country'],
            'temperature': weather_data['temperature'],
            'temperature_str': temperature_str,
            'humidity': weather_data['humidity'],
            'humidity_str': humidity_str,
            'rainfall': rainfall,
            'rainfall_str': rainfall_str,
            'description': weather_data['description'],
            'feels_like': weather_data['feels_like'],
            'wind_speed': weather_data['wind_speed'],
            'pressure': weather_data['pressure'],
            'raw_data': weather_data
        }


weather_service = WeatherService()


def test_weather_api():
    """Test function to verify weather API is working."""
    weather = weather_service.get_formatted_weather('Karachi', 'PK')
    if weather['success']:
        print(f"Weather in {weather['location']}: {weather['temperature_str']}, {weather['humidity_str']} humidity")
        print(f"Description: {weather['description']}")
        print(f"Rainfall: {weather['rainfall_str']}")
    else:
        print(f"Error: {weather['error']}")

if __name__ == '__main__':
    test_weather_api()