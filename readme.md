# Cyberdudebivash's Image File Inspection Utility

## Description

This is a simple GUI application built with Tkinter for detecting and inspecting image files. It analyzes images to extract file creation date, location (if GPS data available), metadata details, system information (e.g., camera make/model), and source details (inferred from metadata).

**Note:** For educational purposes. Supports images with EXIF data (e.g., JPEG, TIFF). Other formats like PNG may have limited metadata.

## Requirements

- Python 3.x
- Packages: See `requirements.txt`

## Installation

1. Install dependencies: `pip install -r requirements.txt`
2. Run `python main.py`

## Usage

1. Launch the app: `python main.py`
2. **Select Image File:** Choose a single image to analyze immediately.
3. **Scan Folder for Images:** Select a folder to scan for images. Found images will be listed; select one and click "Analyze Selected Image" to inspect.
4. Results will display in the text area, including:
   - File metadata (creation date, size, path)
   - EXIF data (capture date, GPS location, camera info, software)
   - Full metadata dump
   - Source details (inferred from EXIF)

## Limitations

- Relies on EXIF for detailed metadata; not all images have this.
- No advanced forensics; expand with libraries like hachoir for more formats.
- GUI is basic; enhance as needed.

## License

MIT License .

##COPYRIGHT@CYBERDUDEBIVASH 2025