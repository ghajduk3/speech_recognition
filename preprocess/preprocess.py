import fleep
import sys,io
from pydub import AudioSegment
import logging
logger = logging.getLogger(__name__)
class Preprocess:
    """
    A class to represent preprocessing.

    """

    @staticmethod
    def getAudioFormat(audio_file_object:bytes)->str:
        '''
        Returns the format of audio file.

                Parameters:
                        audio_file_object (bytes): A audio file object

                Returns:
                        format (str): Format of audio file.
        '''
        info = fleep.get(audio_file_object)
        logger.debug("Determining format of input file")
        if info.type[0] == 'audio':
            logger.debug('Input audio is {} formatted '.format(info.extension[0]))
            return info.extension[0]
        else:
            logger.error("Input file is not audio. Please input the audio file type")
            sys.exit()

    @staticmethod
    def getAudioMetadata(audio_file_object:bytes)->tuple:
        '''
        Returns the metadata(number of channel and frame rate) of audio file.

                Parameters:
                        audio_file_object (bytes): A audio file object

                Returns:
                        channels (int): Number of channels
                        frame_rate (int): Frame rate
        '''
        logger.debug("Extracting audio metadata")
        audio_file = AudioSegment.from_file(io.BytesIO(audio_file_object),Preprocess.getAudioFormat(audio_file_object))
        return (audio_file.channels, audio_file.frame_rate)

    @staticmethod
    def preprocessAudio(input_path:str)->tuple:
        '''
        Preprocess audio file.

                Parameters:
                        input_path (str): Absolute or relative path to audio file
                Returns:
                        audio_file_object (bytes): Raw audio file
                        channels (int):Number of channels
                        frame_rate (int): Frame rate
        '''
        try:
            logger.debug("Reading audio file from path {}".format(input_path))
            with io.open(input_path, "rb") as audio_file:
                audio_file_object = audio_file.read()
            return (audio_file_object,Preprocess.getAudioMetadata(audio_file_object))
        except IOError:
            logger.exception("I/O error")
        except FileNotFoundError:
            logger.exception("FileNotFoundError")
        except Exception:
            logger.exception("Unexpected error")









