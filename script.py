import os
import logging
import multiprocessing
import face_recognition
from PIL import Image
import shutil

# Directory containing the photos to be processed
photo_dir = "/app/photos"
# Maximum number of faces to detect
max_faces = 50

# Logging configuration
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.getLogger('PIL').setLevel(logging.INFO)


# Function to detect faces in an image and return the file name if faces are detected
def detect_faces(filename):

    f = os.path.join("/app/photos", filename)
    
    image = face_recognition.load_image_file(f)

    # Find all the faces in the image
    face_locations = face_recognition.face_locations(image)

    # If at least one face is detected, return the file name
    if len(face_locations) > 0:
        logging.info(f'faces found in: {f}')
        shutil.copy(f, f"/app/photos/training/{filename}")
        files = os.listdir(f"/app/photos/training/")
        logging.info(f"size: {len(files)}")
        return filename
    else:
        logging.debug(f'no faces found in: {os.path.join(photo_dir, filename)}')


# Function to process a batch of files
def process_batch(batch_files, result_queue):
    for filename in batch_files:
        result = detect_faces(filename)
        if result:
            result_queue.put(result)
            logging.debug(f"Processed batch with {len(batch_files)} files. Current results in queue: {list(result_queue.queue)}")


# Main function
def main():
    # Get a list of all the JPEG files in the directory
    filenames = [filename for filename in os.listdir(photo_dir) if filename.endswith(".jpg") or filename.endswith(".jpeg")]
    num_files = len(filenames)
    logging.info(f"Found {num_files} image files in {photo_dir}")

    # Set up the multiprocessing pool
    #num_processes = min(multiprocessing.cpu_count(), num_files)
    num_processes = 4
    pool = multiprocessing.Pool(processes=num_processes)

    # Divide the file list into batches of 100 files each
    batch_size = 20
    num_batches = (num_files + batch_size - 1) // batch_size
    logging.debug(f"Dividing files into {num_batches} batches of {batch_size} files each")
    batches = [filenames[i*batch_size:(i+1)*batch_size] for i in range(num_batches)]

    # Start processing the batches in parallel
    result_queue = multiprocessing.Manager().Queue()
    logging.info(f"Starting processing with {num_processes} processes")
    for batch_num, batch_files in enumerate(batches):
        #logging.debug(f"Starting batch {batch_num}")
        pool.apply_async(process_batch, args=(batch_files, result_queue))


    # Wait for all batches to finish processing
    pool.close()
    pool.join()
    logging.info("Processing complete")

    # Print the list of files with detected faces
    logging.info(f"Detected faces in {result_queue.qsize()} image files:")
    while not result_queue.empty():
        logging.info(result_queue.get())

if __name__ == "__main__":
    main()
