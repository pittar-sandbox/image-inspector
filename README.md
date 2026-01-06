# OCI Image Inspector

Image Inspector is a simple Flask-based web application that utilizes `skopeo` to inspect remote container images without pulling them. It provides a user-friendly interface to view image metadata, including details about layers, environment variables, labels, and more.

This is a test to see if the PR task works.

And another test!

## Features

- **Remote Inspection**: Inspect container images from various registries (Docker Hub, Quay.io, etc.) without downloading the full image.
- **Platform Specifics**: Option to specify OS and Architecture for multi-arch images.
- **Detailed Summary**: Displays key image details such as size, layers, OS, and architecture.
- **JSON Output**: Returns the raw JSON output from `skopeo inspect` for easy programmatic consumption or detailed analysis.
- **Web Interface**: Clean and simple web UI for entering image details.

## Prerequisites

- **Container Runtime**: Podman or Docker
- **Build Tool**: Buildah (optional, for using the provided build script)

## Building the Container

You can build the container image using `buildah` or standard Docker/Podman commands.

### Using Buildah
```bash
buildah bud -t image-inspector:latest -f Containerfile .
```

### Using Podman
```bash
podman build -t image-inspector:latest -f Containerfile .
```

### Using Docker
```bash
docker build -t image-inspector:latest -f Containerfile .
```

## Running the Application

Once built, you can run the container exposing port 5000:

```bash
podman run -d -p 5000:5000 image-inspector:latest
```
*Note: Replace `podman` with `docker` if you are using Docker.*

The application will be accessible at `http://localhost:5000`.

## Usage

1. Open your browser and navigate to `http://localhost:5000`.
2. Enter the **Image URL** (e.g., `quay.io/pittar/petclinic:latest` or `alpine:latest`).
3. (Optional) Specify the **OS** (e.g., `linux`).
4. (Optional) Specify the **Architecture** (e.g., `amd64`, `arm64`).
5. Click **Inspect**.
6. The application will display a summary of the image metadata. You can also view the raw JSON output by clicking "Show Raw JSON Data".

## Local Development

To run the application locally without a container, you need Python 3.12 and `skopeo` installed on your system.

1. **Install Prerequisites**:
   - Python 3.12
   - `skopeo`
     - **Linux (RHEL/Fedora/CentOS)**: `dnf install skopeo`
     - **Linux (Debian/Ubuntu)**: `apt-get install skopeo`
     - **macOS (Homebrew)**: `brew install skopeo`

2. **Set up Virtual Environment**:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the App**:
   ```bash
   python -m flask run --host=0.0.0.0 --port=5000
   ```

## Running Tests

This project uses `pytest` for testing.

1. Ensure your virtual environment is activated and dependencies are installed (see above).
2. Run the tests:
   ```bash
   pytest
   ```
3. To run tests with coverage:
   ```bash
   pytest --cov=app
   ```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
