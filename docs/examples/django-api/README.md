# PyBiorythm Django REST API Example

A simple Django REST Framework example demonstrating how to serve PyBiorythm data through a web API. This example shows developers how to integrate biorhythm calculations into web applications and APIs.

## 🎯 **Purpose**

This example demonstrates:
- **Web API integration** - Serving PyBiorythm data through HTTP endpoints
- **JSON responses** - Structured biorhythm data in JSON format
- **Input validation** - Proper handling of date parameters and user input
- **Error handling** - Graceful error responses for invalid inputs
- **Multiple endpoints** - Different ways to access biorhythm calculations

## 🚀 **Quick Start**

### **Using uv (Recommended):**

```bash
# Navigate to this directory
cd docs/examples/django-api

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv sync

# Run database migrations (creates SQLite database)
python manage.py migrate

# Start the development server
python manage.py runserver
```

### **Using pip:**

```bash
# Navigate to this directory
cd docs/examples/django-api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install django djangorestframework django-cors-headers python-dateutil
pip install git+https://github.com/dkdndes/pybiorythm.git

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

## 📡 **API Endpoints**

Once the server is running (default: http://127.0.0.1:8000/), you can access:

### **1. API Information**
```
GET /api/
```
Returns API documentation and available endpoints.

### **2. Quick Calculation (GET)**
```
GET /api/quick/?birthdate=1990-05-15&days=7
```
Simple calculation via query parameters.

**Parameters:**
- `birthdate` (required): Birth date in YYYY-MM-DD format
- `days` (optional): Number of days to calculate (default: 7, max: 365)

### **3. Full Calculation (POST)**
```
POST /api/calculate/
Content-Type: application/json

{
    "birthdate": "1990-05-15",
    "target_date": "2024-08-10",
    "days": 30
}
```

**Request Body:**
- `birthdate` (required): Birth date in YYYY-MM-DD format
- `target_date` (optional): Calculation start date (defaults to today)
- `days` (optional): Number of days to calculate (1-1095, default: 30)

## 📊 **Example Responses**

### **Quick Calculation Response:**
```json
{
    "birthdate": "1990-05-15",
    "calculation_date": "2024-08-10T16:45:00.123456",
    "days": 7,
    "biorhythm_data": {
        "meta": {
            "generator": "biorhythm_enhanced.py",
            "version": "2025-08-07",
            "birthdate": "1990-05-15",
            "plot_date": "2024-08-10",
            "days_alive": 12506,
            "cycle_lengths_days": {
                "physical": 23,
                "emotional": 28,
                "intellectual": 33
            },
            "chart_orientation": "vertical",
            "days": 7,
            "width": 55
        },
        "data": [
            [-0.997669, -0.781831, -0.189251],
            [-0.942261, -0.900969, -0.0],
            // ... more daily data (physical, emotional, intellectual values)
        ],
        "critical_days": {
            "physical": [1, 5],
            "emotional": [2],
            "intellectual": [2, 6]
        },
        "cycle_repeats": {
            "physical": 0.1304,
            "emotional": 0.1071,
            "intellectual": 0.0909
        }
    }
}
```

### **Full Calculation Response:**
```json
{
    "request_info": {
        "birthdate": "1990-05-15",
        "target_date": "2024-08-10",
        "days_calculated": 30,
        "api_timestamp": "2024-08-10T16:45:00.123456"
    },
    "biorhythm_data": {
        // Same structure as PyBiorythm JSON output
        "meta": { ... },
        "data": [ ... ],
        "critical_days": { ... },
        "cycle_repeats": { ... }
    }
}
```

## 🧪 **Testing the API**

### **1. Interactive Web Interface**
Visit http://127.0.0.1:8000/ for a simple web interface to test the API.

### **2. cURL Examples**

**Quick calculation:**
```bash
curl "http://127.0.0.1:8000/api/quick/?birthdate=1990-05-15&days=7"
```

**Full calculation:**
```bash
curl -X POST http://127.0.0.1:8000/api/calculate/ \
  -H "Content-Type: application/json" \
  -d '{
    "birthdate": "1990-05-15",
    "target_date": "2024-08-10",
    "days": 30
  }'
```

### **3. Python Requests Example**

```python
import requests
import json

# Quick calculation
response = requests.get(
    'http://127.0.0.1:8000/api/quick/',
    params={'birthdate': '1990-05-15', 'days': 7}
)
data = response.json()
print(f"Calculated {data['days']} days of biorhythm data")

# Full calculation
response = requests.post(
    'http://127.0.0.1:8000/api/calculate/',
    json={
        'birthdate': '1990-05-15',
        'target_date': '2024-08-10',
        'days': 30
    }
)
data = response.json()
timeseries = data['biorhythm_data']['timeseries']
print(f"Received {len(timeseries)} data points")
```

### **4. JavaScript/Fetch Example**

```javascript
// Quick calculation
fetch('/api/quick/?birthdate=1990-05-15&days=7')
    .then(response => response.json())
    .then(data => {
        console.log('Biorhythm data:', data.biorhythm_data);
    });

// Full calculation
fetch('/api/calculate/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        birthdate: '1990-05-15',
        target_date: '2024-08-10',
        days: 30
    })
})
.then(response => response.json())
.then(data => {
    console.log('Full calculation result:', data);
});
```

## 🏗️ **Project Structure**

```
django-api/
├── README.md                    # This file
├── pyproject.toml              # Dependencies with PyBiorythm from GitHub
├── manage.py                   # Django management script
├── biorhythm_api/             # Django project settings
│   ├── __init__.py
│   ├── settings.py            # Django configuration
│   ├── urls.py                # URL routing
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
└── biorhythms/                # Django app for biorhythm calculations
    ├── __init__.py
    ├── apps.py                # App configuration
    ├── models.py              # No models needed
    ├── serializers.py         # Request/response validation
    ├── views.py               # API endpoint logic
    ├── urls.py                # App URL patterns
    ├── admin.py               # No admin needed
    └── tests.py               # API tests
```

## 🔧 **Key Features**

### **Input Validation**
- Date format validation (YYYY-MM-DD)
- Range limits (1-1095 days)
- Future date validation for birthdates
- Comprehensive error messages

### **Error Handling**
- Invalid date formats
- Missing required parameters
- PyBiorythm library availability
- Calculation failures

### **CORS Support**
- Configured for frontend integration
- Supports common development ports (3000, 8080)
- Ready for React, Vue, Angular integration

### **Multiple Response Formats**
- JSON API responses
- Django REST Framework browsable API
- Simple HTML test interface

## 🔌 **Integration Examples**

### **Frontend Integration**
This API is designed to work with any frontend framework:

**React:**
```javascript
const [biorhythmData, setBiorhythmData] = useState(null);

const calculateBiorhythm = async (birthdate, days = 7) => {
    const response = await fetch(`/api/quick/?birthdate=${birthdate}&days=${days}`);
    const data = await response.json();
    setBiorhythmData(data.biorhythm_data);
};
```

**Vue.js:**
```javascript
async calculateBiorhythm(birthdate, days = 7) {
    try {
        const response = await this.$http.get('/api/quick/', {
            params: { birthdate, days }
        });
        this.biorhythmData = response.data.biorhythm_data;
    } catch (error) {
        console.error('Calculation failed:', error);
    }
}
```

### **Mobile App Integration**
The JSON API can be consumed by mobile applications:

**Flutter/Dart:**
```dart
Future<Map<String, dynamic>> calculateBiorhythm(String birthdate, int days) async {
    final response = await http.get(
        Uri.parse('http://your-api.com/api/quick/?birthdate=$birthdate&days=$days')
    );
    return json.decode(response.body);
}
```

## 🧪 **Running Tests**

```bash
# Run Django tests
python manage.py test

# Run specific test class
python manage.py test biorhythms.tests.BiorhythmAPITestCase

# Run with verbose output
python manage.py test --verbosity=2
```

## 🚀 **Deployment Considerations**

This is a **development example only**. For production deployment:

### **Security Enhancements Needed:**
- Change the SECRET_KEY
- Set DEBUG = False
- Configure ALLOWED_HOSTS
- Add authentication/authorization
- Enable HTTPS
- Add rate limiting
- Input sanitization
- CSRF protection (if needed)

### **Performance Optimizations:**
- Database connection pooling
- Caching (Redis/Memcached)
- Load balancing
- Static file serving
- API response compression

### **Production Dependencies:**
```bash
pip install gunicorn  # WSGI server
pip install psycopg2  # PostgreSQL adapter
pip install redis     # Caching
```

## 💡 **Usage Scenarios**

### **Web Applications**
- **Biorhythm calculators** - Online tools for personal biorhythm charts
- **Health & wellness apps** - Integration with fitness and wellness platforms
- **Educational tools** - Teaching cyclical patterns and time series analysis

### **Data Integration**
- **Analytics dashboards** - Biorhythm data alongside other health metrics
- **Research platforms** - Academic studies requiring biorhythm calculations
- **Mobile backends** - API for iOS/Android biorhythm applications

### **Development Learning**
- **Django REST Framework** - Learn API development patterns
- **JSON API design** - Understand RESTful API principles
- **Time series data** - Work with cyclical data structures
- **Input validation** - Handle user input securely

## 🔬 **Scientific Disclaimer**

This API serves biorhythm calculations for educational and entertainment purposes. Biorhythm theory is considered pseudoscience and should not be used for making important life decisions.

The value of this example lies in:
- **Technical demonstration** of API development patterns
- **JSON data structure** design for time series data
- **Integration techniques** for serving mathematical calculations
- **Educational use** for learning web API development

## 📚 **Further Reading**

- **[Django REST Framework Documentation](https://www.django-rest-framework.org/)**
- **[PyBiorythm Documentation](../../../)**
- **[API Design Best Practices](https://restfulapi.net/)**
- **[JSON API Specification](https://jsonapi.org/)**

## 🎯 **Next Steps**

After exploring this example:
1. **Try the interactive interface** at http://127.0.0.1:8000/
2. **Test with different birthdates** and time periods
3. **Integrate with a frontend framework** (React, Vue, Angular)
4. **Explore the PyBiorythm JSON structure** for your applications
5. **Adapt the code** for your specific use cases

---

**🚀 Ready to build biorhythm-powered applications?** This API provides a solid foundation for integrating PyBiorythm data into web applications, mobile apps, and data analysis platforms!