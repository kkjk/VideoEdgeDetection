# VideoEdgeDetection

**Canny Edge Detector without predefined functions from opencv like Canny, GaussianBlur,..**

## Python packages/libraries used:
- `OpenCV` (only for opening/closing video files )
- `numpy` (for fourier transforms and array manipulation)
- `PyQt5` for the GUI


## Usage

1.GUI.py

2.Canny_v.py

3.fft_convolution_v.py

Run `python GUI.py`

Upload the video file using `File -> Open` in the GUI

PRESS 'CONVERT' in the GUI to start edge detection process.

Note: 

1. The program takes too long to complete execution with high resolution video file. Each frame takes about 
35 seconds for edges to be detected, so the entire video processes might take a longgg time.

2. low and high thresholds for double threshold step in Canny Edge detection have been hard coded.They can be 
changed in the `non_max_suppression_with_threshold_and_hystersis` function (high, low)


