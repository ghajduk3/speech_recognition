import logging

from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError,NotFound

from utils.singleton import SingletonMeta

logger = logging.getLogger(__name__)

class GoogleCloud(metaclass=SingletonMeta):

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

    def upload_blob(self, source_file_name, destination_blob_name):
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


    def delete_blob(self, blob_name):
        try:
            logger.info("Deleting blob {} from bucket {}".format(blob_name,self.bucket_name))
            blob = self.bucket.blob(blob_name)
            blob.delete()
            logger.info("Successfully deleted blob {} from bucket {}".format(blob_name,self.bucket_name))
        except NotFound:
            logger.exception("Blob not found")
        except Exception:
            logger.exception("Unexpected error")




