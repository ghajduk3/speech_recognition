from cloud.Google_cloud import GoogleCloud
from google.cloud import speech
import logging
logger = logging.getLogger(__name__)
class Transcription:
    """
    A class to represent speech-to-text transcription using Google Cloud speech api.

    ...

    Attributes
    ----------
    input_file_path : str
        absolute or relative path to audio file
    audio_file_name : str
        audio file name
    bucket_name : str
        google cloud storage bucket name
    audio_channel_count : int
        number of channels
    sample_rate_hertz : int
        frame rate


    Methods
    -------
    transcribe_from_gcs():
        Uses google cloud speech api to transcribe speech in Slovenian to text from audio file stored in GCS bucket
    transcribe_from_file(content):
         Uses google cloud speech api to transcribe speech in Slovenian to text from audio file object stored locally.
    """

    def __init__(self,input_file_path,audio_file_name,bucket_name,audio_channel_count,sample_rate_hertz):
        """
        Constructs all the necessary attributes for the transcription object.

        Parameters
        ----------
            input_file_path : str
                absolute or relative path to audio file
            audio_file_name : str
                audio file name
            bucket_name : str
                google cloud storage bucket name
            audio_channel_count : int
                number of channels
            sample_rate_hertz : int
                frame rate

        """
        self.input_file_path = input_file_path
        self.audio_file_name = audio_file_name
        self.bucket_name = bucket_name
        self.google_cloud_storage_uri = 'gs://'+ bucket_name + '/' + audio_file_name
        self.gcs = GoogleCloud(bucket_name)
        self.audio_channel_count = audio_channel_count
        self.sample_rate_hertz = sample_rate_hertz

    def transcribe_from_gcs(self)->str:
        '''
        Uses google cloud speech api to transcribe speech in Slovenian to text from audio file stored in GCS bucket

                Returns:
                        transcript (str): Textual representation of the audio file
        '''
        transcript = ''
        logger.info("Initializing google speech client")
        client = speech.SpeechClient()
        logger.info("Getting audio file from gcs {}".format(self.google_cloud_storage_uri))
        audio = speech.RecognitionAudio(uri=self.google_cloud_storage_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="sl-SI",
            audio_channel_count=self.audio_channel_count,
            sample_rate_hertz = self.sample_rate_hertz,
            enable_automatic_punctuation=True,
            model="command_and_search"
        )
        logger.info("Transcribing audio file")
        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=10000)
        for result in response.results:
            transcript += result.alternatives[0].transcript
        logger.info("Audio file is successfully transcribed")
        return transcript

    def transcribe_from_file(self,content:bytes)->str:
        '''
         Uses google cloud speech api to transcribe speech in Slovenian to text from audio file object stored locally.

                Parameters:
                        content (bytes): Raw audio file
                Returns:
                        transcript (str): Textual representation of the audio file
        '''
        transcript = ''
        logger.info("Initializing google speech client")
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="sl-SI",
            audio_channel_count=self.audio_channel_count,
            sample_rate_hertz = self.sample_rate_hertz,
            enable_automatic_punctuation=True,
            model="command_and_search"
        )
        logger.info("Transcribing audio file")
        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=10000)
        for result in response.results:
            transcript += result.alternatives[0].transcript
        logger.info("Audio file is successfully transcribed")
        return transcript





