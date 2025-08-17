# Multi-stage Dockerfile for Biorythm (M2 Mac optimized)
# Stage 1: Build stage with dependencies
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Accept version as build argument from CI environment
ARG VERSION="0.1.0-dev"
ENV SETUPTOOLS_SCM_PRETEND_VERSION=${VERSION}

# Copy package files first for better caching
COPY pyproject.toml uv.lock* LICENSE README.md ./

# Install uv for faster dependency management
RUN pip install --no-cache-dir uv

# Copy source code needed for installation
COPY biorythm/ ./biorythm/
COPY main.py ./

# Install dependencies and package using uv
RUN uv sync --frozen
RUN uv pip install --system .

# Stage 2: Production stage - minimal runtime image
FROM python:3.12-slim AS production

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash biorythm

# Set working directory
WORKDIR /app

# Copy Python packages and dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy application files
COPY --from=builder /app/biorythm ./biorythm/
COPY --from=builder /app/main.py ./

# Change ownership to non-root user
RUN chown -R biorythm:biorythm /app
USER biorythm

# Add labels for metadata (updated)
LABEL maintainer="Peter Rosemann <dkdndes@gmail.com>"
LABEL description="Biorhythm chart generator (pseudoscience demonstration)"
LABEL org.opencontainers.image.source="https://github.com/dkdndes/pybiorythm"
LABEL org.opencontainers.image.documentation="https://github.com/dkdndes/pybiorythm"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import biorythm; print('✅ Health check OK')" || exit 1

# Default command - interactive mode
CMD ["python", "main.py"]