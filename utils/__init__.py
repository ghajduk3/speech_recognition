import rootpath
import logging
import os
from postprocess.postprocess import Postprocess
logger = logging.getLogger(__name__)

def split_input_path(input_path:str)->tuple:
    '''
    Splits absolute file path to the directory path and the filename.ext.

            Parameters:
                    input_path (str): Absolute or relative path.
            Returns:
                    dir_name (str): Path to the directory of the file
                    file_name (str): File name
    '''
    path = os.path.normpath(input_path)
    return (os.path.dirname(path),os.path.basename(path))

def write_to_file(content,file_name):
    '''
    Writes raw textual content to the output file.

            Parameters:
                    content (bytes): Textual transcription
                    file_name (str): Name of textual file to be created
    '''
    file_name = file_name.split('.')[0] + '.txt'
    output_path = os.path.join(rootpath.detect(),'output','transcriptions',file_name)
    if os.path.exists(output_path):
        logger.info("Transcription of the audio file {} already exists. Overwriting transcription.".format(file_name))
    try:
        with open(output_path,'w+') as out:
            out.write(Postprocess.add_punctuation(content))
            out.close()
            logger.info("Transcription is succesfully written to file {}".format(output_path))
    except IOError:
        logger.exception("I/O error")
    except FileNotFoundError:
        logger.exception("FileNotFoundError")
    except Exception:
        logger.exception("Unexpected error")


