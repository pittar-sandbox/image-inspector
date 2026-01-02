#!/bin/bash
set -e

# Build the container image using Buildah
echo "Building container image..."
buildah bud -f Containerfile -t image-inspector:latest .

echo "Build complete!"
echo "To run the container:"
echo "podman run -d -p 5000:5000 image-inspector:latest"
