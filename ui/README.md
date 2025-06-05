# Deep Fake Live

A web application that allows users to apply different face masks to a live video stream in real-time.

## About

Deep Fake Live is a React-based web application that demonstrates the capabilities of deep fake technology. It allows users to select from various pre-defined face masks (including political figures like Putin, Trump, and Obama) and overlay them onto a video stream in real-time.

The application features:
- A sidebar for selecting different face masks
- A main video player that displays the stream with the selected face overlay
- A responsive design for various screen sizes

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Docker and Docker Compose (for containerized deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd deep-fake-live/ui
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Development

To start the development server:

```bash
npm build dev
```

This will start the Vite development server with hot module replacement (HMR) at `http://localhost:5173`.

### Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run lint` - Run ESLint to check for code issues
- `npm run preview` - Preview the production build locally

## Building for Production

To build the application for production:

```bash
npm build build
```

This will create a `dist` directory with the compiled assets ready for deployment.

## Docker Deployment

The application can be deployed using Docker:

1. Build and start the container:
   ```bash
   docker-compose up -d
   ```

2. Access the application at `http://localhost:3000`

3. To stop the container:
   ```bash
   docker-compose down
   ```

## Project Structure

- `src/` - Source code
  - `components/` - React components
    - `stream/` - Video stream components
    - `sidebar/` - Masks components for face selection
  - `App.tsx` - Main application component
  - `index.css` - Global styles
- `public/` - Static assets
  - `faces/` - Face mask images
  - `demo.mp4` - Demo video for streaming

## Technologies Used

- React 19
- TypeScript
- Vite
- Docker
- Nginx (for production deployment)
