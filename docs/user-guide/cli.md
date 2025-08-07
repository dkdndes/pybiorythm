# Command Line Interface

PyBiorythm provides a comprehensive command-line interface for generating biorhythm charts and JSON data.

## Basic Usage

```bash
python main.py [OPTIONS]
```

## Options

| Option | Short | Type | Description | Default |
|--------|-------|------|-------------|---------|
| `--year` | `-y` | int | Birth year (1-9999) | Interactive prompt |
| `--month` | `-m` | int | Birth month (1-12) | Interactive prompt |
| `--day` | `-d` | int | Birth day (1-31) | Interactive prompt |
| `--orientation` | | choice | Chart orientation | `vertical` |
| `--days` | | int | Number of days to plot | 29 |
| `--help` | `-h` | | Show help message | |

## Orientation Options

- `vertical` - Traditional vertical chart (default)
- `horizontal` - Timeline-style horizontal chart  
- `json-vertical` - JSON output with vertical metadata
- `json-horizontal` - JSON output with horizontal metadata

## Examples

### Interactive Mode
```bash
# Start interactive mode
python main.py

# You will be prompted for:
# Birth year: 1990
# Birth month: 5
# Birth day: 15
```

### Basic Commands
```bash
# Simple chart for May 15, 1990
python main.py -y 1990 -m 5 -d 15

# Horizontal timeline view
python main.py -y 1990 -m 5 -d 15 --orientation horizontal

# Extended 60-day period
python main.py -y 1990 -m 5 -d 15 --days 60
```

### JSON Output
```bash
# JSON data for analysis
python main.py -y 1990 -m 5 -d 15 --orientation json-vertical

# Redirect JSON to file
python main.py -y 1990 -m 5 -d 15 --orientation json-vertical > biorhythm_data.json
```

## Output Examples

### Vertical Chart Output
```
=== BIORHYTHM CHART ===
Birth Date: 1990-05-15
Chart Date: 2025-08-07 (12837 days alive)

⚠️  SCIENTIFIC WARNING ⚠️
Biorhythm theory is PSEUDOSCIENCE with no proven validity!
Use for entertainment and educational purposes only.

Key: Physical (p), Emotional (e), Intellectual (i)
Critical days marked when cycles cross zero line (:)

Thu Aug  7    p     :     e i    
Fri Aug  8       p  :  e      i  
Sat Aug  9          : p    e   i 
```

### Horizontal Chart Output
```
=== BIORHYTHM WAVE (Physical + Emotional + Intellectual) ===
                    e               
            p               i       
                        e           
```

### JSON Output Structure
```json
{
  "meta": {
    "generator": "biorythm",
    "version": "1.2.1",
    "birthdate": "1990-05-15",
    "plot_date": "2025-08-07",
    "days_alive": 12837,
    "cycle_lengths_days": {
      "physical": 23,
      "emotional": 28,
      "intellectual": 33
    },
    "chart_orientation": "vertical",
    "days": 29,
    "width": 55
  },
  "data": [
    {
      "date": "2025-07-24",
      "days_alive": 12823,
      "physical": -0.8987940462991669,
      "emotional": 0.9744583088414919,
      "intellectual": -0.9510565162951536,
      "critical_cycles": []
    }
  ]
}
```

## Error Handling

The CLI provides helpful error messages for invalid inputs:

```bash
# Invalid date
python main.py -y 1990 -m 13 -d 15
# Error: Month must be between 1 and 12

# Invalid year  
python main.py -y 0 -m 5 -d 15
# Error: Year must be between 1 and 9999

# Invalid day for month
python main.py -y 1990 -m 2 -d 30
# Error: Day 30 is not valid for February 1990
```

## Docker Usage

Run CLI commands in Docker:

```bash
# Interactive mode
docker run -it biorythm:latest

# Direct command
docker run biorythm:latest python main.py -y 1990 -m 5 -d 15

# JSON output to host file
docker run biorythm:latest python main.py -y 1990 -m 5 -d 15 --orientation json-vertical > data.json
```

## Scripting and Automation

### Batch Processing
```bash
#!/bin/bash
# Generate charts for multiple birthdates

birthdates=(
    "1980-01-01"
    "1990-05-15"
    "2000-12-31"
)

for birthdate in "${birthdates[@]}"; do
    IFS='-' read -r year month day <<< "$birthdate"
    echo "Generating chart for $birthdate..."
    python main.py -y "$year" -m "$month" -d "$day" --orientation json-vertical > "chart_${birthdate}.json"
done
```

### Python Integration
```python
import subprocess
import json

def generate_biorhythm_data(year, month, day):
    """Generate biorhythm data using CLI"""
    result = subprocess.run([
        'python', 'main.py', 
        '-y', str(year), 
        '-m', str(month), 
        '-d', str(day),
        '--orientation', 'json-vertical'
    ], capture_output=True, text=True)
    
    return json.loads(result.stdout)

# Usage
data = generate_biorhythm_data(1990, 5, 15)
print(f"Physical: {data['data'][0]['physical']}")
```

## Performance Notes

- Chart generation: < 1ms for typical periods (29 days)
- JSON generation: < 10ms for full year (365 days)  
- Memory usage: < 10MB for large datasets
- Supports periods up to 10,000 days efficiently

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Invalid arguments or date |
| 2 | File I/O error |
| 3 | Calculation error |

Use in scripts:
```bash
python main.py -y 1990 -m 5 -d 15
if [ $? -eq 0 ]; then
    echo "Chart generated successfully"
else
    echo "Error generating chart"
fi
```