import pandas as pd
import os
from datetime import datetime
import logging
from region_maping import region_mapping

class CropDataService:
    """Service to handle crop data operations for the harvest calendar."""
    
    def __init__(self, csv_path=None):
        """Initialize the crop data service."""
        self.csv_path = csv_path or os.path.join('data', 'cleaned_crop_data.csv')
        self.df = None
       
        self.region_mapping = region_mapping
        
        self.region_to_province = {
            'Central Punjab': 'Punjab',
            'Northern Punjab': 'Punjab', 
            'Southern Punjab': 'Punjab',
            'Pothowar region': 'Punjab',
            'Upper Sindh': 'Sindh',
            'Lower Sindh': 'Sindh',
            'Irrigated Sindh': 'Sindh',
            'NWFP': 'Khyber Pakhtunkhwa',
            'Irrigated areas of NWFP (Plains of NWFP)': 'Khyber Pakhtunkhwa',
            'Plains of NWFP': 'Khyber Pakhtunkhwa',
            'Rainfed areas of NWFP': 'Khyber Pakhtunkhwa',
            'Upland Balochistan': 'Balochistan',
            'Plains of Balochistan': 'Balochistan',
            'Rainfed Baluchistan': 'Balochistan',
            'Gilgit Baltistan': 'Gilgit-Baltistan',
            'Azad Jammu and kashmir': 'Azad Jammu & Kashmir',
            'Plain and irrigated areas of Pakistan': 'Punjab',  
            'Lowlands': 'Punjab',
            'Upper regions': 'Khyber Pakhtunkhwa'
        }
        
        self.load_data()
    
    def load_data(self):
        """Load crop data from CSV file."""
        try:
            if os.path.exists(self.csv_path):
                self.df = pd.read_csv(self.csv_path)
                
                self._clean_data()
                logging.info(f"Loaded {len(self.df)} crop records from {self.csv_path}")
            else:
                logging.error(f"CSV file not found: {self.csv_path}")
                
                self.df = pd.DataFrame(columns=[
                    'Country Name', 'Crop', 'Region', 'Early Sowing', 'Late Sowing',
                    'Early Harvest', 'Late Harvest', 'Sowing Rate', 'Growing Period'
                ])
        except Exception as e:
            logging.error(f"Error loading crop data: {e}")
            self.df = pd.DataFrame()
    
    def _clean_data(self):
        """Clean and standardize the crop data."""
        if self.df is not None and not self.df.empty:
            
            self.df = self.df.dropna(subset=['Crop', 'Region'])
            
            
            self.df['Crop'] = self.df['Crop'].str.replace('"', '').str.strip()
            
            
            self.df['Region'] = self.df['Region'].str.strip()
            
           
            columns_to_clean = ['Early Sowing', 'Late Sowing', 'Early Harvest', 'Late Harvest']
            for col in columns_to_clean:
                if col in self.df.columns:
                    self.df[col] = self.df[col].replace(['Unknown', 'nan'], None)
    
    def get_available_crops(self):
        """Get list of all available crops."""
        if self.df is not None and not self.df.empty:
            crops = sorted(self.df['Crop'].unique().tolist())
            return [crop for crop in crops if crop and str(crop) != 'nan']
        return []
    
    def get_regions_for_crop(self, crop_name):
        """Get list of regions where a specific crop can be grown."""
        if self.df is not None and not self.df.empty:
            crop_data = self.df[self.df['Crop'] == crop_name]
            regions = sorted(crop_data['Region'].unique().tolist())
            return [region for region in regions if region and str(region) != 'nan']
        return []
    
    def get_all_regions(self):
        """Get list of all available regions."""
        if self.df is not None and not self.df.empty:
            regions = sorted(self.df['Region'].unique().tolist())
            return [region for region in regions if region and str(region) != 'nan']
        return []
    
    def get_crop_calendar(self, crop_name=None, region=None):
        """Get crop calendar information for specific crop and/or region."""
        if self.df is None or self.df.empty:
            return []
        
        
        filtered_df = self.df.copy()
        
        if crop_name:
            filtered_df = filtered_df[filtered_df['Crop'] == crop_name]
        
        if region:
            filtered_df = filtered_df[filtered_df['Region'] == region]
        
        
        calendar_data = []
        for _, row in filtered_df.iterrows():
            calendar_data.append({
                'crop': row['Crop'],
                'region': row['Region'],
                'early_sowing': self._format_date(row.get('Early Sowing')),
                'late_sowing': self._format_date(row.get('Late Sowing')),
                'early_harvest': self._format_date(row.get('Early Harvest')),
                'late_harvest': self._format_date(row.get('Late Harvest')),
                'sowing_rate': row.get('Sowing Rate'),
                'growing_period': row.get('Growing Period')
            })
        
        return calendar_data
    
    def _format_date(self, date_str):
        """Format date string for better display."""
        if pd.isna(date_str) or str(date_str) in ['Unknown', 'nan', 'None']:
            return None
        
        try:
            
            if isinstance(date_str, str) and '/' in date_str:
                parts = date_str.split('/')
                if len(parts) == 2:
                    day, month = parts
                    month_names = {
                        '01': 'January', '02': 'February', '03': 'March', '04': 'April',
                        '05': 'May', '06': 'June', '07': 'July', '08': 'August',
                        '09': 'September', '10': 'October', '11': 'November', '12': 'December'
                    }
                    month_name = month_names.get(month.zfill(2), month)
                    return f"{int(day)} {month_name}"
            return str(date_str)
        except:
            return str(date_str) if date_str else None
    
    def get_planting_suggestions(self, crop_name, region=None, current_month=None):
        """Get planting suggestions for a specific crop and region."""
        calendar_data = self.get_crop_calendar(crop_name, region)
        
        if not calendar_data:
            return None
        
        suggestions = []
        current_month = current_month or datetime.now().month
        
        for entry in calendar_data:
            suggestion = {
                'crop': entry['crop'],
                'region': entry['region'],
                'sowing_period': self._get_period_display(entry['early_sowing'], entry['late_sowing']),
                'harvest_period': self._get_period_display(entry['early_harvest'], entry['late_harvest']),
                'growing_period': entry['growing_period'],
                'sowing_rate': entry['sowing_rate'],
                'is_planting_season': self._is_planting_season(entry, current_month)
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _get_period_display(self, early_date, late_date):
        """Get a readable period display from early and late dates."""
        if early_date and late_date:
            return f"{early_date} - {late_date}"
        elif early_date:
            return f"From {early_date}"
        elif late_date:
            return f"Until {late_date}"
        else:
            return "No data available"
    
    def _is_planting_season(self, entry, current_month):
        """Check if current month is within planting season."""
        try:
            early_sowing = entry.get('early_sowing')
            late_sowing = entry.get('late_sowing')
            
            if not early_sowing and not late_sowing:
                return False
            
            
            early_month = self._extract_month(early_sowing) if early_sowing else None
            late_month = self._extract_month(late_sowing) if late_sowing else None
            
            if early_month and late_month:
              
                if early_month <= late_month:
                    return early_month <= current_month <= late_month
                else:
                    return current_month >= early_month or current_month <= late_month
            elif early_month:
                return current_month >= early_month
            elif late_month:
                return current_month <= late_month
            
        except Exception as e:
            logging.error(f"Error checking planting season: {e}")
        
        return False
    
    def _extract_month(self, date_str):
        """Extract month number from date string."""
        if not date_str or str(date_str) in ['Unknown', 'nan', 'None']:
            return None
        
        try:
            if isinstance(date_str, str) and '/' in date_str:
                parts = date_str.split('/')
                if len(parts) == 2:
                    return int(parts[1])  
        except (ValueError, IndexError):
            pass
        
        return None
    
    def search_crops(self, query):
        """Search crops by name (case-insensitive)."""
        if not query or self.df is None or self.df.empty:
            return []
        
        query = query.lower()
        all_crops = self.get_available_crops()
        matching_crops = [crop for crop in all_crops if query in crop.lower()]
        return matching_crops
    
    def get_crop_activities(self, crop_name, country_name=None):
        """
        Get sowing and harvesting activities for a specific crop.
        Returns data in the format: {sowing: {start_month, end_month}, harvest: {start_month, end_month}}
        """
        if self.df is None or self.df.empty:
            return None
        
        
        filtered_df = self.df[self.df['Crop'] == crop_name].copy()
        if country_name:
            filtered_df = filtered_df[filtered_df['Country Name'] == country_name]
        
        if filtered_df.empty:
            return None
        
        activities = {
            'sowing': {'start_month': None, 'end_month': None, 'period_display': 'No data'},
            'harvest': {'start_month': None, 'end_month': None, 'period_display': 'No data'},
            'regions': []
        }
        
        
        sowing_months = []
        harvest_months = []
        
        for _, row in filtered_df.iterrows():
           
            early_sowing_month = self._extract_month_from_date(row.get('Early Sowing'))
            late_sowing_month = self._extract_month_from_date(row.get('Late Sowing'))
            
            
            early_harvest_month = self._extract_month_from_date(row.get('Early Harvest'))
            late_harvest_month = self._extract_month_from_date(row.get('Late Harvest'))
            
            
            if early_sowing_month:
                sowing_months.append(early_sowing_month)
            if late_sowing_month:
                sowing_months.append(late_sowing_month)
            if early_harvest_month:
                harvest_months.append(early_harvest_month)
            if late_harvest_month:
                harvest_months.append(late_harvest_month)
            
            
            activities['regions'].append({
                'region': row.get('Region', 'Unknown'),
                'sowing_period': self._get_period_display(
                    self._format_date(row.get('Early Sowing')),
                    self._format_date(row.get('Late Sowing'))
                ),
                'harvest_period': self._get_period_display(
                    self._format_date(row.get('Early Harvest')),
                    self._format_date(row.get('Late Harvest'))
                )
            })
        
        
        if sowing_months:
            activities['sowing']['start_month'] = min(sowing_months)
            activities['sowing']['end_month'] = max(sowing_months)
            activities['sowing']['period_display'] = self._get_month_range_display(
                activities['sowing']['start_month'],
                activities['sowing']['end_month']
            )
        
        
        if harvest_months:
            activities['harvest']['start_month'] = min(harvest_months)
            activities['harvest']['end_month'] = max(harvest_months)
            activities['harvest']['period_display'] = self._get_month_range_display(
                activities['harvest']['start_month'],
                activities['harvest']['end_month']
            )
        
        return activities
    
    def _extract_month_from_date(self, date_str):
        """Extract month number from date string in DD/MM format."""
        if pd.isna(date_str) or str(date_str) in ['Unknown', 'nan', 'None']:
            return None
        
        try:
            if isinstance(date_str, str) and '/' in date_str:
                parts = date_str.split('/')
                if len(parts) == 2:
                    return int(parts[1])  
        except (ValueError, IndexError):
            pass
        
        return None
    
    def _get_month_range_display(self, start_month, end_month):
        """Convert month numbers to readable range display."""
        if not start_month or not end_month:
            return 'No data'
        
        month_names = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        
        try:
            start_name = month_names[start_month - 1]
            end_name = month_names[end_month - 1]
            
            if start_month == end_month:
                return start_name
            else:
                return f"{start_name} – {end_name}"
        except IndexError:
            return 'Invalid date'
    
    def check_current_suitability(self, crop_name, country_name=None, current_month=None):
        
        if current_month is None:
            current_month = datetime.now().month
        
        activities = self.get_crop_activities(crop_name, country_name)
        if not activities:
            return {
                'suitable_for_sowing': False,
                'suitable_for_harvest': False,
                'status': 'No data available for this crop',
                'current_month_name': self._get_month_name(current_month)
            }
        
        
        sowing_suitable = False
        if activities['sowing']['start_month'] and activities['sowing']['end_month']:
            sowing_suitable = self._is_month_in_range(
                current_month,
                activities['sowing']['start_month'],
                activities['sowing']['end_month']
            )
        
       
        harvest_suitable = False
        if activities['harvest']['start_month'] and activities['harvest']['end_month']:
            harvest_suitable = self._is_month_in_range(
                current_month,
                activities['harvest']['start_month'],
                activities['harvest']['end_month']
            )
        
        
        status = 'Not suitable for sowing or harvesting'
        if sowing_suitable and harvest_suitable:
            status = 'Suitable for both sowing and harvesting'
        elif sowing_suitable:
            status = 'Suitable for sowing'
        elif harvest_suitable:
            status = 'Suitable for harvesting'
        
        return {
            'suitable_for_sowing': sowing_suitable,
            'suitable_for_harvest': harvest_suitable,
            'status': status,
            'current_month_name': self._get_month_name(current_month),
            'activities': activities
        }
    
    def _is_month_in_range(self, month, start_month, end_month):
        """Check if a month falls within a given range, handling year wrap-around."""
        if start_month <= end_month:
            
            return start_month <= month <= end_month
        else:
            
            return month >= start_month or month <= end_month
    
    def _get_month_name(self, month_num):
        """Convert month number to month name."""
        month_names = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        try:
            return month_names[int(month_num) - 1]
        except (ValueError, IndexError):
            return str(month_num)
    
    def get_countries(self):
        """Get list of all available countries."""
        if self.df is not None and not self.df.empty:
            countries = sorted(self.df['Country Name'].unique().tolist())
            return [country for country in countries if country and str(country) != 'nan']
        return []
    
    def get_crops_by_country(self, country_name):
        """Get list of crops available for a specific country."""
        if self.df is not None and not self.df.empty:
            country_data = self.df[self.df['Country Name'] == country_name]
            crops = sorted(country_data['Crop'].unique().tolist())
            return [crop for crop in crops if crop and str(crop) != 'nan']
        return []
    
    def get_crops_by_region(self, region_name):
        """Get list of crops available for a specific region."""
        if self.df is not None and not self.df.empty:
            region_data = self.df[self.df['Region'] == region_name]
            crops = sorted(region_data['Crop'].unique().tolist())
            return [crop for crop in crops if crop and str(crop) != 'nan']
        return []
    
    def get_province_for_region(self, region):
        """Get the province name for a given region."""
        return self.region_to_province.get(region, 'Punjab')  
    
    def get_weather_location_for_region(self, region):
        """Get the specific weather location (city, province) for a given region using region mapping."""
        if region in self.region_mapping:
            return self.region_mapping[region]
        
        
        province = self.get_province_for_region(region)
        return f"{province}, Pakistan"
    
    def get_crop_regions_with_weather_info(self, crop_name):
        """Get regions for a crop along with their weather location information."""
        regions = self.get_regions_for_crop(crop_name)
        regions_with_weather = []
        
        for region in regions:
            weather_location = self.get_weather_location_for_region(region)
            regions_with_weather.append({
                'region': region,
                'weather_location': weather_location,
                'province': self.get_province_for_region(region)
            })
        
        return regions_with_weather
    
    def get_most_suitable_province(self, crop_name, country_name=None):
        """
        Get the most suitable province for weather data based on crop regions.
        Returns the province that appears most frequently for the crop.
        """
        if self.df is None or self.df.empty:
            return 'Punjab'  
        
        filtered_df = self.df[self.df['Crop'] == crop_name].copy()
        if country_name:
            filtered_df = filtered_df[filtered_df['Country Name'] == country_name]
        
        if filtered_df.empty:
            return 'Punjab'  
        
        
        province_counts = {}
        for _, row in filtered_df.iterrows():
            region = row.get('Region', '')
            province = self.get_province_for_region(region)
            province_counts[province] = province_counts.get(province, 0) + 1
        
        if province_counts:
            return max(province_counts.items(), key=lambda x: x[1])[0]
        
        return 'Punjab'  
    
    def get_statistics(self):
        """Get basic statistics about the crop data."""
        if self.df is None or self.df.empty:
            return {
                'total_crops': 0,
                'total_regions': 0,
                'total_records': 0,
                'total_countries': 0
            }
        
        return {
            'total_crops': len(self.get_available_crops()),
            'total_regions': len(self.get_all_regions()),
            'total_records': len(self.df),
            'total_countries': len(self.get_countries())
        }



crop_service = CropDataService()