## Concurrent Face Detection

This script is used to detect faces in images within a specified directory. It uses the Python `face_recognition` library to detect faces and the `PIL` library to work with images.

### Usage

The script requires a directory containing the images to be processed. The directory is set using the `photo_dir` variable at the beginning of the script.

The script will search for all JPEG files (`.jpg` or `.jpeg` extensions) within the specified directory and its subdirectories. It will then use multiple processes to detect faces in the images in parallel.

The maximum number of faces to detect can be set using the `max_faces` variable at the beginning of the script.

The script outputs a log to the console using the `logging` module. By default, it logs at the `INFO` level, but the `DEBUG` level can be enabled by uncommenting the appropriate line.

The script prints the list of files with detected faces to the console.

### Requirements

- Python 3.6 or higher
- `face_recognition` library
- `PIL` library

### Notes

- The script only works with JPEG files. Other file formats are not supported.
- The script may take some time to run, especially if there are many images to process. The processing time can be reduced by increasing the number of processes used, which can be set by changing the `num_processes` variable. However, increasing the number of processes will also increase the amount of system resources used.
