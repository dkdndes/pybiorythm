# Multi-stage Dockerfile for Biorythm
# Stage 1: Build stage with dependencies
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install numpy directly (no build tools needed for wheel)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir numpy>=1.20.0

# Copy source code
COPY biorythm.py main.py ./

# Stage 2: Production stage - minimal runtime image
FROM python:3.12-slim AS production

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash biorythm

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only necessary application files
COPY --from=builder /app/biorythm.py .
COPY --from=builder /app/main.py .

# Change ownership to non-root user
RUN chown -R biorythm:biorythm /app
USER biorythm

# Add labels for metadata
LABEL maintainer="Peter Rosemann <dkdndes@gmail.com>"
LABEL description="Biorhythm chart generator (pseudoscience demonstration)"
LABEL version="0.1.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import biorythm; print('OK')" || exit 1

# Default command - interactive mode
CMD ["python", "main.py"]