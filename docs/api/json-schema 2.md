# JSON Schema Reference

This document describes the JSON schemas used by PyBiorythm for data exchange, validation, and API responses.

## Overview

PyBiorythm generates structured JSON data for programmatic access to biorhythm calculations. The JSON format is designed to be:

- **Self-documenting**: Includes comprehensive metadata
- **Scientifically responsible**: Contains prominent pseudoscience warnings
- **Machine-readable**: Consistent schema for automated processing
- **Validation-ready**: Follows JSON Schema standards

## Main JSON Schema

### Biorhythm Timeseries Response

The primary JSON output from `generate_timeseries_json()` follows this schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "Biorhythm Timeseries Data",
  "description": "Comprehensive biorhythm calculation results with metadata and scientific warnings",
  "required": ["meta", "cycle_repeats", "critical_days", "data"],
  "properties": {
    "meta": {
      "$ref": "#/definitions/Meta"
    },
    "cycle_repeats": {
      "$ref": "#/definitions/CycleRepeats"
    },
    "critical_days": {
      "$ref": "#/definitions/CriticalDays"
    },
    "data": {
      "$ref": "#/definitions/TimeseriesData"
    }
  },
  "definitions": {
    "Meta": {
      "type": "object",
      "description": "Metadata about the calculation and scientific warnings",
      "required": [
        "generator", "version", "birthdate", "plot_date", "days_alive",
        "cycle_lengths_days", "chart_orientation", "days", "width",
        "scientific_warning"
      ],
      "properties": {
        "generator": {
          "type": "string",
          "description": "Name of the generating program",
          "example": "biorhythm_enhanced.py"
        },
        "version": {
          "type": "string",
          "description": "Version of the generator",
          "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
          "example": "2025-08-07"
        },
        "birthdate": {
          "type": "string",
          "format": "date",
          "description": "Subject's birth date",
          "example": "1990-05-15"
        },
        "plot_date": {
          "type": "string", 
          "format": "date",
          "description": "Starting date for the calculations",
          "example": "2025-08-07"
        },
        "days_alive": {
          "type": "integer",
          "minimum": 0,
          "description": "Number of days the subject has been alive",
          "example": 12837
        },
        "cycle_lengths_days": {
          "$ref": "#/definitions/CycleLengths"
        },
        "chart_orientation": {
          "type": "string",
          "enum": ["vertical", "horizontal"],
          "description": "Chart display orientation",
          "example": "vertical"
        },
        "days": {
          "type": "integer",
          "minimum": 1,
          "description": "Number of days included in the dataset",
          "example": 29
        },
        "width": {
          "type": "integer",
          "minimum": 12,
          "description": "Chart width in characters",
          "example": 55
        },
        "scientific_warning": {
          "type": "string",
          "description": "Mandatory scientific disclaimer about biorhythm pseudoscience",
          "minLength": 100
        }
      }
    },
    "CycleLengths": {
      "type": "object",
      "description": "Biorhythm cycle periods in days",
      "required": ["physical", "emotional", "intellectual"],
      "properties": {
        "physical": {
          "type": "integer",
          "const": 23,
          "description": "Physical cycle length (fixed at 23 days)"
        },
        "emotional": {
          "type": "integer", 
          "const": 28,
          "description": "Emotional cycle length (fixed at 28 days)"
        },
        "intellectual": {
          "type": "integer",
          "const": 33,
          "description": "Intellectual cycle length (fixed at 33 days)"
        }
      }
    },
    "CycleRepeats": {
      "type": "object",
      "description": "Information about when biorhythm cycles repeat",
      "required": ["physical_emotional_repeat_in_days", "all_cycles_repeat_in_days"],
      "properties": {
        "physical_emotional_repeat_in_days": {
          "type": "integer",
          "minimum": 1,
          "maximum": 644,
          "description": "Days until physical and emotional cycles align again",
          "example": 234
        },
        "all_cycles_repeat_in_days": {
          "type": "integer",
          "minimum": 1,
          "maximum": 21252,
          "description": "Days until all three cycles align again",
          "example": 15678
        }
      }
    },
    "CriticalDays": {
      "type": "array",
      "description": "List of days when cycles are near zero (critical days)",
      "items": {
        "$ref": "#/definitions/CriticalDay"
      }
    },
    "CriticalDay": {
      "type": "object",
      "description": "A single critical day entry",
      "required": ["date", "cycles"],
      "properties": {
        "date": {
          "type": "string",
          "format": "date",
          "description": "Date of the critical day",
          "example": "2025-08-15"
        },
        "cycles": {
          "type": "string",
          "description": "Description of which cycles are critical",
          "pattern": ".+ cycle\\(s\\) near zero$",
          "example": "Physical, Emotional cycle(s) near zero"
        }
      }
    },
    "TimeseriesData": {
      "type": "array",
      "description": "Daily biorhythm calculations",
      "minItems": 1,
      "items": {
        "$ref": "#/definitions/DailyCalculation"
      }
    },
    "DailyCalculation": {
      "type": "object",
      "description": "Biorhythm values for a single day",
      "required": [
        "date", "days_alive", "physical", "emotional", 
        "intellectual", "critical_cycles"
      ],
      "properties": {
        "date": {
          "type": "string",
          "format": "date",
          "description": "Date for this calculation",
          "example": "2025-08-07"
        },
        "days_alive": {
          "type": "integer",
          "minimum": 0,
          "description": "Days alive on this date",
          "example": 12837
        },
        "physical": {
          "type": "number",
          "minimum": -1.0,
          "maximum": 1.0,
          "description": "Physical cycle value (-1.0 to +1.0)",
          "example": -0.899
        },
        "emotional": {
          "type": "number",
          "minimum": -1.0,
          "maximum": 1.0, 
          "description": "Emotional cycle value (-1.0 to +1.0)",
          "example": 0.974
        },
        "intellectual": {
          "type": "number",
          "minimum": -1.0,
          "maximum": 1.0,
          "description": "Intellectual cycle value (-1.0 to +1.0)",
          "example": -0.951
        },
        "critical_cycles": {
          "type": "array",
          "description": "List of cycles that are critical (near zero) on this day",
          "items": {
            "type": "string",
            "enum": ["Physical", "Emotional", "Intellectual"]
          },
          "example": ["Physical"]
        }
      }
    }
  }
}
```

## Example JSON Response

### Complete Response Example

```json
{
  "meta": {
    "generator": "biorhythm_enhanced.py",
    "version": "2025-08-07",
    "birthdate": "1990-05-15",
    "plot_date": "2025-08-07",
    "days_alive": 12837,
    "cycle_lengths_days": {
      "physical": 23,
      "emotional": 28,
      "intellectual": 33
    },
    "chart_orientation": "vertical",
    "days": 7,
    "width": 55,
    "scientific_warning": "⚠️  SCIENTIFIC WARNING ⚠️\nBiorhythm theory is PSEUDOSCIENCE with NO scientific evidence.\nMultiple peer-reviewed studies have found NO correlation between\nbiorhythm cycles and human performance beyond random chance.\nThis program is provided for ENTERTAINMENT PURPOSES ONLY."
  },
  "cycle_repeats": {
    "physical_emotional_repeat_in_days": 234,
    "all_cycles_repeat_in_days": 15678
  },
  "critical_days": [
    {
      "date": "2025-08-09",
      "cycles": "Physical cycle(s) near zero"
    }
  ],
  "data": [
    {
      "date": "2025-08-04",
      "days_alive": 12834,
      "physical": -0.743,
      "emotional": 0.891,
      "intellectual": -0.845,
      "critical_cycles": []
    },
    {
      "date": "2025-08-05",
      "days_alive": 12835,
      "physical": -0.829,
      "emotional": 0.951,
      "intellectual": -0.891,
      "critical_cycles": []
    },
    {
      "date": "2025-08-06",
      "days_alive": 12836,
      "physical": -0.899,
      "emotional": 0.988,
      "intellectual": -0.921,
      "critical_cycles": []
    },
    {
      "date": "2025-08-07",
      "days_alive": 12837,
      "physical": -0.951,
      "emotional": 1.000,
      "intellectual": -0.934,
      "critical_cycles": []
    },
    {
      "date": "2025-08-08",
      "days_alive": 12838,
      "physical": -0.988,
      "emotional": 0.988,
      "intellectual": -0.934,
      "critical_cycles": []
    },
    {
      "date": "2025-08-09",
      "days_alive": 12839,
      "physical": -0.009,
      "emotional": 0.951,
      "intellectual": -0.921,
      "critical_cycles": ["Physical"]
    },
    {
      "date": "2025-08-10",
      "days_alive": 12840,
      "physical": 0.034,
      "emotional": 0.891,
      "intellectual": -0.891,
      "critical_cycles": []
    }
  ]
}
```

## Schema Validation

### Using JSON Schema Libraries

#### Python Validation

```python
import json
import jsonschema
from biorythm import BiorhythmCalculator
from datetime import datetime

# Generate data
calc = BiorhythmCalculator(days=7)
json_str = calc.generate_timeseries_json(datetime(1990, 5, 15))
data = json.loads(json_str)

# Load schema (assuming schema is saved as biorhythm_schema.json)
with open('biorhythm_schema.json', 'r') as f:
    schema = json.load(f)

# Validate
try:
    jsonschema.validate(instance=data, schema=schema)
    print("JSON data is valid!")
except jsonschema.ValidationError as e:
    print(f"Validation error: {e}")
```

#### JavaScript Validation

```javascript
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv();
addFormats(ajv);

// Load schema and data
const schema = require('./biorhythm_schema.json');
const data = require('./biorhythm_data.json');

// Validate
const validate = ajv.compile(schema);
const valid = validate(data);

if (!valid) {
    console.error('Validation errors:', validate.errors);
} else {
    console.log('Data is valid!');
}
```

## Data Access Patterns

### Extracting Specific Information

```python
import json
from datetime import datetime

# Parse JSON response
data = json.loads(json_response)

# Access metadata
birthdate = data['meta']['birthdate']
days_alive = data['meta']['days_alive']
warning = data['meta']['scientific_warning']

# Access cycle information
physical_cycle = data['meta']['cycle_lengths_days']['physical']
next_repeat = data['cycle_repeats']['all_cycles_repeat_in_days']

# Access critical days
critical_dates = [day['date'] for day in data['critical_days']]

# Access daily calculations
daily_data = data['data']
for day in daily_data:
    date = day['date']
    p_val = day['physical']
    e_val = day['emotional']
    i_val = day['intellectual']
    critical = day['critical_cycles']
    
    print(f"{date}: P={p_val:.3f}, E={e_val:.3f}, I={i_val:.3f}")
    if critical:
        print(f"  Critical: {', '.join(critical)}")
```

### Data Analysis with Pandas

```python
import pandas as pd
import json

# Convert to DataFrame
data = json.loads(json_response)
df = pd.DataFrame(data['data'])

# Convert date column
df['date'] = pd.to_datetime(df['date'])

# Basic statistics
print("Cycle Statistics:")
print(df[['physical', 'emotional', 'intellectual']].describe())

# Find extremes
physical_max_idx = df['physical'].idxmax()
physical_max_day = df.loc[physical_max_idx]
print(f"Physical peak: {physical_max_day['date']} ({physical_max_day['physical']:.3f})")

# Critical day analysis
critical_df = df[df['critical_cycles'].apply(len) > 0]
print(f"Found {len(critical_df)} critical days")
```

## Schema Versioning

### Version Compatibility

The JSON schema follows semantic versioning principles:

- **Major version**: Breaking changes to required fields or data types
- **Minor version**: New optional fields or enhancements  
- **Patch version**: Bug fixes and clarifications

Current schema version: `1.0.0`

### Backward Compatibility

```python
def handle_json_response(json_str):
    """Handle JSON responses with version compatibility."""
    data = json.loads(json_str)
    
    # Check version compatibility
    version = data['meta'].get('version', 'unknown')
    
    if version.startswith('2025-'):
        # Current format
        return process_current_format(data)
    else:
        # Handle older formats
        return process_legacy_format(data)

def process_current_format(data):
    """Process current JSON format."""
    return {
        'birthdate': data['meta']['birthdate'],
        'days_data': data['data'],
        'critical_days': data['critical_days'],
        'warning': data['meta']['scientific_warning']
    }
```

## Custom Schema Extensions

### Adding Custom Fields

For applications that need additional metadata, extend the schema:

```json
{
  "allOf": [
    {"$ref": "#/definitions/BiorhythmTimeseries"},
    {
      "type": "object",
      "properties": {
        "custom_meta": {
          "type": "object",
          "properties": {
            "user_id": {"type": "string"},
            "analysis_id": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"}
          }
        }
      }
    }
  ]
}
```

### Application-Specific Schemas

```python
def extend_json_output(calculator, birthdate, user_context):
    """Generate extended JSON with application-specific data."""
    base_json = calculator.generate_timeseries_json(birthdate)
    base_data = json.loads(base_json)
    
    # Add custom metadata
    base_data['custom_meta'] = {
        'user_id': user_context.get('user_id'),
        'analysis_id': generate_analysis_id(),
        'created_at': datetime.now().isoformat(),
        'timezone': user_context.get('timezone', 'UTC')
    }
    
    # Add calculated fields
    base_data['analysis'] = {
        'average_physical': statistics.mean(
            day['physical'] for day in base_data['data']
        ),
        'cycle_correlation': calculate_cycle_correlation(base_data['data']),
        'volatility_score': calculate_volatility(base_data['data'])
    }
    
    return json.dumps(base_data, indent=2)
```

## Error Schema

### Validation Errors

When validation fails, errors follow this schema:

```json
{
  "type": "object",
  "required": ["error", "code", "message"],
  "properties": {
    "error": {
      "type": "string",
      "enum": ["validation_error", "calculation_error", "date_error"]
    },
    "code": {
      "type": "integer",
      "minimum": 400,
      "maximum": 599
    },
    "message": {
      "type": "string",
      "description": "Human-readable error message"
    },
    "details": {
      "type": "object",
      "description": "Additional error context"
    }
  }
}
```

**Example Error Response:**
```json
{
  "error": "date_error",
  "code": 400,
  "message": "Birth date cannot be in the future",
  "details": {
    "provided_date": "2030-01-01",
    "current_date": "2025-08-07",
    "field": "birthdate"
  }
}
```

## Best Practices

### Schema Design
- Always include scientific warning in metadata
- Use consistent date formatting (ISO 8601)
- Provide comprehensive field descriptions
- Include value ranges and constraints
- Version your schema properly

### Validation
- Validate all input data before processing
- Handle version compatibility gracefully
- Provide clear error messages
- Log validation failures for debugging

### Performance
- Use streaming JSON parsers for large datasets
- Cache compiled schemas for repeated validation
- Consider schema compression for large responses
- Implement pagination for very large date ranges

---

**Next**: [Error Handling](errors.md) | [Core API](core.md) | [Calculator API](calculator.md)