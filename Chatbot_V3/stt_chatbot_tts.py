# import library
import speech_recognition as sr
import pyaudio
import requests as re
import os
from gtts import gTTS
import playsound

n = 1
while n == 1:
    ## xử lý chuyển giọng nói sang văn bản
    #print(sr.Microphone.list_microphone_names())

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Đọc tệp âm thanh dưới dạng source
    # nghe tệp âm thanh và lưu trữ trong biến audio_text

    # with sr.AudioFile("output.wav") as source:
    with sr.Microphone() as source:
        print("Bot: Mời bạn nói: ")
        audio_text = r.listen(source,phrase_time_limit=5,timeout=30, snowboy_configuration=None)
        # recoginize_() phương thức sẽ đưa ra lỗi yêu cầu nếu không thể truy cập được API, do đó sử dụng xử lý ngoại lệ
        try:
            # sử dụng nhận dạng giọng nói của Google
            text = r.recognize_google(audio_text, language="vi-VI")
            #print("Chuyển đổi bản ghi âm thành văn bản...")
            print("You: " + text)
        except:
            print("Bot: Bạn hãy nói gì đi, năn nỉ bạn đó.")
            output = gTTS("Bạn hãy nói gì đi, năn nỉ bạn đó.",lang="vi", slow=False)
            output.save("output.mp3")
            playsound.playsound('output.mp3', True)
            os.remove("output.mp3")
            #print("Bạn hãy nói gì đi...")
            audio_text = r.listen(source, timeout=30, phrase_time_limit=5, snowboy_configuration= None)
            try:
                # sử dụng nhận dạng giọng nói của Google
                text = r.recognize_google(audio_text, language="vi-VI")
                print("You: "+text)
            except:
                print("Bot : Xin chào, hãy cho tôi biết tên của bạn đễ tôi dễ xưng hô nhé.")
                text = "xin chào"
        with open("data/question.txt", "w", encoding="utf-8") as reader:
            reader.write(text + "\n")

    ## xử lý request api webhook rasa
    with open("data/question.txt", encoding="utf-8") as f:  # context manager
        content = f.readlines()
        content = [x.strip() for x in content]

    for item in content:
        data = {"message": item}

        resp = re.post("http://localhost:5005/webhooks/rest/webhook", json=data)
        answer = resp.json()[0]["text"]

        with open("data/answer.txt", "w", encoding="utf-8") as reader:
            reader.write(str(answer) + "\n")

    ## xử lý chuyển văn bản cua chatbot sang giọng nói
    with open("data/answer.txt", "r", encoding="utf-8") as file:
        output = gTTS(file.read(), lang="vi", slow=False)
    fs = open('data/answer.txt', 'r', encoding="utf-8")
    str1= fs.read()
    print("Bot: "+str1)
    output.save("output.mp3")
    playsound.playsound("output.mp3", True)
    os.remove("output.mp3")

