from audio_recorder.listener import Listener
from audio_recorder.player import Player
from audio_recorder.recorder import Recorder
from preprocess.preprocess import Preprocess
import argparse,rootpath,os
from cloud.Google_cloud import GoogleCloud
import logging
from utils import is_valid_file,split_input_path,write_to_file
from transcription import Transcription
from dotenv import load_dotenv
from emails.mail_server import MailServer
from datetime import date
logger = logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
load_dotenv()


def processArgs():
    parser = argparse.ArgumentParser(description='Speech to text Google Speech Api interface for Slovenian language. Documentation can be found on  <github documentation link>')
    parser.add_argument('-i', '--input', required=True, default='empty',
                        help='[required] Input audio file path.', metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-s', '--storage', required=True, default='server', type=str,
                        help='[required] Which storage type to use for saving audio file. Available options (server|gcs) ,default is local.')
    parser.add_argument('-b', '--bucket', required=False, default='a1audio', type=str,
                        help='[optional] Google cloud storage bucket name. Required for Google cloud storage type(gcs).')
    return parser.parse_args()


if __name__ == '__main__':
    # args = processArgs()

    r = Recorder()
    p = Player()
    l = Listener(r, p)
    l.start() #keyboard listener is a thread so we start it here
    l.join() #wait for the tread to terminate so the program doesn't instantly close


    audio_file_name = l.audio_path
    folder_name = os.path.join(rootpath.detect(),'output','audio')
    audio_object, (audio_channels, audio_frame_rate) = Preprocess.preprocessAudio(os.path.join(folder_name,audio_file_name))
    bucket_name = 'a1audio'
    trans = Transcription(folder_name, audio_file_name, bucket_name, audio_channels, audio_frame_rate)
    write_to_file(trans.transcribe_from_file(audio_object), audio_file_name)

    subject = "Meeting transcription, {}".format(date.today().strftime("%Y-%m-%d"))
    body = "Please find the meeting's transcription enclosed in the attachment."
    serve = MailServer()
    receivers = ['a1testmailrecord@gmail.com']
    serve.send_mail(subject,body,os.path.join(rootpath.detect(),'output','transcriptions',audio_file_name.split('.')[0] + '.txt'), receivers)



    # folder_name,audio_file_name = split_input_path(args.input)
    #
    # bucket_name = args.bucket
    #
    # audio_object,(audio_channels,audio_frame_rate) = Preprocess.preprocessAudio(args.input)
    # trans = Transcription(folder_name,audio_file_name,bucket_name,audio_channels,audio_frame_rate)
    #
    # if args.storage == 'gcs':
    #     gc = GoogleCloud(bucket_name)
    #     gc.upload_blob(args.input, audio_file_name)
    #     write_to_file(trans.transcribe_from_gcs(),audio_file_name)
    #     gc.delete_blob(audio_file_name)
    # else:
    #     write_to_file(trans.transcribe_from_file(audio_object),audio_file_name)


