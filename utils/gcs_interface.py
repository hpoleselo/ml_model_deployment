from google.cloud import storage
import logging
import google.cloud.logging

client = storage.Client()

application_bucket = client.get_bucket('ml_model_api')

# Python's Native Logging
logging.basicConfig(level=logging.INFO,
             format='[%(levelname)s] - [%(funcName)s] - [%(filename)s:%(lineno)d] - [%(asctime)s] - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('app_logger')

# Cloud Logging
client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()

def write_to_gcs(filename: str, bucket: str = application_bucket):
    """ Writes to a file to Google Cloud Storage bucket. 
    
    Args:
    - bucket_name: Cloud storage client bucket
    - filename: Absolute path to the filename to be uploaded

    Returns:
    - object_gcs_id: String of the uploaded file
    """

    try:
        object_name_in_gcs_bucket = bucket.blob(filename)
        # TODO: Check if slicing for the filename is needed
        object_name_in_gcs_bucket.upload_from_filename(filename)
        logger.info(f"File {filename} succesfully written to GCS {bucket.name} bucket.")
        logger.info(f"With given object id: {bucket.id}.")
    except FileNotFoundError as e:
        logger.error(f"Could not find given file, check if the path is correct.\n{e}")

def read_from_gcs(filename: str, bucket: str = application_bucket):
    """ Reads a file from Google Cloud Storage.
    
    https://cloud.google.com/storage/docs/downloading-objects?hl=pt_br#code-samples-download-object
    """
    output_path = f"downloaded_{filename}"
    blob = bucket.blob(filename)
    blob.download_to_filename(output_path)
    logger.info("Downloaded file from GCS succesfully.")
    # If downloading to memory (to a string)
    #contents = blob.download_as_string()
    #print(contents)


if __name__ == "__main__":
    write_to_gcs("test.txt")
    read_from_gcs("test.txt")