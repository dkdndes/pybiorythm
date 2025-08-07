# Software Bill of Materials (SBOM)

This document describes the SBOM (Software Bill of Materials) generation and management for the pybiorythm project.

## Overview

The project generates comprehensive SBOMs using industry-standard formats to provide transparency into all software components and dependencies, supporting supply chain security and vulnerability management.

## SBOM Formats

### CycloneDX
- **Primary format** used for all SBOM generation
- **Version**: 1.4 specification
- **Features**: Rich metadata, vulnerability correlation, licensing information
- **Tools**: cyclonedx-python-lib, Syft

### SPDX
- **Secondary format** for Docker containers
- **Version**: 2.3 specification  
- **Features**: License compliance, legal analysis
- **Tools**: Syft

## SBOM Types Generated

### 1. Python Application SBOM
**File**: `sbom-python-complete.json`
**Content**: 
- All Python dependencies from pip/uv
- Package metadata and versions
- License information
- Vulnerability identifiers

**Generation Method**:
```bash
cyclonedx-py requirements --format json --output-file sbom-python.json
```

**Components Tracked**:
- Production dependencies (numpy, etc.)
- Development dependencies (pytest, ruff, etc.)
- Transitive dependencies
- Python runtime environment

### 2. Docker Container SBOM
**File**: `sbom-docker-complete.json`
**Content**:
- Container base image components
- System packages and libraries
- Python packages within container
- File system artifacts

**Generation Method**:
```bash
syft pybiorythm:latest --output cyclonedx-json=sbom-docker.json
```

**Components Tracked**:
- Debian/Ubuntu packages from base image
- Python packages and their files
- System libraries and binaries
- Configuration files

### 3. Combined SBOM
**File**: `sbom-combined.json`
**Content**:
- Unified view of all components
- Deduplicated component list
- Complete supply chain picture
- Build environment metadata

**Features**:
- Combines Python and Docker SBOMs
- Eliminates duplicate components
- Adds build and environment context
- Includes attestation metadata

## SBOM Metadata

Each SBOM includes comprehensive metadata:

### Component Information
```json
{
  "component": {
    "type": "application",
    "name": "pybiorythm",
    "version": "0.1.0",
    "description": "Python library for biorhythm calculations",
    "licenses": [{"license": {"id": "MIT"}}],
    "supplier": {
      "name": "dkdndes",
      "url": ["https://github.com/dkdndes/pybiorythm"]
    }
  }
}
```

### Build Environment
```json
{
  "properties": [
    {"name": "github:repository", "value": "dkdndes/pybiorythm"},
    {"name": "github:sha", "value": "abc123..."},
    {"name": "github:workflow", "value": "SBOM Generation"},
    {"name": "build:timestamp", "value": "2023-12-01T10:30:00Z"}
  ]
}
```

## Automation Workflows

### CI/CD Integration
- **Quick SBOM**: Generated on every PR/push for validation
- **Full SBOM**: Generated weekly and on releases
- **Container SBOM**: Generated with every Docker build

### Release Process
1. **Build** - Generate SBOMs for Python and Docker
2. **Combine** - Merge into unified SBOM
3. **Attest** - Create cryptographic attestation
4. **Publish** - Attach to GitHub releases
5. **Validate** - Verify SBOM integrity

### Scheduled Generation
- **Weekly**: Complete SBOM regeneration
- **On dependency updates**: Automatic SBOM refresh
- **On security alerts**: Emergency SBOM analysis

## Vulnerability Management

### SBOM-Based Scanning
SBOMs enable automated vulnerability scanning:

```bash
# Example vulnerability scanning with generated SBOM
grype sbom:sbom-combined.json --output json
```

### Vulnerability Correlation
- Each component includes CPE (Common Platform Enumeration)
- PURL (Package URL) identifiers for package tracking
- CVE correlation through vulnerability databases
- CVSS scoring integration

### Alert Integration
- GitHub Security Advisories
- Dependabot vulnerability alerts  
- Third-party security scanners
- Supply chain attack detection

## Supply Chain Security

### Component Provenance
- Source repository tracking
- Build environment documentation
- Dependency resolution chain
- Package integrity verification

### License Compliance
- Complete license inventory
- License conflict detection
- Compliance reporting
- Legal risk assessment

### Attestation Support
- Cryptographic SBOM signing (future)
- Build provenance attestation
- Supply chain verification
- Tamper detection

## Usage Examples

### Viewing SBOM Contents
```bash
# Download SBOM from release
wget https://github.com/dkdndes/pybiorythm/releases/latest/download/sbom-combined.json

# Extract component list
jq '.components[] | {name: .name, version: .version, licenses: .licenses}' sbom-combined.json
```

### Vulnerability Analysis
```bash
# Scan SBOM for vulnerabilities
docker run --rm -v $(pwd):/tmp anchore/grype sbom:/tmp/sbom-combined.json

# License analysis
docker run --rm -v $(pwd):/tmp licensefinder/license_finder --decisions-file=/tmp/sbom-combined.json
```

### Supply Chain Analysis
```bash
# Component dependency graph
jq '.dependencies' sbom-combined.json

# Risk assessment
jq '.components[] | select(.scope == "required") | {name: .name, licenses: .licenses}' sbom-combined.json
```

## Security Benefits

### Threat Detection
- **Supply chain attacks**: Component tampering detection
- **Vulnerability tracking**: Automated CVE correlation
- **License violations**: Legal compliance monitoring
- **Dependency confusion**: Package verification

### Incident Response
- **Component inventory**: Complete asset visibility
- **Impact analysis**: Vulnerability scope assessment
- **Remediation planning**: Dependency upgrade paths
- **Compliance reporting**: Audit trail maintenance

### Risk Management
- **Third-party risk**: Vendor component tracking
- **Technical debt**: Dependency age analysis
- **Maintenance burden**: Update frequency tracking
- **Security posture**: Vulnerability exposure metrics

## Best Practices

### SBOM Management
- ✅ **Regular generation**: Weekly automated updates
- ✅ **Version control**: Track SBOM changes over time
- ✅ **Validation**: Verify SBOM completeness and accuracy
- ✅ **Distribution**: Share SBOMs with stakeholders

### Security Integration
- ✅ **Continuous monitoring**: Automated vulnerability scanning
- ✅ **Alert management**: Timely security notifications
- ✅ **Response procedures**: Defined incident workflows
- ✅ **Compliance tracking**: Regulatory requirement adherence

### Tooling Integration
- ✅ **CI/CD pipelines**: Automated SBOM generation
- ✅ **Security scanners**: SBOM-based vulnerability detection
- ✅ **Dependency managers**: SBOM-aware package management
- ✅ **Monitoring systems**: SBOM-driven risk assessment

## Files and Artifacts

### Generated Files
```
SBOMs/
├── sbom-python-complete.json    # Python dependencies
├── sbom-docker-complete.json    # Container components  
├── sbom-combined.json           # Unified SBOM
├── sbom-attestation.json        # Cryptographic attestation
├── sbom-docker-spdx.json        # SPDX format (containers)
└── SBOM_SUMMARY.md              # Human-readable summary
```

### Retention Policy
- **CI SBOMs**: 7 days (validation only)
- **Release SBOMs**: 365 days (audit requirements)
- **Combined SBOMs**: Permanent (supply chain records)
- **Attestations**: Permanent (security verification)

## Compliance and Standards

### Industry Standards
- **NIST SP 800-218**: Secure Software Development Framework
- **Executive Order 14028**: Improving Cybersecurity
- **ISO/IEC 5230**: Software Supply Chain Security
- **CISA Guidelines**: Software Bill of Materials

### Regulatory Requirements
- **Supply chain transparency**: Component visibility
- **Vulnerability disclosure**: Timely security updates
- **License compliance**: Legal obligation fulfillment
- **Audit trail**: Change documentation

This SBOM implementation provides comprehensive supply chain visibility and security for the pybiorythm project, enabling proactive vulnerability management and compliance with modern software security standards.