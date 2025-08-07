# Docker Deployment Guide for M2 Mac

This guide covers Docker deployment on Apple M2 Mac with Docker Desktop and Kubernetes integration.

## 🏗️ Architecture Considerations

### Your Setup
- **Hardware**: Apple M2 Mac (ARM64 architecture)
- **Docker**: Docker Desktop with Kubernetes enabled
- **Context**: `desktop-linux` (Docker Desktop's Linux VM)
- **Native Support**: ARM64 containers run natively for best performance

### Key Differences from Intel Macs
1. **Native ARM64**: Containers built for ARM64 run without emulation
2. **Multi-architecture**: Can build for both ARM64 (local) and AMD64 (production)
3. **Performance**: ARM64 containers are faster than emulated AMD64 containers
4. **Compatibility**: Some images may not have ARM64 variants

## 🚀 Quick Start

### 1. Build for Local Development (ARM64)
```bash
# Fast local build
./docker-build-m2.sh

# Or manually
docker build --platform linux/arm64 -t pybiorythm:local .
```

### 2. Build Multi-Architecture (Production)
```bash
# For deployment to various architectures
./docker-build-m2.sh v1.0.0 multi
```

### 3. Deploy with Docker Compose
```bash
# Build and deploy locally
./docker-build-m2.sh latest compose

# Or manually
docker-compose -f docker-compose.local.yml up -d
```

### 4. Deploy to Kubernetes
```bash
# Build and deploy to Docker Desktop K8s
./docker-build-m2.sh latest k8s

# Or manually
kubectl apply -f k8s-deployment.yaml
```

## 📋 Available Commands

### Docker Build Script (`docker-build-m2.sh`)

| Command | Description | Use Case |
|---------|-------------|----------|
| `./docker-build-m2.sh` | Build for local M2 Mac | Development |
| `./docker-build-m2.sh v1.0.0 multi` | Multi-architecture build | CI/CD |
| `./docker-build-m2.sh latest compose` | Build + Docker Compose | Local testing |
| `./docker-build-m2.sh latest k8s` | Build + Kubernetes | Local K8s testing |
| `./docker-build-m2.sh latest all` | Build + Deploy everywhere | Full local setup |
| `./docker-build-m2.sh clean` | Clean old images | Maintenance |

### Docker Compose Commands
```bash
# Start services
docker-compose -f docker-compose.local.yml up -d

# View logs
docker-compose -f docker-compose.local.yml logs -f

# Access container
docker-compose -f docker-compose.local.yml exec biorythm bash

# Stop services
docker-compose -f docker-compose.local.yml down

# Start with development tools
docker-compose -f docker-compose.local.yml --profile dev up -d
```

### Kubernetes Commands
```bash
# Deploy application
kubectl apply -f k8s-deployment.yaml

# Check status
kubectl get pods -l app=biorythm
kubectl get services

# Access application
kubectl port-forward svc/biorythm-service 8080:8080

# View logs
kubectl logs -l app=biorythm -f

# Delete deployment
kubectl delete -f k8s-deployment.yaml
```

## 🔧 Configuration Files

### `docker-compose.local.yml`
- **Purpose**: Local development with Docker Compose
- **Features**: 
  - Native ARM64 build
  - Volume mounts for development
  - Resource limits optimized for M2 Mac
  - Health checks
  - Development tools container (optional)

### `k8s-deployment.yaml`
- **Purpose**: Local Kubernetes deployment
- **Features**:
  - Deployment with ARM64 node affinity
  - Service with LoadBalancer (Docker Desktop)
  - ConfigMap for configuration
  - Resource requests/limits
  - Liveness/readiness probes

### `.actrc` (Updated for M2)
- **Docker Socket**: Uses Docker Desktop's socket
- **Architecture**: linux/amd64 for GitHub Actions compatibility
- **Performance**: Optimized for M2 Mac

## 🏃‍♂️ Performance Optimizations

### For M2 Mac
1. **Native ARM64 Builds**: Best performance, no emulation
2. **Multi-stage Dockerfile**: Smaller final images
3. **Layer Caching**: Optimized layer ordering
4. **Resource Limits**: Tuned for local development

### Build Performance
```bash
# Use BuildKit for faster builds
export DOCKER_BUILDKIT=1

# Enable build cache
docker buildx create --use

# Parallel builds
docker buildx build --platform linux/arm64,linux/amd64
```

## 🔍 Troubleshooting

### Common Issues

#### 1. "No such image" Error with act
```bash
# Pull the required image
docker pull catthehacker/ubuntu:act-latest
```

#### 2. Platform Mismatch Warnings
```bash
# Specify platform explicitly
docker run --platform linux/arm64 pybiorythm:local
```

#### 3. Kubernetes Context Issues
```bash
# Switch to Docker Desktop context
kubectl config use-context docker-desktop

# Verify context
kubectl config current-context
```

#### 4. Resource Constraints
```bash
# Check Docker Desktop resource limits
docker system df
docker system prune -f
```

### Performance Issues
1. **Increase Docker Desktop memory**: Settings > Resources > Memory > 8GB+
2. **Enable Docker Desktop experimental features**: Settings > Experimental
3. **Use ARM64 images**: Avoid AMD64 images when ARM64 alternatives exist

## 🔐 Security Considerations

### Container Security
- **Non-root user**: Containers run as `biorythm` user
- **Minimal base**: Uses `python:3.12-slim`
- **Health checks**: Built-in health monitoring
- **Resource limits**: Prevents resource exhaustion

### Kubernetes Security
- **Node affinity**: Ensures ARM64 node placement
- **Resource constraints**: CPU/memory limits
- **Service isolation**: LoadBalancer type for controlled access

## 🚢 Deployment Strategies

### Development Workflow
1. **Local testing**: `./docker-build-m2.sh latest local`
2. **Integration testing**: `./docker-build-m2.sh latest compose`
3. **K8s testing**: `./docker-build-m2.sh latest k8s`
4. **Multi-arch build**: `./docker-build-m2.sh v1.0.0 multi`

### Production Deployment
1. **GitHub Actions**: Builds multi-architecture images
2. **Container Registry**: Push to ghcr.io
3. **Kubernetes**: Deploy to production cluster
4. **Monitoring**: Health checks and metrics

## 📊 Monitoring

### Docker Desktop Dashboard
- Container resource usage
- Build history
- Volume management
- Network inspection

### Kubernetes Dashboard
```bash
# Access K8s dashboard (if enabled)
kubectl proxy
# Open: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

### Commands for Monitoring
```bash
# Docker stats
docker stats

# K8s resource usage
kubectl top pods
kubectl top nodes

# Application logs
kubectl logs -l app=biorythm --tail=100 -f
```

## 🎯 Best Practices

### For M2 Mac Development
1. **Use native ARM64 builds** for best performance
2. **Test multi-architecture builds** before production
3. **Leverage Docker Desktop's K8s** for local testing
4. **Monitor resource usage** to optimize limits
5. **Use build cache** to speed up iterations

### Container Best Practices
1. **Multi-stage builds** for smaller images
2. **Non-root users** for security
3. **Health checks** for reliability
4. **Resource limits** for stability
5. **Proper labels** for metadata

This setup provides optimal Docker experience on M2 Mac with seamless local development and production deployment capabilities.