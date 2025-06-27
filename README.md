# Fakely Live

A real-time face swapping application that allows users to replace faces in video streams with selected face masks using deep learning technology.

## Project Overview

Fakely Live is a web-based application that enables real-time face swapping in video streams. The system uses deep learning models to detect faces in video frames and replace them with selected face masks. The application provides a user-friendly interface for selecting face masks and recording videos with the face swapping effect applied.

### Key Features

- Real-time face swapping in video streams
- Selection from a library of face masks
- Video recording with face swapping applied
- Web-based user interface
- GPU-accelerated processing for optimal performance

### Architecture

The project consists of several components:

- **UI**: React-based web interface for user interaction (vertical layout 1080x1850)
- **API**: FastAPI backend that handles WebRTC connections and mask selection
- **Frames Handler**: Processes video frames and applies face swapping
- **RabbitMQ**: Message broker for frame data exchange between components
- **Redis**: In-memory database for caching and temporary storage

## Requirements

- Docker and Docker Compose
- NVIDIA GPU with CUDA support
- Modern web browser with WebRTC support

## Quick start

1. Create an `.env` file with the required environment variables:
   ```
   # Common
   REDIS_HOST=redis
   RABBITMQ_HOST=rabbitmq
   RABBITMQ_USER=guest
   RABBITMQ_PASS=guest

   # Handler
   WORKER_COUNT=5
   DET_SIZE_W=640
   DET_SIZE_H=640
   DET_THRESH=0.5

   # Api
   ENABLE_HANDLE_STREAM=1
   ```

2. Create a `models/` directory at the root of the project and download the face swapping model:
   ```bash
   mkdir -p models
   wget -O models/inswapper_128.onnx https://huggingface.co/deepinsight/inswapper/resolve/main/inswapper_128.onnx
   ```

3. Start the containers using Docker Hub images:
   ```bash
   docker compose up -d
   ```

## Usage

1. Open your web browser and navigate to `http://localhost` (or `https://localhost` if SSL is configured).

2. Grant camera access permissions when prompted.

3. Accept the terms and conditions in the consent panel.

4. Select a face mask from the available options in the sidebar.

5. The face swapping will be applied in real-time to your video stream.

6. Use the recording controls to capture videos with the face swapping effect:
   - Click the record button to start recording
   - A countdown will appear before recording begins
   - Recording will automatically stop after the configured time limit
   - The recorded video can be downloaded to your device

## Face Masks

The application uses face mask images to replace faces in the video stream. You can add your own face masks to the system:

1. Create a `faces/` directory at the root of the project if it doesn't exist:
   ```bash
   mkdir -p faces
   ```

2. Place your face mask images in the `faces/` directory.
3. Supported image formats include JPG, JPEG, PNG, and JFIF.
4. For best results, use high-quality frontal face images with good lighting and clear facial features.
5. The face mask images are automatically mounted to the container via a volume, so any changes to the `faces/` directory on your host machine will be immediately available in the application without needing to restart the container.
6. The new face masks will appear in the selection panel in the UI after refreshing the page.

## Face Swap Model

The application requires a face swapping model to perform the face replacement:

1. Create a `models/` directory at the root of the project if it doesn't exist:
   ```bash
   mkdir -p models
   ```

2. Place your face swapping model in the `models/` directory next to the docker-compose.yml file.
3. The model is automatically mounted to the container via a volume, so any changes to the `models/` directory on your host machine will be immediately available in the application.

## Development

### Project Structure

- `api/`: FastAPI backend for handling WebRTC connections and mask selection
- `frames-handler/`: Service for processing video frames and applying face swapping
- `ui/`: React frontend for user interaction
- `models/`: Directory for storing face swapping models
- `scripts/`: Utility scripts for development and deployment

### Running in Development Mode

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

This will:
- Build the services from source code
- Expose additional ports for debugging
- Mount local directories for live code changes

### API Endpoints

- `POST /api/offer`: Establish a WebRTC connection
- `GET /api/masks`: Get a list of available face masks
- `POST /api/masks`: Set the active face mask

## Troubleshooting

- **No video stream**: Ensure camera permissions are granted in your browser
- **Slow performance**: Check GPU utilization and ensure CUDA is properly configured
- **Connection issues**: Verify that all services are running with `docker-compose ps`
