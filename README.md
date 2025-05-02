# SIFT-Based Object Detection in Images and Video

This project utilizes OpenCV's SIFT feature detector and FLANN matcher to locate a query object in both a target image and a video stream. Homography estimation is applied to project the object's outline onto the target.

## Core Concepts

- **SIFT (Scale-Invariant Feature Transform)** : Detects keypoints and computes descriptors invariant to scale and rotation.
- **FLANN (Fast Library for Approximate Nearest Neighbors)** : Efficiently matches descriptors.
- **Lowe’s Ratio Test** : Filters ambiguous matches.
- **Homography** : Estimates perspective transformation between matching points.

## File Structure

```
project/
│
├── query.png          # Object to detect
├── target.jpg         # Image containing the object
├── cocacola.mp4       # Video for real-time object detection
└── SIFT.ipynb         # Main Python script
```

## How It Works

1. Load the query and target images in grayscale.
2. Detect and compute SIFT keypoints and descriptors.
3. Match descriptors using FLANN with Lowe's ratio test.
4. If sufficient good matches are found:
   - Compute homography using RANSAC.
   - Project the query object onto the target using `cv2.perspectiveTransform`.
   - Visualize results with a bounding box and keypoint matches.
5. Repeat the same steps per frame for video detection.

## Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- NumPy
- Matplotlib (for image display)

Install dependencies with:

```bash
pip install opencv-python numpy matplotlib
```

## Sample Use

### Image Detection

Detects the query object in a still image, highlighting the match with a bounding polygon and drawing feature matches.

### Video Detection

Tracks the object in a video stream, continuously detecting and updating its position in each frame.

## Controls

- Press `Q` to exit the video window.
