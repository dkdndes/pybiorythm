# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Multi-Environment CI/CD Pipeline**: Complete deployment strategy supporting dev/staging/prod environments
- **Blue-Green Deployment**: Zero-downtime deployment with traffic switching capabilities
- **Docker Image Generation**: Automatic multi-architecture builds for all branch types with semantic versioning
- **BSI TR-03183-2-2 Compliant SBOM**: German security standard compliant Software Bill of Materials
- **Local Testing Framework**: Complete act-based local GitHub Actions testing with M2 Mac optimization
- **Comprehensive Security Scanning**: Trivy, CodeQL, Bandit, and Safety vulnerability scanning
- **Environment-Specific Configuration**: Dev/staging/prod configuration with resource allocation
- **Kubernetes Manifests**: Auto-generated deployment manifests with health checks and auto-scaling
- **Performance Benchmarking**: Automated performance testing with regression detection
- **Docker Compose Support**: Local development with environment-specific compose files

### Enhanced
- **Test Coverage**: Expanded to 89%+ with comprehensive integration and unit tests  
- **Docker Security**: Non-root containers, multi-stage builds, and security validation
- **Documentation**: Added deployment guide, Docker M2 guide, and local testing documentation
- **GitHub Actions**: Updated all actions to latest versions, eliminated deprecated warnings
- **JSON Output**: Enhanced biorhythm visualization with proper JSON formatting and validation

### Infrastructure
- **Branch Strategy**: Feature branches → develop → main with automatic version generation
- **Version Management**: Semantic versioning with branch-specific tags (dev-latest, staging-latest)  
- **Artifact Management**: 365-day retention for SBOMs, 90-day for security reports
- **Environment Protection**: Production deployments with approval requirements
- **Rollback Capabilities**: Instant rollback with blue-green deployment strategy
- **Monitoring Integration**: Health checks, metrics endpoints, and observability features

### Security
- **Supply Chain Security**: Complete SBOM generation with SHA-512 checksums
- **Vulnerability Management**: Automated scanning with GitHub Security tab integration
- **Container Security**: Distroless base images, non-root execution, minimal attack surface
- **Secret Management**: Environment-specific secrets with proper access control
- **Compliance**: BSI TR-03183-2-2 compliant security documentation and processes

### Developer Experience  
- **Local Development**: One-command setup with Docker Compose and act integration
- **M2 Mac Support**: Optimized for Apple Silicon with ARM64/AMD64 builds
- **Interactive Testing**: Local GitHub Actions testing with real workflow validation
- **Auto-Documentation**: Generated deployment guides and troubleshooting documentation
- **Quality Gates**: Automated linting, formatting, and test coverage enforcement

## [1.0.0] - 2024-12-07

### Added
- Initial release of pybiorythm biorhythm calculation library
- Core biorhythm calculation algorithms for physical, emotional, and intellectual cycles
- Command-line interface with multiple output formats (text, horizontal, JSON)
- Python package structure with proper dependencies management
- Basic test suite with pytest framework
- Docker containerization support
- GitHub Actions basic CI pipeline

### Features
- Calculate biorhythm values for any given date and birth date
- Support for different visualization orientations (vertical, horizontal)
- Customizable day range calculations
- JSON output format for API integration
- Cross-platform compatibility (Linux, macOS, Windows)

---

## Version History Summary

- **v1.0.0**: Initial release with core biorhythm calculations
- **v1.1.0**: Enhanced CI/CD pipeline and Docker support (upcoming)
- **v1.2.0**: Multi-environment deployment and blue-green strategy (upcoming)
- **v2.0.0**: Full production-ready enterprise features (planned)

## Migration Guide

### From v0.x to v1.0.0
No breaking changes - direct upgrade supported.

### Upcoming v1.1.0 Changes
- Enhanced Docker images with semantic versioning
- New environment-specific deployment options
- Improved security scanning and SBOM generation

## Contributing

This project follows conventional commits for automatic changelog generation:
- `feat:` for new features
- `fix:` for bug fixes  
- `docs:` for documentation changes
- `test:` for test improvements
- `ci:` for CI/CD pipeline changes
- `security:` for security-related changes

---

*This changelog is automatically maintained by semantic-release based on conventional commits.*
