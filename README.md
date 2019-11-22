# Dynamic wallpaper changer for elementary OS

Simple wallpaper changing python script that reads gnome dynamic wallpaper xml files.
At the moment not much more than a proof of concept... but hey... it works :).

## Requirements
- beautifulsoup 4 (pip3 install beautifulsoup4)

## Usage
- python3 eos_dynwall.py <path/to/your/xml/file>

## Current limitations:

- It expects the start time to be midnight and the images to cover the full 24 hours of a day. 
