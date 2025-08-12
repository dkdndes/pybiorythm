# PyBiorythm Dashboard

A Django web dashboard that consumes the PyBiorythm REST API and presents interactive Plotly visualizations using HTMX for dynamic updates.

## Overview

This dashboard application is the third component in the PyBiorythm database integration example. It demonstrates how to:

- **Consume REST APIs**: Connect to the Django REST API server using a custom API client
- **Interactive Visualizations**: Create dynamic Plotly charts based on biorhythm data
- **Progressive Enhancement**: Use HTMX for seamless user interactions without page reloads
- **Real-time Updates**: Provide live chart updates and API status monitoring
- **Responsive Design**: Bootstrap-based UI that works on desktop and mobile devices

## Architecture

```
┌─────────────────────┐    HTTP/JSON    ┌──────────────────────┐    SQL    ┌──────────────┐
│                     │    ────────>    │                      │  ──────>  │              │
│  PyBiorythm         │                 │  Django REST API     │           │   SQLite     │
│  Dashboard          │                 │  Server (Port 8001)  │           │   Database   │
│  (Port 8000)        │    <────────    │                      │  <──────  │              │
│                     │                 │                      │           │              │
└─────────────────────┘                 └──────────────────────┘           └──────────────┘
        │                                         │
        │                                         │
    Django + HTMX                          Django REST Framework
    Plotly.js                              + PyBiorythm Library
    Bootstrap UI                           + Token Authentication
```

## Features

### 🎯 Dashboard Home
- API connection status monitoring
- Global statistics overview
- People search and filtering
- Quick person selection

### 📊 Person Dashboard
- **Biorhythm Line Chart**: Interactive timeline showing all three cycles
- **Distribution Analysis**: Histogram of cycle value distributions
- **Critical Days Calendar**: Visual calendar highlighting critical periods
- **Current Phases**: Polar chart showing current cycle positions
- **Statistics Summary**: Comprehensive statistical analysis

### ⚡ Technical Features
- **HTMX Integration**: Dynamic chart loading without page refreshes
- **API Caching**: Intelligent caching for improved performance
- **Real-time Monitoring**: Live API status updates
- **Error Handling**: Graceful fallbacks for API failures
- **Responsive Design**: Mobile-friendly interface

## Installation

### Prerequisites

1. **Python 3.8+** with `uv` package manager
2. **PyBiorythm REST API Server** running on port 8001
3. **Database with biorhythm data** (from previous examples)

### Setup

1. **Install Dependencies**:
   ```bash
   cd biorhythm-dashboard
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API configuration
   ```

3. **Initialize Database**:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

4. **Test API Connection**:
   ```bash
   python manage.py test_api --detailed
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following settings:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PyBiorythm API Configuration
PYBIORYTHM_API_BASE_URL=http://localhost:8001/api/
PYBIORYTHM_API_TOKEN=your-api-token-here

# Logging
DJANGO_LOG_LEVEL=INFO
```

### API Configuration

The dashboard connects to the PyBiorythm REST API server. Make sure:

1. **API Server is Running**: The Django REST API server should be running on port 8001
2. **Authentication Token**: Obtain a token from the API server:
   ```bash
   curl -X POST http://localhost:8001/api/auth/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "your-password"}'
   ```
3. **Database has Data**: Ensure the API server has biorhythm data to display

## Usage

### Starting the Dashboard

1. **Start the API Server** (from the django-api-server directory):
   ```bash
   source .venv/bin/activate
   daphne -b 0.0.0.0 -p 8001 biorhythm_api.asgi:application
   ```

2. **Start the Dashboard** (from the biorhythm-dashboard directory):
   ```bash
   source .venv/bin/activate
   python manage.py runserver 8000
   ```

3. **Access the Dashboard**:
   - Open http://localhost:8000 in your browser
   - The dashboard will automatically check API connectivity

### Navigation

- **Home Page**: Overview of all people and global statistics
- **Person Dashboard**: Detailed visualizations for a specific person
- **Chart Tabs**: Switch between different visualization types
- **Date Filtering**: Adjust date ranges for time-series analysis
- **Calculate Button**: Trigger new biorhythm calculations

### Chart Types

1. **Biorhythm Cycles**: Line chart showing physical, emotional, and intellectual cycles over time
2. **Distribution**: Histogram showing the distribution of cycle values
3. **Critical Days**: Calendar view highlighting critical periods
4. **Current Phases**: Polar chart showing current position in each cycle
5. **Statistics**: Summary bar chart of cycle averages and critical day counts

## API Integration

### API Client Service

The dashboard uses a custom API client (`dashboard/services.py`) that provides:

- **Connection Management**: Automatic token authentication
- **Error Handling**: Graceful fallbacks for API failures
- **Caching**: Intelligent caching for improved performance
- **Request Optimization**: Efficient data fetching patterns

### Example API Usage

```python
from dashboard.services import api_client

# Get person data
person_data = api_client.get_person_cached(person_id=1)

# Get biorhythm data with date filtering
biorhythm_data = api_client.get_biorhythm_data_fresh(
    person_id=1,
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31),
    limit=1000
)

# Trigger new calculation
result = api_client.calculate_biorhythm_and_invalidate(
    person_id=1,
    days=365,
    notes="Annual calculation"
)
```

## HTMX Integration

The dashboard uses HTMX for dynamic interactions:

### Chart Loading
```html
<div id="line-chart" 
     hx-get="/charts/person/1/line/"
     hx-trigger="load"
     hx-swap="none">
</div>
```

### Search Functionality
```html
<input type="text" 
       hx-get="/partials/people/"
       hx-target="#people-list"
       hx-trigger="keyup changed delay:500ms"
       name="search">
```

### Form Submissions
```html
<form hx-post="/person/1/calculate/"
      hx-target="#calculation-result">
    <!-- Form fields -->
</form>
```

## Plotly Visualizations

### Chart Creation

Charts are created server-side using Plotly and sent as JSON:

```python
def create_biorhythm_line_chart(biorhythm_data, person_name):
    fig = go.Figure()
    
    # Add traces for each cycle
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['physical'],
        name='Physical (23 days)',
        line=dict(color='#FF6B6B', width=2)
    ))
    
    return json.dumps(fig, cls=PlotlyJSONEncoder)
```

### Client-side Rendering

Charts are rendered using Plotly.js:

```javascript
function renderChart(elementId, chartData, config) {
    const element = document.getElementById(elementId);
    const plotData = JSON.parse(chartData);
    Plotly.newPlot(element, plotData.data, plotData.layout, config);
}
```

## Development

### Project Structure

```
biorhythm-dashboard/
├── biorhythm_dashboard/          # Django project settings
│   ├── settings.py              # Configuration with API settings
│   ├── urls.py                  # Main URL routing
│   └── asgi.py                  # ASGI configuration
├── dashboard/                    # Main application
│   ├── views.py                 # Dashboard and chart views
│   ├── urls.py                  # App URL patterns
│   ├── services.py              # API client service
│   ├── plotly_utils.py          # Chart creation utilities
│   └── management/commands/     # Management commands
│       └── test_api.py          # API testing command
├── templates/                    # Django templates
│   ├── base.html               # Base template with HTMX/Plotly
│   └── dashboard/              # Dashboard-specific templates
│       ├── home.html           # Home page
│       ├── person_dashboard.html # Person detail page
│       └── partials/           # HTMX partial templates
└── static/                      # Static files (CSS, JS, images)
```

### Adding New Charts

1. **Create Chart Function** in `plotly_utils.py`:
   ```python
   def create_new_chart(data, person_name):
       # Create Plotly figure
       fig = go.Figure()
       # Add traces and customize
       return json.dumps(fig, cls=PlotlyJSONEncoder)
   ```

2. **Add View Function** in `views.py`:
   ```python
   @require_http_methods(["GET"])
   @never_cache
   def chart_new_chart(request, person_id):
       # Get data and create chart
       chart_data = create_new_chart(data, person_name)
       return JsonResponse({
           'chart_data': chart_data,
           'config': get_chart_config()
       })
   ```

3. **Add URL Pattern** in `urls.py`:
   ```python
   path('charts/person/<int:person_id>/new/', views.chart_new_chart, name='chart_new'),
   ```

4. **Add Template Integration** in templates:
   ```html
   <div id="new-chart" 
        hx-get="{% url 'dashboard:chart_new' person.id %}"
        hx-trigger="intersect once"
        hx-swap="none">
   </div>
   ```

### Testing

Test the dashboard with:

```bash
# Test API connection
python manage.py test_api --detailed

# Check Django configuration
python manage.py check

# Run development server
python manage.py runserver 8000
```

## Troubleshooting

### Common Issues

1. **API Connection Failed**:
   - Verify the API server is running on port 8001
   - Check the API URL in `.env` file
   - Ensure authentication token is valid

2. **Charts Not Loading**:
   - Check browser console for JavaScript errors
   - Verify HTMX requests are succeeding
   - Ensure Plotly.js is loaded correctly

3. **No Data Available**:
   - Confirm the API server has biorhythm data
   - Check date range filters
   - Verify person exists in the database

4. **Static Files Not Loading**:
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATIC_ROOT` settings
   - Ensure WhiteNoise is configured correctly

### Debug Mode

Enable detailed logging by setting in `.env`:

```env
DEBUG=True
DJANGO_LOG_LEVEL=DEBUG
```

This will provide detailed information about API requests, chart generation, and HTMX interactions.

## Next Steps

This dashboard demonstrates advanced integration patterns. Consider extending it with:

1. **Real-time Updates**: WebSocket integration for live data updates
2. **Export Features**: PDF/PNG chart export functionality  
3. **User Authentication**: Multi-user dashboard with personal data
4. **Advanced Analytics**: Machine learning insights and predictions
5. **Mobile App**: React Native or Flutter companion app

## Integration with Phase 3

This dashboard completes **Phase 3 - Advanced Integration Examples** by demonstrating:

- ✅ Database integration (SQLite with Django ORM)
- ✅ REST API serving (Django REST Framework with token auth)
- ✅ Web dashboard consumption (Django + HTMX + Plotly)
- ✅ Interactive visualizations (Multiple chart types from notebooks)
- ✅ Real-time monitoring (API status and live updates)

The complete Phase 3 example shows a production-ready biorhythm analysis system with separate concerns, scalable architecture, and modern web technologies.