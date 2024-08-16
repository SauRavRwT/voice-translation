# Speech Translation

## Setup

1. Clone the repository: 

```bash
git clone https://github.com/SauRavRwT/voice-translation.git
```
2. Navigate to the project directory: 

```bash
cd voice-translation
```
3. create python virtual env: 

```bash
mkdir venv # making dir

python -m venv venv # making virtual env
```
4. To activate virtual env: 

```bash
source venv/bin/activate  # For Linux/Mac

venv\scripts\activate  # For Windows
```
5. Install python dependencies: 

```bash
!pip install googletrans==4.0.0-rc1

!pip install gtts googletrans==4.0.0-rc1 speechrecognition pydub

!pip install sounddevice googletrans==4.0.0-rc1 gtts speechrecognition pydub

!pip install sounddevice wavio SpeechRecognition

!pip install langdetect

!pip install sounddevice wavio SpeechRecognition googletrans==4.0.0-rc1 langdetect gtts pydub

!pip install sounddevice numpy pygame

!pip install sounddevice numpy pygame speech_recognition googletrans==4.0.0-rc1 gTTS langdetect
```

6. Now you are done!!, Run your python file: 

```bash
python speech_translation.py
```