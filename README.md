# Flask Web Application

A modern, responsive Flask web application with a clean design and essential features.

## Features

- 🚀 **Fast & Lightweight**: Built with Flask for optimal performance
- 📱 **Responsive Design**: Bootstrap 5 for mobile-first design
- 🎨 **Modern UI**: Clean and professional interface
- 📝 **Contact Form**: Working contact form with validation
- 🔧 **Easy Configuration**: Environment-based configuration
- 📊 **API Endpoints**: RESTful API for status checks
- 🛡️ **Error Handling**: Custom 404 and 500 error pages
- ✨ **Interactive**: JavaScript enhancements and animations

## Project Structure

```
Flask/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore file
├── README.md            # This file
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Custom styles
│   │   └── js/
│   │       └── main.js      # JavaScript functionality
│   └── templates/
│       ├── base.html        # Base template
│       ├── index.html       # Home page
│       ├── about.html       # About page
│       ├── contact.html     # Contact page
│       ├── 404.html         # 404 error page
│       └── 500.html         # 500 error page
└── instance/                # Instance-specific files
```

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project:**
   ```bash
   # If using git
   git clone <repository-url>
   cd Flask
   
   # Or simply navigate to the project directory
   cd "c:\Users\jawad\OneDrive\Desktop\Flask"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables (optional):**
   ```bash
   copy .env.example .env
   # Edit .env file with your specific settings
   ```

6. **Run the application:**
   ```bash
   python app.py
   ```

7. **Open your browser:**
   Navigate to `http://localhost:5000`

## Usage

### Development Mode

The application runs in debug mode by default, which means:
- Automatic reloading when files change
- Detailed error messages
- Debug toolbar (if installed)

### Routes

- `/` - Home page with application overview
- `/about` - About page with feature details
- `/contact` - Contact form
- `/api/status` - API endpoint for status checks

### Customization

#### Adding New Routes

Add new routes in `app.py`:

```python
@app.route('/new-page')
def new_page():
    return render_template('new_page.html', title='New Page')
```

#### Styling

- Modify `app/static/css/style.css` for custom styles
- The application uses Bootstrap 5 for base styling

#### JavaScript

- Add custom JavaScript in `app/static/js/main.js`
- The file includes utilities for forms, animations, and API calls

## Configuration

The application supports different configurations:

- **Development**: Debug enabled, detailed error messages
- **Production**: Debug disabled, optimized for deployment
- **Testing**: Special configuration for unit tests

Modify `config.py` to adjust settings for different environments.

## API Endpoints

### Status Check
- **URL**: `/api/status`
- **Method**: GET
- **Response**: JSON with application status and timestamp

## Deployment

### Production Considerations

1. **Set environment variables:**
   ```bash
   set SECRET_KEY=your-production-secret-key
   set FLASK_ENV=production
   ```

2. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Configure a reverse proxy** (nginx, Apache)

4. **Set up SSL/HTTPS** for secure connections

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions or issues:
- Check the documentation
- Create an issue in the repository
- Contact the development team

## Changelog

### Version 1.0.0
- Initial release
- Basic Flask application structure
- Responsive design with Bootstrap 5
- Contact form functionality
- Error handling
- API endpoints
- Configuration management