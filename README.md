# DMDraw: A Simple DMD Pattern Generator

A Python application for generating Digital Micromirror Device (DMD) patterns and saving them as 1-bit BMP files.

## Features

- **912×1140 pixel pattern**: Creates patterns with the exact dimensions required for DMD applications
- **1-bit BMP output**: Saves patterns as 1-bit depth BMP files
- **Interactive GUI**: Visual interface with real-time preview
- **Pattern tools**: Add rectangles, circles, and lines to create complex patterns
- **Utility functions**: Clear, invert, and generate random patterns
- **Live preview**: See your pattern before saving

## Context: The TI DLP 4500 DMD
This software is desined to work with the Texas Instruments DLP 4500 DMD. On this device, the pixels are right diamonds oriented in zig-zagging rows and columns as follows. Before using this software, please see the TI docs [here](https://www.ti.com/lit/ds/symlink/dlp4500.pdf?ts=1755526644323&ref_url=https%253A%252F%252Fwww.ti.com%252Fproduct%252FDLP4500)

## Installation

1. Install Python 3.7 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python dmd_pattern_generator.py
```

### Pattern Tools

- **Rectangle**: Add rectangular regions by specifying X, Y coordinates and width/height
- **Circle**: Add circular regions by specifying center coordinates and radius
- **Line**: Draw lines between two points using Bresenham's algorithm

### Utilities

- **Clear Pattern**: Reset the pattern to all zeros
- **Invert Pattern**: Flip all pixels (0→1, 1→0)
- **Random Pattern**: Generate a random pattern

### Saving

Click "Save as BMP" to save your pattern. The application will:
1. Show a file save dialog
2. Convert the pattern to 1-bit BMP format
3. Display a success message with the file location

## File Format

The generated BMP files are:
- **Dimensions**: 912 columns × 1140 rows
- **Bit depth**: 1 bit per pixel (black and white only)
- **Format**: Standard BMP format compatible with DMD systems

## Dependencies

- `numpy`: Array manipulation and mathematical operations
- `Pillow`: Image processing and BMP file creation
- `tkinter`: GUI framework (included with Python)
