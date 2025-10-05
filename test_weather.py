from get_weather_api import weather_service


print("Testing weather for Pakistani provinces:")
provinces = ['Sindh', 'Punjab', 'Khyber Pakhtunkhwa', 'Balochistan']

for province in provinces:
    print(f"\n--- {province} ---")
    result = weather_service.get_formatted_weather_for_province(province)
    if result.get('success'):
        print(f"Location: {result.get('location_display', 'N/A')}")
        print(f"Temperature: {result.get('temperature_str', 'N/A')}")
        print(f"Humidity: {result.get('humidity_str', 'N/A')}")
        print(f"Description: {result.get('description', 'N/A')}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")