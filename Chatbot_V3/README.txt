OS Linux (ubuntu18.04) or window10
Python3.6+
#### cài đặt môi trường ảo để làm việc ngay trong thư mục chatbot_v2
+ sudo apt update
+ sudo -H pip3 install --upgrade pip
+ python3 -m pip install --user virtualenv

- tạo thư mục môi trường ảo
+ virtualenv -p pthon3 env

- truy cập vào môi trường ảo để làm việc
+ source env/bin/activate


#### cài đặt các gói thư viện cần thiết để chatbot_v3_p
+ sudo apt update
+ sudo -H pip3 install --upgrade pip
+ pip install --upgrade setuptools pip
+ pip install --upgrade pip setuptools wheel
+ pip install rasa==1.7.0
+ pip install rasa[spacy]
+ python -m spacy download en_core_web_md
+ python -m spacy link en_core_web_md en


#### su dung void vs rasa 
- cai dat cac goi sau 
+ pip install SpeechRecognition
+ pip install gtts
+ pip install playsound
+ pip install PyAudio
- khi cai dat Pyaudio se gap error, cach fix loi nhu sau
+ sudo apt-get install portaudio19-dev python-pyaudio
+ pip install PyAudio

- run file stt_chatbot_tts.py: python stt_chatbot_tts.py , gap error module 'gi' -> cach fix
+ sudo apt-get install python3-gi
+ pip install vext
+ pip install vext.gi

### Run chatbot tren LOCAL
+ rasa train
+ rasa run actions
+ rasa shell (dạng text)
+ python stt_chatbot_tts.py (dạng voice)// yêu cầu máy connect internet
