# Speech-to-text for Slovene language 
- [Setup](#setup)
- [Description](#description)

## Setup

The following instructions assume that the user has cloned the repo and is in the project's root.

- Install the required packages listed in requirements.txt
```shell script
pip install -r requirements.txt
```
- In case of having troubles upon installation of PyAudio on Windows. Install PyAudio via `pipwin`
```shell script
pip install pipwin
pipwin install PyAudio
```
**NOTE:** as a prerequisite you must have `gcloud` account. Follow the [steps](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries) required for initial setup of the project.
Do not forget to set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of the JSON file that contains your service account key.
Also, the GC storage bucket is required. Please, fill the name of it in .env file. 
I.e on Linux :
```shell script
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```
- In order to configure e-mail server please copy the .env_example file to .env and fill in your config
 

**Running the app locally**
- Position in the project's root directory. Then, run following command:
```shell script
python main.py  
```

## Description
***Speech-recognition*** is a simple python cli application that conducts speech-to-text transcription for Slovene language.
The app flow consists of three main parts:
- ****Speech recorder**** - Input microphone audio is recorded while `ctrl` button is pressed. The wav file is saved into `{root}/output/audio/audio_file*.wav` 
- ****Speech transcription**** - Input speech file is transcribed into textual file via Google Cloud speech api. The transcription is saved into  `{root}/output/transcriptions/audio_file*.txt`
- ****Transcription mailer**** - Mails the transcribed speech file to the mailer list.