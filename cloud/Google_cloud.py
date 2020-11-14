import logging

from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError,NotFound

from utils.singleton import SingletonMeta

logger = logging.getLogger(__name__)

class GoogleCloud(metaclass=SingletonMeta):
    """
    A singleton patterned class to represent connection and upload/delete operations to Google Cloud Storage .

    ...

    Attributes
    ----------
    bucket_name : str
        name of the google cloud storage bucket

    Methods
    -------
    upload_blob(source_file_name,destination_blob_name):
        Uploads blob from file to the destination's GCS bucket.
    delete_blob(blob_name):
         Deletes the blob from GCS bucket.
    """

    def __init__(self, bucket_name):
        """
        Constructs all the necessary attributes for the google cloud object.

        Parameters
        ----------
            bucket_name : str
                name of the google cloud storage bucket
            storage_client : google.cloud.storage.Client
                storage client object
            bucket :
                gcs bucket object

        """
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

    def upload_blob(self, source_file_name:str, destination_blob_name:str):
        '''
        Uploads blob from file to the destination's GCS bucket.

                Parameters:
                        source_file_name (str) : Source file name of the object to be uploaded to GCS bucket
                        destination_blob_name (str) : File name by which it is stored in GCS bucket.

        '''
        try:
            logger.info("Uploading blob {} to 'gs://'+ {} + '/' + {}".format(destination_blob_name,self.bucket_name,destination_blob_name))
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
            logger.info("Successfully uploaded blob {}".format(destination_blob_name))
        except GoogleCloudError:
            logger.exception("GoogleCloudError")
        except NotFound:
            logger.exception("Blob not found")
        except:
            logger.exception("Unexpected error")


    def delete_blob(self, blob_name:str):
        '''
         Deletes the blob from GCS bucket.

                Parameters:
                        blob_name (str) : Name of the blob to be deleted from GCS bucket.

        '''
        try:
            logger.info("Deleting blob {} from bucket {}".format(blob_name,self.bucket_name))
            blob = self.bucket.blob(blob_name)
            blob.delete()
            logger.info("Successfully deleted blob {} from bucket {}".format(blob_name,self.bucket_name))
        except NotFound:
            logger.exception("Blob not found")
        except Exception:
            logger.exception("Unexpected error")




