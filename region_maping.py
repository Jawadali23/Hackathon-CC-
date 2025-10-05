
region_mapping = {
    # Original mappings
    "Upland Balochistan": "Quetta, Balochistan",
    "Plains of Balochistan": "Sibi, Balochistan",
    "Upper Sindh": "Sukkur, Sindh",
    "Lower Sindh": "Hyderabad, Sindh",
    "Southern irrigated Plain": "Multan, Punjab",
    "Central Punjab": "Faisalabad, Punjab",
    "Pothowar region": "Rawalpindi, Punjab",
    "NWFP": "Peshawar, Khyber Pakhtunkhwa",
    "Irrigated areas of NWFP (Plains of NWFP)": "Mardan, Khyber Pakhtunkhwa",
    "Sindh": "Karachi, Sindh",
    "Plain and irrigated areas of Pakistan": "Islamabad, Pakistan",
    "Rainfed areas of NWFP": "Kohat, Khyber Pakhtunkhwa",
    "Southern Punjab": "Bahawalpur, Punjab",
    "Rainfed Baluchistan": "Zhob, Balochistan",   # CSV version with 'u'
    "Northern Punjab": "Lahore, Punjab",
    "Irrigated Sindh": "Larkana, Sindh",
    
    # CSV version with exact case matching
    "Azad Jammu and kashmir": "Muzaffarabad, AJK",  # Note: lowercase 'k' as in CSV
}



def get_region_city_mapping():
    """
    Create a region-to-cities mapping from the existing region_mapping data.
    Extracts regions based on the cities in the CSV data.
    """
    region_city_map = {}
    
    # Group cities by their main region/province
    sindh_cities = []
    punjab_cities = []
    balochistan_cities = []
    kpk_cities = []
    other_cities = []
    
    for city, location in region_mapping.items():
        if "Sindh" in location:
            sindh_cities.append(city)
        elif "Punjab" in location:
            punjab_cities.append(city)
        elif "Balochistan" in location or "Baluchistan" in location:
            balochistan_cities.append(city)
        elif "Khyber Pakhtunkhwa" in location or "NWFP" in city:
            kpk_cities.append(city)
        else:
            other_cities.append(city)
    
    # Create the mapping
    if sindh_cities:
        region_city_map["Sindh"] = sorted(sindh_cities)
    if punjab_cities:
        region_city_map["Punjab"] = sorted(punjab_cities)
    if balochistan_cities:
        region_city_map["Balochistan"] = sorted(balochistan_cities)
    if kpk_cities:
        region_city_map["Khyber Pakhtunkhwa"] = sorted(kpk_cities)
    if other_cities:
        region_city_map["Other Areas"] = sorted(other_cities)
    
    return region_city_map

# Generate the region-city mapping
region_city_map = get_region_city_mapping()

