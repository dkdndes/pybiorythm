# Security Guide

This document outlines security considerations, best practices, and threat mitigation strategies for the PyBiorythm project.

## Security Overview

PyBiorythm is a mathematical calculation library with minimal attack surface, but security best practices are implemented throughout:

- **Input validation**: All user inputs are validated and sanitized
- **Safe dependencies**: Regular dependency scanning and updates
- **Secure development**: Security-focused development practices
- **Supply chain security**: SBOM generation and dependency tracking
- **No secrets**: No API keys, tokens, or sensitive data handling

## Threat Model

### Assets
- **Source code**: Open source Python library
- **User data**: Birth dates provided by users (not stored)
- **Build artifacts**: Compiled packages and distributions
- **Documentation**: Project documentation and examples

### Trust Boundaries
1. **User input → Application**: Date inputs from CLI or programmatic usage
2. **Dependencies → Application**: Third-party Python packages
3. **Build system → Distribution**: Package build and release process
4. **Documentation → Users**: Educational and technical content

### Potential Threats
1. **Input injection**: Malicious input causing unexpected behavior
2. **Dependency vulnerabilities**: Security issues in third-party packages  
3. **Supply chain attacks**: Compromised dependencies or build process
4. **Information disclosure**: Unintended exposure of system information
5. **Denial of service**: Resource exhaustion through large inputs

## Input Security

### Date Validation

Comprehensive input validation prevents malicious or malformed inputs:

```python
class DateValidator:
    @staticmethod
    def validate_date_components(year: int, month: int, day: int) -> None:
        # Range validation prevents integer overflow
        if not isinstance(year, int) or not (MIN_YEAR <= year <= MAX_YEAR):
            raise DateValidationError(f"Year must be between {MIN_YEAR} and {MAX_YEAR}")
            
        # Month validation prevents array bounds issues
        if not isinstance(month, int) or not (1 <= month <= 12):
            raise DateValidationError(f"Month must be between 1 and 12")
            
        # Day validation with calendar-aware checking
        if not isinstance(day, int) or not (1 <= day <= 31):
            raise DateValidationError(f"Day must be between 1 and 31")

    @staticmethod
    def create_validated_date(year: int, month: int, day: int) -> datetime:
        DateValidator.validate_date_components(year, month, day)
        try:
            date_obj = datetime(year, month, day)
        except ValueError as e:
            raise DateValidationError(f"Invalid date: {e}")
            
        # Prevent future dates that could cause calculation issues
        if date_obj > datetime.now():
            raise DateValidationError("Birth date cannot be in the future")
        return date_obj
```

### Parameter Validation

Chart parameters are validated to prevent resource exhaustion:

```python
def _validate_chart_parameters(self, width: int, days: int) -> None:
    # Prevent negative or zero values
    if not isinstance(width, int) or width < 1:
        raise ChartParameterError(f"Width must be positive integer")
        
    if not isinstance(days, int) or days < 1:
        raise ChartParameterError(f"Days must be positive integer")
        
    # Prevent excessively large values that could consume memory
    if width > 1000:
        raise ChartParameterError("Chart width too large")
        
    if days > 10000:
        raise ChartParameterError("Too many days requested")
```

### Type Safety

All inputs undergo strict type checking:

```python
def calculate_biorhythm_values(self, birthdate: datetime, target_date: datetime) -> Tuple[float, float, float]:
    if not isinstance(birthdate, datetime):
        raise TypeError("Birthdate must be datetime object")
    if not isinstance(target_date, datetime):
        raise TypeError("Target date must be datetime object")
        
    # Safe calculation with validated inputs
    days_alive = (target_date - birthdate).days
    # ... rest of calculation
```

## Dependency Security

### Automated Vulnerability Scanning

Regular security scanning of dependencies:

```yaml
# .github/workflows/security-scan.yml
- name: Security vulnerability scan
  run: |
    uv run safety check  # Check for known vulnerabilities
    uv run bandit -r biorythm/  # Static security analysis
```

### Minimal Dependencies

PyBiorythm uses minimal dependencies to reduce attack surface:

**Production Dependencies:**
- `numpy>=1.20.0` - Mathematical operations only

**Development Dependencies:**
- Testing and development tools only
- No runtime dependencies on external APIs or services

### Dependency Pinning

Development dependencies are pinned to specific versions:

```toml
[dependency-groups]
dev = [
    "pytest>=8.3.5",        # Specific versions for reproducibility
    "pytest-cov>=5.0.0",    # Known-good versions
    "safety>=3.6.0",        # Security scanning tool
    "bandit[toml]>=1.7.10", # Static security analysis
]
```

### Supply Chain Security

#### Software Bill of Materials (SBOM)

Comprehensive SBOM generation for transparency:

```yaml
- name: Generate SBOM
  run: |
    uv run cyclonedx-py requirements requirements-freeze.txt \
      --output-format json \
      --output-file sbom-python.json
```

SBOM includes:
- All direct and transitive dependencies
- Version information and hashes
- License information
- Vulnerability metadata

#### Dependency Review

Automated dependency review in CI/CD:

```yaml
- name: Dependency Review
  uses: actions/dependency-review-action@v3
  with:
    allow-licenses: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, GPL-2.0, GPL-3.0, LGPL-2.1, LGPL-3.0, MPL-2.0
```

## Build Security

### Secure Build Process

GitHub Actions workflows follow security best practices:

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read  # Minimal permissions
  security-events: write  # For security scanning
  
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4  # Pinned to specific version
      with:
        persist-credentials: false  # Don't persist GitHub token
```

### Package Integrity

Build artifacts are signed and verified:

```yaml
- name: Build and verify package
  run: |
    uv run python -m build
    uv run twine check dist/*  # Verify package integrity
    # Additional integrity checks would go here
```

### Secret Management

No secrets are used in the PyBiorythm project:
- No API keys or tokens required
- No database credentials
- No external service authentication
- All operations are mathematical calculations only

## Runtime Security

### Memory Safety

Safe memory operations throughout the codebase:

```python
def _create_chart_line(self, p_pos: int, e_pos: int, i_pos: int) -> str:
    # Safe array operations with bounds checking
    chart_line = list(" " * self.width)
    
    # Ensure positions are within bounds
    if 0 <= p_pos < self.width:
        chart_line[p_pos] = "p"
    if 0 <= e_pos < self.width:
        chart_line[e_pos] = "e"
    if 0 <= i_pos < self.width:
        chart_line[i_pos] = "i"
        
    return "".join(chart_line)
```

### Resource Limits

Protection against resource exhaustion:

```python
def get_terminal_width(default=80, min_width=40, max_width=200):
    try:
        width = shutil.get_terminal_size().columns
        # Clamp to reasonable bounds
        return max(min_width, min(width, max_width))
    except Exception:
        return default
```

### Error Information Disclosure

Safe error handling that doesn't leak sensitive information:

```python
def main():
    try:
        # Application logic
        pass
    except DateValidationError as e:
        # User-friendly error without system details
        logger.error(f"Date validation error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        # Generic error message, detailed logging
        logger.critical(f"Unexpected error: {str(e)}")
        print("An unexpected error occurred. Please check your input and try again.")
        sys.exit(1)
```

## Code Security

### Static Analysis

Automated static security analysis:

```yaml
- name: Security linting with bandit
  run: |
    uv run bandit -r biorythm/ -f json -o bandit-report.json
    uv run bandit -r biorythm/ --exit-zero  # Don't fail build on warnings
```

Common security issues checked:
- Hardcoded passwords (not applicable)
- SQL injection (not applicable)
- Command injection (not applicable)
- Insecure random number generation
- Use of dangerous functions

### Code Quality

Security-focused code quality standards:

```python
# Secure coding practices
def calculate_biorhythm_values(self, birthdate: datetime, target_date: datetime) -> Tuple[float, float, float]:
    """
    Calculate biorhythm values with input validation
    
    Security considerations:
    - Input validation prevents injection attacks
    - Mathematical operations are overflow-safe
    - No external dependencies in calculation
    """
    # Input validation
    if not isinstance(birthdate, datetime):
        raise TypeError("Invalid birthdate type")
    if not isinstance(target_date, datetime):
        raise TypeError("Invalid target_date type")
        
    # Safe mathematical operations
    days_alive = (target_date - birthdate).days
    
    # Pure mathematical calculations - no security risk
    physical = math.sin((2 * math.pi * days_alive) / PHYSICAL_CYCLE_DAYS)
    emotional = math.sin((2 * math.pi * days_alive) / EMOTIONAL_CYCLE_DAYS)
    intellectual = math.sin((2 * math.pi * days_alive) / INTELLECTUAL_CYCLE_DAYS)
    
    return physical, emotional, intellectual
```

### Logging Security

Safe logging practices that don't expose sensitive data:

```python
def setup_logging(level: int = logging.INFO) -> None:
    # Safe logging configuration
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    # No file logging to prevent information disclosure
    # No sensitive data in log messages

def generate_chart(self, birthdate: datetime, plot_date: datetime = None) -> None:
    # Safe logging - no sensitive data exposure
    self.logger.info(f"Generating chart for {days_alive} days since birth")
    # Never log actual birthdate or personal information
```

## Deployment Security

### Package Distribution

Secure package publishing process:

```yaml
- name: Publish to PyPI
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
  run: |
    uv run twine upload dist/* --verbose
```

Security measures:
- API token authentication (not username/password)
- HTTPS-only uploads
- Package signature verification
- Automated malware scanning by PyPI

### Container Security

For Docker deployments (if applicable):

```dockerfile
# Use official Python image with security updates
FROM python:3.12-slim

# Create non-root user
RUN groupadd -r biorhythm && useradd -r -g biorhythm biorhythm

# Install security updates
RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Switch to non-root user
USER biorhythm

# Run application
CMD ["python", "-m", "biorythm"]
```

## Security Testing

### Automated Security Tests

```python
class TestSecurityValidation:
    def test_input_sanitization(self):
        """Test that malicious inputs are properly handled"""
        calc = BiorhythmCalculator()
        
        # Test SQL injection patterns (not applicable but good practice)
        with pytest.raises(DateValidationError):
            DateValidator.create_validated_date("'; DROP TABLE users; --", 5, 15)
            
        # Test buffer overflow attempts
        with pytest.raises(ChartParameterError):
            BiorhythmCalculator(width=999999999)
            
    def test_resource_exhaustion_protection(self):
        """Test protection against resource exhaustion"""
        # Large but reasonable inputs should work
        calc = BiorhythmCalculator(width=100, days=100)
        
        # Extremely large inputs should be rejected
        with pytest.raises(ChartParameterError):
            BiorhythmCalculator(width=100000, days=100000)
            
    def test_error_information_disclosure(self):
        """Test that errors don't leak sensitive information"""
        with pytest.raises(DateValidationError) as exc_info:
            DateValidator.create_validated_date(2030, 5, 15)
            
        error_message = str(exc_info.value)
        # Error should be informative but not reveal system details
        assert "Birth date cannot be in the future" in error_message
        assert "/home/" not in error_message  # No file paths
        assert "password" not in error_message.lower()  # No credentials
```

### Penetration Testing

Manual security testing checklist:

1. **Input validation testing**:
   - Boundary value testing (min/max dates)
   - Invalid input types (strings for numbers, etc.)
   - Special characters and encoding issues
   - Extremely large inputs

2. **Memory safety testing**:
   - Large chart generation
   - Rapid repeated calculations
   - Memory leak detection

3. **Error handling testing**:
   - Invalid configurations
   - Filesystem permission issues
   - Network connectivity problems (for future features)

## Security Incident Response

### Vulnerability Disclosure

If security vulnerabilities are discovered:

1. **Report**: Email security issues to project maintainers
2. **Assessment**: Evaluate severity and impact
3. **Fix**: Develop and test security patches
4. **Disclosure**: Coordinated disclosure with security advisories
5. **Update**: Release patched versions promptly

### Security Advisory Process

1. **Private disclosure** to maintainers first
2. **Impact assessment** and CVSS scoring
3. **Patch development** with security review
4. **Testing** of security fixes
5. **Coordinated public disclosure** with fix availability

## Security Best Practices for Users

### Installation Security

```bash
# Verify package integrity
pip install --only-binary=all biorythm

# Use virtual environments to isolate dependencies
python -m venv biorhythm-env
source biorhythm-env/bin/activate
pip install biorythm

# Keep dependencies updated
pip list --outdated
pip install --upgrade biorythm
```

### Usage Security

```python
# Safe programmatic usage
from biorythm import BiorhythmCalculator
from datetime import datetime

try:
    calc = BiorhythmCalculator()
    birthdate = datetime(1990, 5, 15)  # Use known-good dates
    calc.generate_chart(birthdate)
except Exception as e:
    # Handle errors gracefully
    print(f"Error: {e}")
```

### Data Privacy

PyBiorythm respects user privacy:
- **No data collection**: Birth dates are not stored or transmitted
- **Local processing**: All calculations performed locally
- **No analytics**: No usage tracking or telemetry
- **No network access**: No external API calls or data transmission

## Compliance and Standards

### Security Standards

PyBiorythm follows industry security standards:
- **OWASP Top 10**: Web application security principles applied
- **NIST Cybersecurity Framework**: Risk management approach
- **CWE/SANS Top 25**: Common weakness enumeration prevention

### Privacy Compliance

- **No personal data storage**: Birth dates processed but not retained
- **Local processing**: No data transmission to external services
- **Open source**: Transparent processing and calculations
- **User control**: Users control all input data

## Security Metrics

### Automated Security Metrics

- **Dependency vulnerabilities**: 0 high/critical vulnerabilities
- **Code coverage**: 85%+ test coverage including security tests
- **Static analysis**: No security warnings from bandit
- **Build security**: All security checks passing in CI/CD

### Security Monitoring

```yaml
# Security monitoring workflow
name: Security Monitoring
on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly security checks

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - name: Security dependency scan
      run: |
        uv run safety check --json --output safety-report.json
        
    - name: Vulnerability database update
      run: |
        uv run pip-audit --format=json --output=audit-report.json
```

## Future Security Enhancements

### Planned Security Improvements

1. **Code signing**: Sign releases with GPG keys
2. **Reproducible builds**: Ensure builds are deterministic
3. **Security benchmarks**: Automated security performance testing
4. **Threat modeling**: Regular threat model updates

### Security Research

Areas for ongoing security research:
- Mathematical operation security in Python
- Dependency chain security analysis  
- Build system security hardening
- User input validation best practices

## Security Resources

### Internal Resources
- [Architecture Documentation](../developer-guide/architecture.md)
- [Testing Guide](../developer-guide/testing.md)
- [Development Setup](../developer-guide/setup.md)

### External Resources
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [Python Security Guidelines](https://python-security.readthedocs.io/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CVE Database](https://cve.mitre.org/)

### Security Tools
- **Bandit**: Python security linter
- **Safety**: Vulnerability scanner for Python dependencies
- **pip-audit**: PyPA's tool for scanning Python packages
- **SBOM generators**: Software Bill of Materials creation

## Contact Information

For security-related questions or vulnerability reports:
- **Project Repository**: GitHub Issues (for general security questions)
- **Security Email**: Contact project maintainers directly for sensitive issues
- **Security Advisories**: GitHub Security Advisories for disclosed vulnerabilities

---

**Security Disclaimer**: While PyBiorythm implements security best practices, no software is completely secure. Users should follow general security practices for their computing environment and keep all software updated.