# PyBiorythm Docker Image

[![Docker](https://img.shields.io/badge/docker-multi--stage-blue.svg)](./Dockerfile)
[![GitHub Container Registry](https://img.shields.io/badge/ghcr.io-pybiorythm-green.svg)](https://github.com/dkdndes/pybiorythm/pkgs/container/pybiorythm)

A containerized biorhythm calculation library with multi-architecture support.

## Quick Start

### Pull and Run
```bash
# Pull latest image
docker pull ghcr.io/dkdndes/pybiorythm:latest

# Run with example calculation
docker run --rm ghcr.io/dkdndes/pybiorythm:latest python main.py -y 1990 -m 5 -d 15
```

### Interactive Mode
```bash
# Run interactively
docker run -it ghcr.io/dkdndes/pybiorythm:latest bash

# Or use the default command
docker run -it ghcr.io/dkdndes/pybiorythm:latest
```

## Available Tags

- `latest` - Latest stable release
- `main` - Latest from main branch
- `develop-latest` - Latest development build
- `v2.8.0` - Specific version tags

## Image Features

✅ **Multi-Architecture**: AMD64 and ARM64 support  
✅ **Security**: Non-root user execution  
✅ **Minimal Size**: Multi-stage build optimization  
✅ **Health Checks**: Built-in container health monitoring  
✅ **Dynamic Versioning**: Git-based version management  

## Usage Examples

### Basic Calculation
```bash
docker run --rm ghcr.io/dkdndes/pybiorythm:latest \
  python main.py --year 1990 --month 5 --day 15 --days 30
```

### JSON Output
```bash
docker run --rm ghcr.io/dkdndes/pybiorythm:latest \
  python main.py -y 1990 -m 5 -d 15 --orientation json-vertical
```

### Mount Volume for Output
```bash
docker run --rm -v $(pwd):/output ghcr.io/dkdndes/pybiorythm:latest \
  python main.py -y 1990 -m 5 -d 15 > /output/biorhythm.txt
```

## Development Images

Development builds are available with environment-specific tags:

```bash
# Development environment
docker pull ghcr.io/dkdndes/pybiorythm:dev-latest

# Staging environment  
docker pull ghcr.io/dkdndes/pybiorythm:staging-latest
```

## Docker Compose

```yaml
version: '3.8'
services:
  pybiorythm:
    image: ghcr.io/dkdndes/pybiorythm:latest
    container_name: pybiorythm
    command: python main.py -y 1990 -m 5 -d 15
    restart: unless-stopped
```

## Building Locally

```bash
# Clone repository
git clone https://github.com/dkdndes/pybiorythm.git
cd pybiorythm

# Build image
docker build -t pybiorythm:local .

# Run local build
docker run --rm pybiorythm:local python main.py -y 1990 -m 5 -d 15
```

## Security

- **Non-root execution**: Container runs as `biorythm` user
- **Minimal attack surface**: Multi-stage build removes build dependencies
- **Regular security scans**: Trivy vulnerability scanning in CI/CD
- **SBOM included**: Software Bill of Materials for compliance

## Health Check

The container includes a health check that verifies the Python module can be imported:

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' <container_id>
```

## Environment Variables

- `PYTHONUNBUFFERED=1` - Real-time output
- `PYTHONDONTWRITEBYTECODE=1` - No .pyc files
- `PYTHONPATH=/app` - Python module path

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker logs <container_id>

# Run with debug
docker run --rm -it ghcr.io/dkdndes/pybiorythm:latest bash
```

### Import Errors
```bash
# Verify installation
docker run --rm ghcr.io/dkdndes/pybiorythm:latest python -c "import biorythm; print('OK')"
```

## Scientific Disclaimer

⚠️ **This software implements biorhythm theory, which is considered PSEUDOSCIENCE.** This containerized implementation is provided FOR ENTERTAINMENT PURPOSES ONLY and should NOT be used for making important life decisions.

## Support

- **Issues**: [GitHub Issues](https://github.com/dkdndes/pybiorythm/issues)
- **Documentation**: [Project README](https://github.com/dkdndes/pybiorythm)
- **Registry**: [GitHub Container Registry](https://github.com/dkdndes/pybiorythm/pkgs/container/pybiorythm)