# Video Steganography Analysis Tool

A powerful video steganography analysis tool that can decompose videos into different color channels, bit planes, and various steganography analysis views.

## Features

- Basic color channel separation (Red, Green, Blue, Grayscale)
- Saturation adjustment analysis
- Bit plane analysis (0-7 bits)
- Stegsolve style analysis
- Channel operation analysis (XOR, addition, subtraction)
- Color filter analysis
- Automatic audio synchronization
- Maintain original video frame rate

## Installation

1. Ensure Python 3.7+ is installed
2. Clone or download this project
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. On Windows:
```bash
# Double-click run.bat
# Or run in command line:
python video_color_separator.py
```

2. On Linux/MacOS:
```bash
# Add execute permission
chmod +x run.sh
# Run the script
./run.sh
# Or run the Python file directly
python3 video_color_separator.py
```

3. Select the video file to analyze in the file selection dialog
4. Choose the output directory
5. Wait for the processing to complete

## Output Structure

```
output_dir/
├── frames/                    # All frame images
│   ├── basic/                # Basic color channels
│   │   ├── blue/            # Blue channel
│   │   ├── green/           # Green channel
│   │   ├── red/             # Red channel
│   │   └── grayscale/       # Grayscale
│   ├── saturation/           # Saturation analysis
│   │   ├── low_sat/         # Low saturation
│   │   ├── normal_sat/      # Original saturation
│   │   └── high_sat/        # High saturation
│   ├── bit_planes/           # Bit plane analysis
│   │   ├── bit_plane_0/     # Bit plane 0
│   │   └── .../             # Up to bit plane 7
│   ├── stegsolve/            # Stegsolve style analysis
│   │   ├── red_plane/       # Red plane
│   │   ├── green_plane/     # Green plane
│   │   ├── blue_plane/      # Blue plane
│   │   └── .../             # Other analyses
│   └── steganography/        # Other steganography analyses
│       ├── xor_analysis/     # XOR analysis
│       ├── channel_operations/# Channel operations
│       └── color_filters/    # Color filters
└── videos/                    # Processed video files
```

## Notes

- Ensure sufficient disk space (at least 50 times the size of the original video is recommended)
- Processing large videos may take a long time
- The output videos will maintain the original video's frame rate and audio
- **All processes are executed sequentially, which may result in slower processing speeds**. Please be patient when processing large files.
- **This script was created using AI and has been tested on Windows 10. It should work on other systems, but please test or modify as needed.**

## System Requirements

- Windows/Linux/MacOS
- Python 3.7+
- 4GB+ RAM (recommended)
- Sufficient disk space

## Dependencies

- OpenCV (image processing)
- NumPy (numerical computation)
- MoviePy (video and audio processing)