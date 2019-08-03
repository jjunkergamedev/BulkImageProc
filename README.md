# BulkImageProc
Processes images in bulk for renaming, cropping, and resizing.

Usage:
python main.py --src <source pattern> --out <output directory> [--mode <mode>]

- src: The input files to process. Parsed with python's glob module; should look something like "SourceDirectory/*.png"
- out: The output directory. Use <path> as the relative path to the current working directory, e.g. "<path>/out".
- mode: The mode that determines how images are processed and renamed. Currently defaults to the only supported mode, "eternal_draft".

Modes:

eternal_draft:
Assumes input images are a 16x9 aspect ratio. Crops the image to the visible cards for an eternal draft, resizes and saves as jpeg.
Names images like "02_p1p2.jpg".

Requirements:
Must have Python Image Library installe. Get it with "pip install pillow".
