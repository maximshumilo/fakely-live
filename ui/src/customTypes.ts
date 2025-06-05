export interface HTMLMediaElementWithCaptureStream extends HTMLVideoElement{
  captureStream(): MediaStream;
}