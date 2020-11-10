from functools import wraps
from datetime import datetime
import rootpath
import logging
import os,sys
logger = logging.getLogger(__name__)
def is_valid_file(parser, arg):
    print(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists(arg):
        parser.error(f"The path `{arg}` does not exist!")
    else:
        return arg

def split_input_path(input_path):
    path = os.path.normpath(input_path)
    return os.path.dirname(path),os.path.basename(path)

def write_to_file(content,file_name):
    file_name = file_name.split('.')[0] + '.txt'
    output_path = os.path.join(rootpath.detect(),'output','transcriptions',file_name)
    # output_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), 'output', file_name)
    if os.path.exists(output_path):
        logger.info("Transcription of the audio file {} already exists. Overwriting transcription.".format(file_name))

    try:
        with open(output_path,'w+') as out:
            out.write(content)
            out.close()
            logger.info("Transcription is succesfully written to file {}".format(output_path))
    except IOError:
        logger.exception("I/O error")
    except FileNotFoundError:
        logger.exception("FileNotFoundError")
    except Exception:
        logger.exception("Unexpected error")


