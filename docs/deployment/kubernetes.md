# Kubernetes Deployment Guide

This guide covers deploying PyBiorythm applications to Kubernetes clusters, including local development with Docker Desktop and production deployments.

!!! info "CLI Application Deployment"
    **PyBiorythm is a CLI application** that generates biorhythm charts and data. The Kubernetes deployments shown here demonstrate **enterprise deployment patterns** but are adapted for CLI usage:
    
    - **Job/CronJob patterns** for scheduled chart generation
    - **Interactive pods** for development and testing
    - **Batch processing** for bulk chart generation
    
    The HTTP server configurations are **demonstration examples** of production deployment patterns.

## Overview

PyBiorythm supports containerized deployment through Docker and orchestration with Kubernetes. This enables:

- **Scalable deployments** for high-traffic applications
- **Resource management** with CPU/memory limits
- **Health monitoring** with liveness and readiness probes
- **Configuration management** through ConfigMaps and Secrets
- **Multi-architecture support** (AMD64, ARM64)

## Prerequisites

### Local Development
- Docker Desktop with Kubernetes enabled
- kubectl CLI tool
- PyBiorythm Docker image built locally

### Production Deployment
- Access to Kubernetes cluster (EKS, GKE, AKS, etc.)
- kubectl configured for your cluster
- Container registry access (Docker Hub, ECR, etc.)
- Appropriate cluster permissions

## Basic Deployment Configuration

### Standard Deployment Manifest

The project includes a comprehensive Kubernetes deployment manifest at `k8s-deployment.yaml`:

```yaml
# Kubernetes deployment for biorythm on Docker Desktop
# Optimized for M2 Mac with Docker Desktop Kubernetes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: biorythm
  labels:
    app: biorythm
    version: local
spec:
  replicas: 1
  selector:
    matchLabels:
      app: biorythm
  template:
    metadata:
      labels:
        app: biorythm
    spec:
      containers:
      - name: biorythm
        image: pybiorythm:local-arm64
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8080
        env:
        - name: PYTHONUNBUFFERED
          value: "1"
        - name: PYTHON_ENV
          value: "development"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        # Health checks for CLI application
        livenessProbe:
          exec:
            command:
            - python
            - -c
            - "import biorythm; print('✅ Liveness OK')"
          initialDelaySeconds: 30
          periodSeconds: 30
        readinessProbe:
          exec:
            command:
            - python
            - -c
            - "import biorythm.core; calc = biorythm.core.BiorhythmCalculator(); print('✅ Ready')"
          initialDelaySeconds: 5
          periodSeconds: 10
      # Node affinity for ARM64 (M2 Mac)
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: kubernetes.io/arch
                operator: In
                values: ["arm64"]
---
apiVersion: v1
kind: Service
metadata:
  name: biorythm-service
spec:
  selector:
    app: biorythm
  ports:
  - port: 8080
    targetPort: 8080
    protocol: TCP
  type: LoadBalancer  # Uses Docker Desktop's load balancer
---
# Optional: ConfigMap for configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: biorythm-config
data:
  python_env: "development"
  log_level: "INFO"
```

## CLI-Specific Deployment Patterns

### Kubernetes Jobs for Batch Processing

```yaml
# job-biorhythm-generation.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: biorhythm-batch-job
spec:
  template:
    spec:
      containers:
      - name: biorhythm
        image: pybiorythm:latest
        command: ["python", "main.py"]
        args: ["-y", "1990", "-m", "5", "-d", "15", "--orientation", "json-vertical"]
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
      restartPolicy: Never
  backoffLimit: 4
```

### CronJobs for Scheduled Chart Generation

```yaml
# cronjob-daily-biorhythm.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-biorhythm-report
spec:
  schedule: "0 6 * * *"  # Daily at 6 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: biorhythm
            image: pybiorythm:latest
            command: ["python", "main.py"]
            args: ["-y", "1990", "-m", "5", "-d", "15"]
            env:
            - name: OUTPUT_FORMAT
              value: "json-vertical"
          restartPolicy: OnFailure
```

### Interactive Development Pod

```yaml
# interactive-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: biorhythm-dev
spec:
  containers:
  - name: biorhythm
    image: pybiorythm:latest
    command: ["/bin/bash"]
    stdin: true
    tty: true
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
  restartPolicy: Never
```

## Deployment Steps

### Local Development Deployment

1. **Build the Docker image:**
   ```bash
   # For ARM64 (M2 Mac)
   docker build -t pybiorythm:local-arm64 .
   
   # For AMD64 (Intel)
   docker build -t pybiorythm:local-amd64 .
   ```

2. **Deploy to local Kubernetes:**
   ```bash
   # Apply the deployment
   kubectl apply -f k8s-deployment.yaml
   
   # Check deployment status
   kubectl get deployments
   kubectl get pods
   kubectl get services
   ```

3. **Access the application:**
   ```bash
   # Get service details
   kubectl get svc biorythm-service
   
   # Port forward for local access
   kubectl port-forward svc/biorythm-service 8080:8080
   ```

4. **Monitor the deployment:**
   ```bash
   # View logs
   kubectl logs -l app=biorythm -f
   
   # Describe resources
   kubectl describe deployment biorythm
   kubectl describe pod <pod-name>
   ```

### Production Deployment

1. **Push image to container registry:**
   ```bash
   # Tag for your registry
   docker tag pybiorythm:local-amd64 your-registry/pybiorythm:v1.0.0
   
   # Push to registry
   docker push your-registry/pybiorythm:v1.0.0
   ```

2. **Create production manifest:**
   ```yaml
   # production-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: pybiorythm-prod
     namespace: production
     labels:
       app: pybiorythm
       version: v1.0.0
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: pybiorythm
     template:
       metadata:
         labels:
           app: pybiorythm
       spec:
         containers:
         - name: pybiorythm
           image: your-registry/pybiorythm:v1.0.0
           imagePullPolicy: Always
           ports:
           - containerPort: 8080
           env:
           - name: PYTHONUNBUFFERED
             value: "1"
           - name: PYTHON_ENV
             value: "production"
           - name: LOG_LEVEL
             valueFrom:
               configMapKeyRef:
                 name: pybiorythm-config
                 key: log_level
           resources:
             requests:
               memory: "512Mi"
               cpu: "500m"
             limits:
               memory: "1Gi"
               cpu: "1000m"
           # Production health checks for CLI application
           livenessProbe:
             exec:
               command:
               - python
               - -c
               - "import biorythm; print('✅ Production Liveness OK')"
             initialDelaySeconds: 30
             periodSeconds: 10
           readinessProbe:
             exec:
               command:
               - python
               - main.py
               - --help
             initialDelaySeconds: 5
             periodSeconds: 5
   ```

3. **Deploy to production:**
   ```bash
   kubectl apply -f production-deployment.yaml -n production
   ```

## Configuration Management

### ConfigMaps

Create ConfigMaps for application configuration:

```yaml
# config/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: pybiorythm-config
  namespace: production
data:
  # Application settings
  log_level: "INFO"
  chart_width: "80"
  default_days: "30"
  
  # Feature flags
  enable_json_output: "true"
  enable_horizontal_charts: "true"
  
  # Performance settings
  max_days_calculation: "365"
  cache_calculations: "false"
  
  # Scientific disclaimer settings
  display_warnings: "true"
  warning_level: "comprehensive"
```

Apply the ConfigMap:
```bash
kubectl apply -f config/configmap.yaml
```

### Secrets

For sensitive configuration (if needed):

```yaml
# config/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: pybiorythm-secrets
  namespace: production
type: Opaque
data:
  # Base64 encoded values
  api_key: <base64-encoded-api-key>
  database_url: <base64-encoded-db-url>
```

Apply secrets:
```bash
kubectl apply -f config/secrets.yaml
```

### Environment-Specific Configurations

```yaml
# Development environment
apiVersion: v1
kind: ConfigMap
metadata:
  name: pybiorythm-config-dev
data:
  log_level: "DEBUG"
  python_env: "development"
  enable_debug_output: "true"
---
# Production environment
apiVersion: v1
kind: ConfigMap
metadata:
  name: pybiorythm-config-prod
data:
  log_level: "WARNING"
  python_env: "production"
  enable_debug_output: "false"
```

## Advanced Configurations

### Horizontal Pod Autoscaler (HPA)

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: pybiorythm-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pybiorythm-prod
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Pod Disruption Budget

```yaml
# pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: pybiorythm-pdb
  namespace: production
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: pybiorythm
```

### Network Policies

```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: pybiorythm-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: pybiorythm
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - {} # Allow all egress (modify as needed)
```

## Service Configurations

### ClusterIP Service (Internal)

```yaml
# service-internal.yaml
apiVersion: v1
kind: Service
metadata:
  name: pybiorythm-internal
  namespace: production
spec:
  selector:
    app: pybiorythm
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
  type: ClusterIP
```

### LoadBalancer Service (External)

```yaml
# service-external.yaml
apiVersion: v1
kind: Service
metadata:
  name: pybiorythm-external
  namespace: production
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  selector:
    app: pybiorythm
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
  type: LoadBalancer
```

### Ingress Configuration

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: pybiorythm-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - api.pybiorythm.example.com
    secretName: pybiorythm-tls
  rules:
  - host: api.pybiorythm.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: pybiorythm-internal
            port:
              number: 80
```

## Multi-Architecture Support

### Building Multi-Arch Images

```bash
# Create buildx builder
docker buildx create --name multiarch --use

# Build multi-architecture image
docker buildx build --platform linux/amd64,linux/arm64 \
  -t your-registry/pybiorythm:v1.0.0 --push .
```

### Architecture-Specific Deployments

```yaml
# deployment-amd64.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pybiorythm-amd64
spec:
  template:
    spec:
      nodeSelector:
        kubernetes.io/arch: amd64
      containers:
      - name: pybiorythm
        image: your-registry/pybiorythm:v1.0.0-amd64
---
# deployment-arm64.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pybiorythm-arm64
spec:
  template:
    spec:
      nodeSelector:
        kubernetes.io/arch: arm64
      containers:
      - name: pybiorythm
        image: your-registry/pybiorythm:v1.0.0-arm64
```

## Monitoring and Observability

### Health Check Endpoints (Demonstration)

**HTTP Health Checks (Example for Web Applications):**

```yaml
# NOTE: These are demonstration examples for HTTP-based applications
# PyBiorythm is a CLI application and uses exec probes instead

livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 2
```

**Actual CLI Health Checks:**

```yaml
# For PyBiorythm CLI application
livenessProbe:
  exec:
    command:
    - python
    - -c
    - "import biorythm; print('✅ Healthy')"
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  exec:
    command:
    - python
    - -c
    - "import biorythm.core; calc = biorythm.core.BiorhythmCalculator(); print('✅ Ready')"
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 2
```

### Prometheus Monitoring

```yaml
# service-monitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: pybiorythm-monitor
  namespace: production
spec:
  selector:
    matchLabels:
      app: pybiorythm
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### Log Aggregation

```yaml
# Fluent Bit configuration for log collection
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
data:
  fluent-bit.conf: |
    [INPUT]
        Name              tail
        Path              /var/log/containers/pybiorythm*.log
        Parser            docker
        Tag               kube.*
        Refresh_Interval  5
        
    [OUTPUT]
        Name  es
        Match kube.*
        Host  elasticsearch.logging.svc.cluster.local
        Port  9200
        Index pybiorythm-logs
```

## Deployment Strategies

### Rolling Updates

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

### Blue-Green Deployments

See [Blue-Green Deployment Workflow](../workflows/blue-green.md) for detailed implementation.

### Canary Deployments

```yaml
# canary-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pybiorythm-canary
  labels:
    version: canary
spec:
  replicas: 1  # Small number for canary
  selector:
    matchLabels:
      app: pybiorythm
      version: canary
```

## Troubleshooting

### Common Issues

1. **Image Pull Errors:**
   ```bash
   # Check image exists
   docker pull your-registry/pybiorythm:v1.0.0
   
   # Verify image pull secrets
   kubectl get secrets
   kubectl describe secret regcred
   ```

2. **Pod Startup Failures:**
   ```bash
   # Check pod logs
   kubectl logs <pod-name> --previous
   
   # Describe pod for events
   kubectl describe pod <pod-name>
   ```

3. **Service Connection Issues:**
   ```bash
   # Test service connectivity
   kubectl exec -it <pod-name> -- curl http://pybiorythm-service:8080
   
   # Check endpoints
   kubectl get endpoints pybiorythm-service
   ```

4. **Resource Constraints:**
   ```bash
   # Check resource usage
   kubectl top nodes
   kubectl top pods
   
   # Describe node capacity
   kubectl describe node <node-name>
   ```

### Debugging Commands

```bash
# Get all resources
kubectl get all -l app=pybiorythm

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Port forward for debugging
kubectl port-forward deployment/pybiorythm 8080:8080

# Execute commands in pod
kubectl exec -it <pod-name> -- python -c "import biorythm; print('OK')"

# View detailed resource info
kubectl describe deployment pybiorythm
kubectl describe service pybiorythm-service
kubectl describe configmap pybiorythm-config
```

## Security Best Practices

### Pod Security Standards

```yaml
# security-context.yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
      containers:
      - name: pybiorythm
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
```

### Resource Limits

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
    ephemeral-storage: "1Gi"
  limits:
    memory: "512Mi"
    cpu: "500m"
    ephemeral-storage: "2Gi"
```

### Network Security

```yaml
# Restrict network access
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: pybiorythm-deny-all
spec:
  podSelector:
    matchLabels:
      app: pybiorythm
  policyTypes:
  - Ingress
  - Egress
  # No ingress/egress rules = deny all
```

## Performance Optimization

### Resource Tuning

```yaml
# Performance-optimized configuration
resources:
  requests:
    memory: "1Gi"
    cpu: "1000m"
  limits:
    memory: "2Gi"
    cpu: "2000m"

# JVM-style settings for Python
env:
- name: PYTHONUNBUFFERED
  value: "1"
- name: PYTHONOPTIMIZE
  value: "1"  # Enable optimizations
```

### Scaling Configuration

```yaml
# Aggressive scaling for high load
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
```

---

**Next**: [Blue-Green Deployment](../workflows/blue-green.md) | [Docker Guide](docker.md) | [Security](security.md)