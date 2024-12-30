# README

## Overview

This Python script is designed to read a video stream from an RTSP URL and save it to a local video file. The script leverages the OpenCV library to handle video capture and writing operations.

## Prerequisites

### Required Libraries
- **OpenCV**: Ensure you have OpenCV installed in your Python environment. You can install it using pip:
  ```bash
  pip install opencv-python
  ```

### RTSP Stream Configuration
Make sure you have access to an RTSP stream with valid credentials. The script uses the following RTSP URL format:
```
rtsp://<username>:<password>@<ip_address>:<port>/<path>
```

## Script Details

### Input
- **RTSP URL**: The script connects to the RTSP stream using the specified URL:
  ```python
  cap = cv2.VideoCapture("rtsp://admin:xckj2024@192.168.1.64:554/h264/ch1/sub/av_stream")
  ```
  Replace `admin`, `xckj2024`, and `192.168.1.64` with your actual credentials and IP address.

### Output
- The captured video is saved locally as `video/object_counting_output.avi`. The script uses the `mp4v` codec for video encoding.

### Functionality
1. **Video Capture**:
   - The script attempts to open the RTSP stream. If it fails, an assertion error is raised.
   - Video properties such as width, height, and frames per second (FPS) are read.

2. **Video Writing**:
   - The script initializes a video writer object using the extracted video properties.
   - Each frame from the RTSP stream is written to the output file.

3. **Termination**:
   - The script stops when the stream ends or an error occurs.
   - Resources such as the video capture and writer objects are released, and all OpenCV windows are closed.

## Usage

1. **Modify the RTSP URL**:
   Update the RTSP URL in the script with your credentials and the correct IP address.

2. **Run the Script**:
   Execute the script from your terminal or an IDE:
   ```bash
   python record.py
   ```

3. **Output Video**:
   After the script completes, check the `video` directory for the `object_counting_output.avi` file.

## Notes
- Ensure the RTSP URL is accessible and the credentials are valid.
- The script assumes the `video` directory exists. Create the directory if it does not.
  ```bash
  mkdir -p video
  ```
- The output video file will overwrite any existing file with the same name.

## Troubleshooting

1. **Assertion Error**:
   - Check if the RTSP URL is correct and the camera is reachable.
   - Verify your network connection.

2. **Empty Frames**:
   - Ensure the RTSP stream is active and not experiencing interruptions.

3. **Missing Codec**:
   - If you encounter codec issues, install the OpenCV contrib package:
     ```bash
     pip install opencv-contrib-python
     ```

## License
This script is open-source and available for personal or educational use. Modify it as needed for your specific requirements.

---

Feel free to customize this `README.md` file as per your project’s needs.

