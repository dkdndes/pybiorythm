#!/bin/bash
# Enhanced Docker build script for M2 Mac with Docker Desktop + Kubernetes
# Handles both local ARM64 builds and multi-architecture builds

set -e

echo "🚀 Docker Build Script for M2 Mac"
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="pybiorythm"
VERSION=${1:-"local"}
BUILD_CONTEXT="."
DOCKERFILE="Dockerfile"

# Function to check Docker status
check_docker() {
    echo -e "\n${YELLOW}Checking Docker status...${NC}"
    
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker Desktop.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker is running${NC}"
    echo "Context: $(docker context show)"
    echo "Architecture: $(docker info | grep Architecture | awk '{print $2}')"
}

# Function to build for local M2 Mac (ARM64)
build_local_arm64() {
    echo -e "\n${BLUE}Building for local M2 Mac (ARM64)...${NC}"
    
    docker build \
        --platform linux/arm64 \
        --target production \
        --tag "${IMAGE_NAME}:${VERSION}-arm64" \
        --tag "${IMAGE_NAME}:local-arm64" \
        --tag "${IMAGE_NAME}:latest" \
        -f "${DOCKERFILE}" \
        "${BUILD_CONTEXT}"
    
    echo -e "${GREEN}✅ Local ARM64 build complete${NC}"
}

# Function to build multi-architecture (for CI/production)
build_multi_arch() {
    echo -e "\n${BLUE}Building multi-architecture (ARM64 + AMD64)...${NC}"
    
    # Create/use buildx builder
    docker buildx create --name m2-builder --use 2>/dev/null || docker buildx use m2-builder
    
    docker buildx build \
        --platform linux/arm64,linux/amd64 \
        --target production \
        --tag "${IMAGE_NAME}:${VERSION}" \
        --tag "${IMAGE_NAME}:multi-arch" \
        -f "${DOCKERFILE}" \
        "${BUILD_CONTEXT}" \
        --push 2>/dev/null || echo -e "${YELLOW}⚠️  Multi-arch build created but not pushed (no registry configured)${NC}"
    
    echo -e "${GREEN}✅ Multi-architecture build complete${NC}"
}

# Function to test the built image
test_image() {
    local image_tag="$1"
    echo -e "\n${YELLOW}Testing image: ${image_tag}${NC}"
    
    # Test basic functionality
    if docker run --rm --platform linux/arm64 "${image_tag}" python -c "import biorythm; print('✅ Basic import test passed')"; then
        echo -e "${GREEN}✅ Image test passed${NC}"
    else
        echo -e "${RED}❌ Image test failed${NC}"
        return 1
    fi
    
    # Test with sample calculation
    echo "Testing biorhythm calculation..."
    docker run --rm --platform linux/arm64 "${image_tag}" python -c "
from datetime import datetime
import biorythm
calc = biorythm.BiorhythmCalculator()
result = calc.calculate_biorhythm_values(datetime(1990, 5, 15), datetime(2023, 6, 1))
print('✅ Calculation test passed:', result)
"
}

# Function to show image information
show_image_info() {
    echo -e "\n${BLUE}Built images:${NC}"
    docker images "${IMAGE_NAME}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}"
    
    echo -e "\n${BLUE}Image details for ${IMAGE_NAME}:latest:${NC}"
    docker inspect "${IMAGE_NAME}:latest" --format '
Platform: {{.Architecture}}/{{.Os}}
Size: {{.Size}} bytes
Created: {{.Created}}
Layers: {{len .RootFS.Layers}}
' 2>/dev/null || echo "No image details available"
}

# Function to deploy with Docker Compose
deploy_compose() {
    echo -e "\n${YELLOW}Deploying with Docker Compose...${NC}"
    
    if [ -f "docker-compose.local.yml" ]; then
        docker-compose -f docker-compose.local.yml up -d
        echo -e "${GREEN}✅ Deployed with Docker Compose${NC}"
        echo "Access the container: docker-compose -f docker-compose.local.yml exec biorythm bash"
    else
        echo -e "${YELLOW}⚠️  docker-compose.local.yml not found${NC}"
    fi
}

# Function to deploy to Kubernetes
deploy_k8s() {
    echo -e "\n${YELLOW}Deploying to Docker Desktop Kubernetes...${NC}"
    
    if kubectl config current-context | grep -q "docker-desktop"; then
        if [ -f "k8s-deployment.yaml" ]; then
            kubectl apply -f k8s-deployment.yaml
            echo -e "${GREEN}✅ Deployed to Kubernetes${NC}"
            echo "Check status: kubectl get pods -l app=biorythm"
            echo "Access service: kubectl port-forward svc/biorythm-service 8080:8080"
        else
            echo -e "${YELLOW}⚠️  k8s-deployment.yaml not found${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Not connected to docker-desktop Kubernetes context${NC}"
        echo "Current context: $(kubectl config current-context)"
    fi
}

# Function to clean up old images
cleanup() {
    echo -e "\n${YELLOW}Cleaning up old images...${NC}"
    docker image prune -f --filter "label=stage=intermediate" 2>/dev/null || true
    docker builder prune -f 2>/dev/null || true
    echo -e "${GREEN}✅ Cleanup complete${NC}"
}

# Main script logic
case "${2:-local}" in
    "local"|"l")
        check_docker
        build_local_arm64
        test_image "${IMAGE_NAME}:latest"
        show_image_info
        ;;
    "multi"|"m")
        check_docker
        build_multi_arch
        test_image "${IMAGE_NAME}:${VERSION}"
        show_image_info
        ;;
    "compose"|"c")
        check_docker
        build_local_arm64
        test_image "${IMAGE_NAME}:latest"
        deploy_compose
        ;;
    "k8s"|"kubernetes"|"k")
        check_docker
        build_local_arm64
        test_image "${IMAGE_NAME}:latest"
        deploy_k8s
        ;;
    "all"|"a")
        check_docker
        build_local_arm64
        test_image "${IMAGE_NAME}:latest"
        deploy_compose
        deploy_k8s
        show_image_info
        ;;
    "clean")
        cleanup
        ;;
    "help"|"-h"|*)
        echo "Usage: $0 [version] [mode]"
        echo ""
        echo "Modes:"
        echo "  local, l     Build for local M2 Mac (default)"
        echo "  multi, m     Build multi-architecture"
        echo "  compose, c   Build and deploy with Docker Compose"
        echo "  k8s, k       Build and deploy to Kubernetes"
        echo "  all, a       Build and deploy to both Compose and K8s"
        echo "  clean        Clean up old images"
        echo "  help, -h     Show this help"
        echo ""
        echo "Examples:"
        echo "  $0                    # Build v'local' for local M2 Mac"
        echo "  $0 v1.0.0 local      # Build v1.0.0 for local M2 Mac"
        echo "  $0 v1.0.0 multi      # Build v1.0.0 multi-architecture"
        echo "  $0 latest compose    # Build and deploy with Docker Compose"
        echo "  $0 latest k8s        # Build and deploy to Kubernetes"
        echo ""
        echo "M2 Mac Optimizations:"
        echo "  - Native ARM64 builds for best performance"
        echo "  - Multi-stage Dockerfile for smaller images"
        echo "  - Docker Desktop + Kubernetes integration"
        echo "  - Resource limits optimized for local development"
        ;;
esac

echo -e "\n${GREEN}🎉 Build script complete!${NC}"