# 🚀 Deployment Guide

This guide explains the complete CI/CD pipeline and deployment strategies for the pybiorythm application across development, staging, and production environments.

!!! info "CLI Application Notice"
    **PyBiorythm is a command-line interface (CLI) application**, not a web service. The HTTP server deployment patterns, health endpoints, and load balancer configurations described in this guide are **demonstration examples** showing how to implement such features in production applications.
    
    For actual PyBiorythm deployments, the application runs as:
    - **Batch processing jobs** in Kubernetes CronJobs
    - **One-time containers** for generating biorhythm charts
    - **Development containers** with interactive CLI access

## 📋 Overview

### Environment Strategy
- **Development** (`dev`): Feature branches, experimental builds
- **Staging** (`staging`): Pre-production testing, `develop` branch
- **Production** (`prod`): Live production, `main` branch only

### Deployment Patterns
- **Rolling Updates**: Default for development and staging
- **Blue-Green**: Production deployments with zero downtime
- **Canary**: Available for gradual production rollouts

## 🔄 Automatic Workflows

### 1. Development Docker Build (`dev-docker.yml`)

**Triggers:**
- Push to `develop`, `feature/*`, `bugfix/*`, `hotfix/*` branches
- Pull requests to `develop`
- Manual workflow dispatch

**What it does:**
- Generates semantic version numbers based on branch
- Builds multi-architecture Docker images (AMD64/ARM64)
- Creates environment-specific tags
- Generates Kubernetes manifests
- Performs security scanning
- Creates deployment summaries

**Version Pattern:**
```
feature/auth-system → 1.0.0-dev.feature-auth-system.a1b2c3d4
develop            → 1.0.0-staging.a1b2c3d4
main               → 1.0.0
```

### 2. Blue-Green Deployment (`blue-green-deploy.yml`)

**Triggers:**
- Manual workflow dispatch only

**What it does:**
- Deploys to blue or green slot
- Validates deployment health
- Switches traffic between slots
- Provides rollback capabilities
- Cleans up inactive deployments

## 🏗️ Usage Examples

### Automatic Development Deployment

When you push a feature branch:

```bash
git checkout -b feature/new-calculation
# Make changes
git commit -m "feat: add new calculation method"
git push origin feature/new-calculation
```

**Result:**
- Builds image: `ghcr.io/dkdndes/pybiorythm:1.0.0-dev.feature-new-calculation.a1b2c3d4`
- Creates deployment manifests for `dev` environment
- Available tags: `dev-latest`, `dev-a1b2c3d4`

### Staging Deployment

Push to develop branch:

```bash
git checkout develop
git merge feature/new-calculation
git push origin develop
```

**Result:**
- Builds image: `ghcr.io/dkdndes/pybiorythm:1.0.0-staging.b2c3d4e5`
- Creates deployment manifests for `staging` environment
- Available tags: `staging-latest`, `staging-b2c3d4e5`

### Production Blue-Green Deployment

1. **Deploy to Green Slot** (without switching traffic):
```bash
gh workflow run blue-green-deploy.yml \
  -f environment=prod \
  -f image_tag=1.0.0 \
  -f deployment_slot=green \
  -f switch_traffic=false
```

2. **Test Green Slot**:
```bash
kubectl port-forward service/pybiorythm-prod-green 8080:80
curl http://localhost:8080/health
```

3. **Switch Traffic to Green**:
```bash
gh workflow run blue-green-deploy.yml \
  -f environment=prod \
  -f image_tag=1.0.0 \
  -f deployment_slot=green \
  -f switch_traffic=true
```

## 🎯 Deployment Strategies

### Rolling Updates (Default)
- **Use case**: Development and staging environments
- **Benefits**: Simple, automatic
- **Drawbacks**: Brief service interruption possible

### Blue-Green Deployment
- **Use case**: Production deployments
- **Benefits**: Zero downtime, instant rollback
- **Process**:
  1. Deploy new version to inactive slot (green)
  2. Test green slot thoroughly
  3. Switch traffic from blue to green
  4. Keep blue as rollback option
  5. Clean up old blue deployment

### Canary Deployment (Future)
- **Use case**: Risk-sensitive production changes
- **Process**:
  1. Deploy to small subset of users (5-10%)
  2. Monitor metrics and errors
  3. Gradually increase traffic
  4. Full rollout or rollback based on results

## 🔧 Manual Deployment Commands

### Quick Docker Test
```bash
# Pull and test latest dev image
docker run --rm ghcr.io/dkdndes/pybiorythm:dev-latest python main.py -y 1990 -m 5 -d 15

# Test specific version
docker run --rm ghcr.io/dkdndes/pybiorythm:1.0.0-dev.feature-auth.a1b2c3d4 python main.py --help
```

### Local Development with Docker Compose
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Start staging environment
docker-compose -f docker-compose.staging.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

### Kubernetes Deployment
```bash
# Deploy to development
kubectl apply -f manifests/dev/

# Deploy to staging
kubectl apply -f manifests/staging/

# Blue-green production deployment
kubectl apply -f manifests/blue-green/deployment-green.yaml
kubectl apply -f manifests/blue-green/service-green.yaml

# Switch traffic (blue-green)
kubectl patch service pybiorythm-prod -p '{"spec":{"selector":{"slot":"green"}}}'

# Rollback (switch back to blue)
kubectl patch service pybiorythm-prod -p '{"spec":{"selector":{"slot":"blue"}}}'
```

## 📊 Monitoring and Observability

### Health Checks (Demonstration Examples)
HTTP-based deployments typically include:
- **Readiness Probe**: Checks if container is ready to serve traffic
- **Liveness Probe**: Restarts container if unhealthy  
- **Startup Probe**: Allows slow-starting containers

!!! note "CLI Application Health Checks"
    For PyBiorythm CLI deployments, health verification is done through:
    - **Import Test**: `python -c "import biorythm; print('OK')"`
    - **Calculation Test**: Running actual biorhythm calculations
    - **Dependencies Check**: Verifying all required packages load correctly

### Available Endpoints (Demonstration Only)
```bash
# NOTE: These endpoints are demonstration examples for HTTP-based applications
# PyBiorythm is a CLI application and does not provide HTTP endpoints

# Health check (example for web services)
curl http://app-url/health

# Metrics (example for web services)
curl http://app-url/metrics

# Version info (example for web services)
curl http://app-url/version
```

### Actual CLI Health Verification
```bash
# Verify CLI application health
docker run --rm pybiorythm:latest python -c "import biorythm; print('✅ Health check OK')"

# Test biorhythm calculation
docker run --rm pybiorythm:latest python main.py -y 1990 -m 5 -d 15

# Verify all dependencies
docker run --rm pybiorythm:latest python -c "
import biorythm.core
import datetime
calc = biorythm.core.BiorhythmCalculator()
result = calc.calculate_biorhythm(datetime.datetime(1990, 5, 15), datetime.datetime.now())
print('✅ CLI application healthy')
"
```

### Monitoring Commands
```bash
# Watch deployment progress
kubectl rollout status deployment/pybiorythm-prod-green

# View pod status
kubectl get pods -l app=pybiorythm -o wide

# Check service endpoints
kubectl get endpoints pybiorythm-prod

# View recent logs
kubectl logs -l app=pybiorythm --tail=100 --since=1h

# Monitor resource usage
kubectl top pods -l app=pybiorythm
```

## 🚨 Rollback Procedures

### Immediate Rollback (Blue-Green)
```bash
# Switch back to previous slot
kubectl patch service pybiorythm-prod -p '{"spec":{"selector":{"slot":"blue"}}}'
```

### Rolling Update Rollback
```bash
# Rollback to previous deployment
kubectl rollout undo deployment/pybiorythm-staging

# Rollback to specific revision
kubectl rollout undo deployment/pybiorythm-staging --to-revision=3

# Check rollout history
kubectl rollout history deployment/pybiorythm-staging
```

### Emergency Procedures
```bash
# Scale down problematic deployment
kubectl scale deployment pybiorythm-prod-green --replicas=0

# Emergency rollback with immediate effect
kubectl patch service pybiorythm-prod -p '{"spec":{"selector":{"slot":"blue"}}}'
kubectl scale deployment pybiorythm-prod-blue --replicas=5
```

## 🔒 Security Considerations

### Image Security
- All images are scanned with Trivy
- Vulnerabilities reported to GitHub Security tab
- Base images updated regularly
- Non-root user in containers

### Access Control
- Environment-specific namespaces
- RBAC configured per environment
- Secrets managed through Kubernetes secrets
- Network policies for traffic isolation

### Compliance
- All deployments logged and auditable
- Git history tracks all changes
- Deployment manifests versioned
- Security scans archived for 90 days

## 📈 Performance Tuning

### Resource Allocation

| Environment | CPU Request | Memory Request | CPU Limit | Memory Limit |
|-------------|-------------|----------------|-----------|--------------|
| Development | 50m         | 64Mi           | 200m      | 256Mi        |
| Staging     | 100m        | 128Mi          | 500m      | 512Mi        |
| Production  | 200m        | 256Mi          | 1000m     | 1Gi          |

### Auto-scaling
- **Development**: Disabled (cost optimization)
- **Staging**: 2-5 replicas based on CPU (70% threshold)
- **Production**: 3-10 replicas based on CPU (60% threshold)

## 🔍 Troubleshooting

### Common Issues

1. **Image Pull Errors**
   ```bash
   # Check if image exists
   docker manifest inspect ghcr.io/dkdndes/pybiorythm:tag
   
   # Verify registry credentials
   kubectl get secret regcred -o yaml
   ```

2. **Pod Startup Issues**
   ```bash
   # Check pod events
   kubectl describe pod pod-name
   
   # View container logs
   kubectl logs pod-name -c container-name
   ```

3. **Service Not Accessible**
   ```bash
   # Check service endpoints
   kubectl get endpoints service-name
   
   # Test service connectivity
   kubectl run test-pod --image=busybox -it --rm -- wget -qO- http://service-name/health
   ```

4. **Blue-Green Switch Issues**
   ```bash
   # Check current service selector
   kubectl get service pybiorythm-prod -o yaml | grep -A 5 selector
   
   # Verify both slots are running
   kubectl get pods -l app=pybiorythm -o wide
   ```

## 🎛️ Environment Variables

### Application Configuration
```yaml
env:
  - name: ENVIRONMENT
    value: "dev|staging|prod"
  - name: VERSION
    value: "1.0.0-dev.feature.abc123"
  - name: LOG_LEVEL
    value: "debug|info|warn|error"
  - name: DEPLOYMENT_SLOT
    value: "blue|green"
```

### Infrastructure Configuration
Environment-specific settings are stored in `.github/environments/*.env` files:
- `dev.env`: Development configuration
- `staging.env`: Staging configuration  
- `prod.env`: Production configuration

## 📝 Best Practices

### Branch Strategy
1. Create feature branches from `develop`
2. Test in development environment automatically
3. Merge to `develop` for staging deployment
4. Merge `develop` to `main` for production
5. Use semantic commits for version generation

### Deployment Strategy
1. Always test in lower environments first
2. Use blue-green for production deployments
3. Monitor deployments actively
4. Keep rollback plans ready
5. Document all changes

### Security
1. Never commit secrets to Git
2. Use least privilege access
3. Scan all images for vulnerabilities
4. Keep dependencies updated
5. Monitor security advisories

## Next Steps

- **Docker Deployment**: [Docker Setup Guide](docker.md) for container-specific deployment
- **Kubernetes**: [Kubernetes Guide](kubernetes.md) for cluster deployment
- **Security**: [Security & Compliance](security.md) for security best practices
- **CI/CD Workflows**: [GitHub Actions](../workflows/github-actions.md) for automation details
- **Local Testing**: [Local GitHub Actions](local-github-actions.md) for testing deployments locally
- **Development**: [Architecture Overview](../developer-guide/architecture.md) for understanding the application structure

This deployment guide provides comprehensive coverage of all deployment scenarios and strategies for the pybiorythm application.