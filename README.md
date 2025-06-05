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

- **UI**: React-based web interface for user interaction
- **API**: FastAPI backend that handles WebRTC connections and mask selection
- **Frames Handler**: Processes video frames and applies face swapping
- **RabbitMQ**: Message broker for frame data exchange between components
- **Redis**: In-memory database for caching and temporary storage

## Requirements

- Docker and Docker Compose
- NVIDIA GPU with CUDA support
- Modern web browser with WebRTC support

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fakely-live.git
   cd fakely-live
   ```

2. Create an `.env` file with the required environment variables:
   ```
   RABBITMQ_HOST=rabbitmq
   RABBITMQ_USER=guest
   RABBITMQ_PASSWORD=guest
   ```

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

   For development:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
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

## Development

### Project Structure

- `api/`: FastAPI backend for handling WebRTC connections and mask selection
- `frames-handler/`: Service for processing video frames and applying face swapping
- `ui/`: React frontend for user interaction
- `models/`: Directory for storing face swapping models
- `scripts/`: Utility scripts for development and deployment

### Running in Development Mode

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
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
