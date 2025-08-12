from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from .serializers import BiorhythmRequestSerializer

# Import PyBiorythm
try:
    from biorythm import BiorhythmCalculator

    BIORYTHM_AVAILABLE = True
except ImportError:
    BIORYTHM_AVAILABLE = False


class BiorhythmCalculationView(APIView):
    """
    Simple API endpoint to calculate biorhythm data using PyBiorythm.

    POST /api/calculate/
    {
        "birthdate": "1990-05-15",
        "target_date": "2024-08-10",  // optional, defaults to today
        "days": 30                    // optional, defaults to 30
    }

    Returns PyBiorythm JSON format with biorhythm calculations.
    """

    def get(self, request):
        """GET endpoint with example usage information."""
        return Response(
            {
                "message": "PyBiorythm Django API Example",
                "endpoints": {"calculate": "/api/calculate/", "quick": "/api/quick/"},
                "example_request": {
                    "method": "POST",
                    "url": "/api/calculate/",
                    "body": {
                        "birthdate": "1990-05-15",
                        "target_date": "2024-08-10",
                        "days": 30,
                    },
                },
                "library_available": BIORYTHM_AVAILABLE,
            }
        )

    def post(self, request):
        """Calculate biorhythm data based on input parameters."""

        if not BIORYTHM_AVAILABLE:
            return Response(
                {
                    "error": "PyBiorythm library not available",
                    "message": "Please install PyBiorythm: pip install git+https://github.com/dkdndes/pybiorythm.git",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # Validate request data
        serializer = BiorhythmRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid input data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Extract validated data
        validated_data = serializer.validated_data
        birthdate = validated_data["birthdate"]
        target_date = validated_data.get("target_date", datetime.now().date())
        days = validated_data.get("days", 30)

        try:
            # Create biorhythm calculator
            calc = BiorhythmCalculator(days=days)

            # Convert dates to datetime objects
            birthdate_dt = datetime.combine(birthdate, datetime.min.time())
            target_date_dt = datetime.combine(target_date, datetime.min.time())

            # Generate biorhythm data
            biorhythm_data = calc.generate_timeseries_json(birthdate_dt, target_date_dt)

            # Add request metadata
            response_data = {
                "request_info": {
                    "birthdate": birthdate.isoformat(),
                    "target_date": target_date.isoformat(),
                    "days_calculated": days,
                    "api_timestamp": datetime.now().isoformat(),
                },
                "biorhythm_data": biorhythm_data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Calculation failed", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class QuickBiorhythmView(APIView):
    """
    Quick biorhythm calculation with minimal input.

    GET /api/quick/?birthdate=1990-05-15&days=7

    Returns biorhythm data for the specified birthdate and number of days.
    """

    def get(self, request):
        """Quick calculation via GET parameters."""

        if not BIORYTHM_AVAILABLE:
            return JsonResponse(
                {"error": "PyBiorythm library not available"}, status=503
            )

        # Get parameters from query string
        birthdate_str = request.GET.get("birthdate")
        days_str = request.GET.get("days", "7")

        if not birthdate_str:
            return JsonResponse(
                {
                    "error": "Missing required parameter: birthdate",
                    "example": "/api/quick/?birthdate=1990-05-15&days=7",
                },
                status=400,
            )

        try:
            # Parse parameters
            birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
            days = int(days_str)

            if days < 1 or days > 365:
                raise ValueError("Days must be between 1 and 365")

            # Calculate biorhythm
            calc = BiorhythmCalculator(days=days)
            biorhythm_data = calc.generate_timeseries_json(birthdate, datetime.now())

            # Return simple response
            return JsonResponse(
                {
                    "birthdate": birthdate_str,
                    "calculation_date": datetime.now().isoformat(),
                    "days": days,
                    "biorhythm_data": biorhythm_data,
                }
            )

        except ValueError as e:
            return JsonResponse(
                {
                    "error": f"Invalid parameter: {str(e)}",
                    "example": "/api/quick/?birthdate=1990-05-15&days=7",
                },
                status=400,
            )
        except Exception as e:
            return JsonResponse({"error": f"Calculation failed: {str(e)}"}, status=500)


def api_home(request):
    """Simple HTML page for testing the API."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PyBiorythm Django API Example</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; }
            .endpoint { 
                background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; 
            }
            .example { 
                background: #e8f4f8; padding: 10px; margin: 5px 0; border-radius: 3px; 
            }
            button { 
                background: #007cba; color: white; padding: 10px 20px; 
                border: none; border-radius: 3px; cursor: pointer; 
            }
            button:hover { background: #005a87; }
            input { 
                padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 3px; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔬 PyBiorythm Django API Example</h1>
            <p>Simple demonstration of serving PyBiorythm data through Django REST Framework.</p>
            
            <div class="endpoint">
                <h3>📊 Quick Test</h3>
                <p>Test the API with your birthdate:</p>
                <input type="date" id="birthdate" placeholder="Birth date">
                <input type="number" id="days" value="7" min="1" max="30" placeholder="Days">
                <button onclick="testAPI()">Calculate Biorhythm</button>
                <div id="result" style="margin-top: 15px;"></div>
            </div>
            
            <div class="endpoint">
                <h3>📋 API Endpoints</h3>
                <p><strong>GET /api/</strong> - API information</p>
                <p><strong>POST /api/calculate/</strong> - Full biorhythm calculation</p>
                <p><strong>GET /api/quick/</strong> - Quick calculation via query parameters</p>
            </div>
            
            <div class="endpoint">
                <h3>💡 Example Requests</h3>
                <div class="example">
                    <strong>Quick GET:</strong><br>
                    <code>/api/quick/?birthdate=1990-05-15&days=7</code>
                </div>
                <div class="example">
                    <strong>POST JSON:</strong><br>
                    <code>{"birthdate": "1990-05-15", "target_date": "2024-08-10", "days": 30}</code>
                </div>
            </div>
        </div>
        
        <script>
            function testAPI() {
                const birthdate = document.getElementById('birthdate').value;
                const days = document.getElementById('days').value || 7;
                const resultDiv = document.getElementById('result');
                
                if (!birthdate) {
                    resultDiv.innerHTML = '<span style="color: red;">Please enter your birth date</span>';
                    return;
                }
                
                resultDiv.innerHTML = 'Calculating...';
                
                fetch(`/api/quick/?birthdate=${birthdate}&days=${days}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            resultDiv.innerHTML = `<span style="color: red;">Error: ${data.error}</span>`;
                        } else {
                            resultDiv.innerHTML = `
                                <h4>✅ Calculation Successful!</h4>
                                <p><strong>Birthdate:</strong> ${data.birthdate}</p>
                                <p><strong>Days calculated:</strong> ${data.days}</p>
                                <p><strong>Data points:</strong> ${data.biorhythm_data.data.length}</p>
                                <details>
                                    <summary>📋 Raw JSON Response</summary>
                                    <pre style="background: #f0f0f0; padding: 10px; overflow: auto; max-height: 300px;">${JSON.stringify(data, null, 2)}</pre>
                                </details>
                            `;
                        }
                    })
                    .catch(error => {
                        resultDiv.innerHTML = `<span style="color: red;">Request failed: ${error.message}</span>`;
                    });
            }
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_content, content_type="text/html")
