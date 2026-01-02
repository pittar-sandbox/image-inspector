# Stage 1: Builder
FROM registry.access.redhat.com/ubi9/ubi:latest AS builder

# Install Python 3.12 and build dependencies
RUN dnf install -y python3.12 python3.12-pip python3.12-devel && \
    dnf clean all

# Create a virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3.12 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Image
FROM registry.access.redhat.com/ubi9/ubi-minimal:latest

# Install runtime dependencies
# shadow-utils is needed for user creation (useradd) if not present, but ubi-minimal might not have it.
# We can use microdnf.
RUN microdnf install -y python3.12 skopeo shadow-utils && \
    microdnf clean all

# Create a non-root user
RUN useradd -m -s /bin/bash appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set environment variables
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP=app.py

# Set working directory
WORKDIR /app

# Copy application code
COPY app.py .
COPY templates/ templates/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
