# no-red

This is a Python script to find and mark red pixels in an image.

## Description

The script `no-red.py` counts the number of pixels where the red color is dominant in the given image, logs the details, and marks the top 3 most dominant red pixels with rectangles in the output image.

## Usage

To use the script, run the following command:

```sh
python no-red.py
```

This will process the image `no-red.png`, save the marked image as `no-red-marked.png`, and log the details in `red_pixels_log.txt`.

## Requirements

- Pillow

Install the required package using:

```sh
pip install -r requirements.txt
```