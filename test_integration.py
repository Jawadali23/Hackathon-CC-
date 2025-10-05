

from crop_service import crop_service
from get_weather_api import weather_service

def test_region_mapping():
    """Test the region mapping functionality."""
    print("=== Testing Region Mapping Integration ===\n")
    
    
    print("1. Testing region mapping load:")
    print(f"   Region mapping entries: {len(crop_service.region_mapping)}")
    print(f"   Sample mapping: Upland Balochistan -> {crop_service.get_weather_location_for_region('Upland Balochistan')}")
    print()
    
    
    print("2. Testing crop data:")
    crops = crop_service.get_available_crops()
    print(f"   Total crops available: {len(crops)}")
    if crops:
        print(f"   Sample crops: {crops[:5]}")
    print()
    
    
    if crops:
        test_crop = crops[0]
        print(f"3. Testing weather mapping for '{test_crop}':")
        regions = crop_service.get_regions_for_crop(test_crop)
        print(f"   Regions for {test_crop}: {regions}")
        
        if regions:
            test_region = regions[0]
            weather_location = crop_service.get_weather_location_for_region(test_region)
            print(f"   Weather location for '{test_region}': {weather_location}")
            
            
            print(f"   Testing weather API for {weather_location}...")
            weather_data = weather_service.get_formatted_weather_for_city(weather_location)
            if weather_data and weather_data.get('success'):
                print(f"   ✓ Weather data retrieved successfully!")
                print(f"     Temperature: {weather_data.get('temperature_str')}")
                print(f"     Location: {weather_data.get('location_display')}")
            else:
                print(f"   ✗ Weather data failed: {weather_data.get('error', 'Unknown error')}")
        print()
    
    
    print("4. Testing crop regions with weather info:")
    if crops:
        test_crop = crops[0]
        regions_with_weather = crop_service.get_crop_regions_with_weather_info(test_crop)
        print(f"   Regions with weather info for '{test_crop}':")
        for region_info in regions_with_weather[:3]: 
            print(f"     - {region_info['region']} -> {region_info['weather_location']}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_region_mapping()