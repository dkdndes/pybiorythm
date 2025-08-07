#!/bin/bash
# Build script for Biorythm Docker images

set -e  # Exit on any error

echo "Building Biorythm Docker images..."

# Build production image (multi-stage, minimal)
echo "Building production image..."
docker build --target production -t biorythm:latest .

# Build development image (optional)
echo "Building development image..."
docker build --target builder -t biorythm:dev .

# Show image sizes
echo -e "\nImage sizes:"
docker images | grep biorythm

# Test the production image
echo -e "\nTesting production image..."
docker run --rm biorythm:latest python -c "
import biorythm
from datetime import datetime
calc = biorythm.BiorhythmCalculator()
result = calc.calculate_biorhythm_values(datetime(1990, 5, 15), datetime(2023, 6, 1))
print('Production image test passed!')
print(f'Sample calculation result: {result}')
"

echo -e "\nBuild completed successfully!"
echo "Usage examples:"
echo "  docker run -it biorythm:latest  # Interactive mode"
echo "  docker run biorythm:latest python main.py -y 1990 -m 5 -d 15  # With arguments"
echo "  docker-compose up biorythm  # Using docker-compose"