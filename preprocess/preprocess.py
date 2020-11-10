import fleep
import sys,io
from pydub import AudioSegment
import logging
logger = logging.getLogger(__name__)
class Preprocess:

    @staticmethod
    def getAudioFormat(audio_file)->str:
        info = fleep.get(audio_file)
        logger.debug("Determining format of input file")
        if info.type[0] == 'audio':
            logger.debug('Input audio is {} formatted '.format(info.extension[0]))
            return info.extension[0]
        else:
            logger.error("Input file is not audio. Please input the audio file type")
            sys.exit()

    @staticmethod
    def getAudioMetadata(audio_file_object)->tuple:
        logger.debug("Extracting audio metadata")
        audio_file = AudioSegment.from_file(io.BytesIO(audio_file_object),Preprocess.getAudioFormat(audio_file_object))
        return (audio_file.channels, audio_file.frame_rate)

    @staticmethod
    def preprocessAudio(input_path):
        try:
            logger.debug("Reading audio file from path {}".format(input_path))
            with io.open(input_path, "rb") as audio_file:
                audio_file_object = audio_file.read()
            return audio_file_object, Preprocess.getAudioMetadata(audio_file_object)
        except IOError:
            logger.exception("I/O error")
        except FileNotFoundError:
            logger.exception("FileNotFoundError")
        except Exception:
            logger.exception("Unexpected error")









