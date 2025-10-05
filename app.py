from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import logging
from datetime import datetime
from crop_service import crop_service
from get_weather_api import weather_service
from region_maping import get_region_city_mapping


logging.basicConfig(level=logging.INFO)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, 
                template_folder='app/templates',
                static_folder='app/static')
    

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'harvest-calendar-secret-key'
    app.config['DEBUG'] = True
    
    
    @app.route('/')
    def home():
        """Home page - redirect to crop weather form."""
        return redirect(url_for('crop_weather_form'))
    
    @app.route('/region-selection/<crop_name>')
    def region_selection(crop_name):
        """Region selection page for a specific crop with weather preview."""
        regions = crop_service.get_regions_for_crop(crop_name)
        
        if not regions:
            flash(f'No regional data found for {crop_name}', 'warning')
            return redirect(url_for('crop_weather_form'))
        
        
        regions_with_weather = []
        for region in regions:
            
            weather_location = crop_service.get_weather_location_for_region(region)
            weather_data = weather_service.get_formatted_weather_for_city(weather_location)
            
            regions_with_weather.append({
                'name': region,
                'weather_location': weather_location,
                'weather': weather_data
            })
        
        return render_template('region_selection.html',
                             title=f'Select Region for {crop_name}',
                             crop_name=crop_name,
                             regions=regions,
                             regions_with_weather=regions_with_weather)
    
    @app.route('/harvest-calendar')
    def harvest_calendar():
        """Main harvest calendar page with recommendations and weather data."""
        crop_name = request.args.get('crop')
        region = request.args.get('region')
        
        if not crop_name:
            flash('Please select a crop first', 'warning')
            return redirect(url_for('crop_weather_form'))
        
        
        suggestions = crop_service.get_planting_suggestions(crop_name, region)
        
        if not suggestions:
            flash(f'No data found for {crop_name} in the selected region', 'error')
            return redirect(url_for('crop_weather_form'))
        
        
        current_month = datetime.now().month
        month_name = datetime.now().strftime('%B')
        
        
        weather_data = None
        if region:
            
            weather_location = crop_service.get_weather_location_for_region(region)
            weather_data = weather_service.get_formatted_weather_for_city(weather_location)
        else:
            
            if suggestions:
                
                default_region = suggestions[0].get('region')
                if default_region:
                    weather_location = crop_service.get_weather_location_for_region(default_region)
                    weather_data = weather_service.get_formatted_weather_for_city(weather_location)
        
        return render_template('harvest_calendar.html',
                             title=f'Harvest Calendar - {crop_name}',
                             crop_name=crop_name,
                             region=region,
                             suggestions=suggestions,
                             current_month=current_month,
                             month_name=month_name,
                             weather=weather_data)
    
    @app.route('/quick-search')
    def quick_search():
        """Quick search for crops and regions."""
        query = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'crop')  
        
        if not query:
            return jsonify({'results': []})
        
        if search_type == 'crop':
            results = crop_service.search_crops(query)
            return jsonify({
                'results': [{'name': crop, 'type': 'crop'} for crop in results[:10]]
            })
        else:
            
            all_regions = crop_service.get_all_regions()
            matching_regions = [region for region in all_regions 
                              if query.lower() in region.lower()]
            return jsonify({
                'results': [{'name': region, 'type': 'region'} for region in matching_regions[:10]]
            })
    
    @app.route('/api/crop-calendar')
    def api_crop_calendar():
        """API endpoint for crop calendar data."""
        crop_name = request.args.get('crop')
        region = request.args.get('region')
        
        calendar_data = crop_service.get_crop_calendar(crop_name, region)
        
        return jsonify({
            'success': True,
            'data': calendar_data,
            'count': len(calendar_data)
        })
    
    @app.route('/api/stats')
    def api_stats():
        """API endpoint for application statistics."""
        stats = crop_service.get_statistics()
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
    
    @app.route('/crop-weather')
    def crop_weather_form():
        """Crop Calendar & Weather form page."""
        from region_maping import get_region_city_mapping
        
        try:
            countries = crop_service.get_countries()
            current_month = datetime.now().month
            current_month_name = datetime.now().strftime('%B')
            region_city_map = get_region_city_mapping()
            regions = list(region_city_map.keys()) if region_city_map else []
            
            logging.info(f"Region mapping loaded: {len(regions)} regions")
            logging.info(f"Region city map type: {type(region_city_map)}")
            
            return render_template('crop_weather.html',
                                 title='Crop Calendar & Weather',
                                 countries=countries,
                                 regions=regions,
                                 region_city_map=region_city_map or {},
                                 current_month_name=current_month_name)
        except Exception as e:
            logging.error(f"Error in crop_weather_form: {e}")
            # Fallback with empty data
            return render_template('crop_weather.html',
                                 title='Crop Calendar & Weather',
                                 countries=[],
                                 regions=[],
                                 region_city_map={},
                                 current_month_name=datetime.now().strftime('%B'))
    
    @app.route('/crop-weather-results', methods=['POST'])
    def crop_weather_results():
        """Process crop weather form and show results directly."""
        region = request.form.get('region')
        city = request.form.get('city')
        crop = request.form.get('crop')
        
        if not region or not city or not crop:
            flash('Please select region, city, and crop', 'error')
            return redirect(url_for('crop_weather_form'))
        
        # Check if crop data exists for the selected region/city
        regions_for_crop = crop_service.get_regions_for_crop(crop)
        
        if not regions_for_crop:
            flash(f'No data found for {crop}', 'error')
            return redirect(url_for('crop_weather_form'))
        
        # Redirect to harvest calendar with the selected information
        return redirect(url_for('harvest_calendar', crop=crop, region=city, source='crop_weather'))
    
    @app.route('/api/crops-by-country')
    def api_crops_by_country():
        """API endpoint to get crops for a specific country."""
        country = request.args.get('country')
        if not country:
            return jsonify({'error': 'Country parameter is required'}), 400
        
        crops = crop_service.get_crops_by_country(country)
        return jsonify({'crops': crops})
    
    @app.route('/api/crops-by-region')
    def api_crops_by_region():
        """API endpoint to get crops for a specific region/city."""
        region = request.args.get('region')
        if not region:
            return jsonify({'error': 'Region parameter is required'}), 400
        
        crops = crop_service.get_crops_by_region(region)
        return jsonify({'crops': crops})
    
    @app.route('/api/region-city-mapping')
    def api_region_city_mapping():
        """API endpoint to get the complete region-city mapping."""
        region_city_map = get_region_city_mapping()
        return jsonify({'region_city_map': region_city_map})
    
    @app.route('/api/cities-by-region')
    def api_cities_by_region():
        """API endpoint to get cities for a specific region."""
        region = request.args.get('region')
        if not region:
            return jsonify({'error': 'Region parameter is required'}), 400
        
        region_city_map = get_region_city_mapping()
        cities = region_city_map.get(region, [])
        return jsonify({'cities': cities})
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors."""
        return render_template('404.html', title='Page Not Found'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return render_template('500.html', title='Server Error'), 500
    

    @app.template_filter('format_month')
    def format_month(month_num):
        """Convert month number to month name."""
        month_names = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        try:
            return month_names[int(month_num) - 1]
        except (ValueError, IndexError):
            return str(month_num)
    
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)