from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_sdk import Action
#from rasa_core_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import Restarted

import requests
#import json
from bs4 import BeautifulSoup
from pyvi import ViTokenizer, ViPosTagger
###
from typing import Text, List, Dict, Any
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet, ActionExecuted, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
import re
import sqlite3
#from rasa_core_sdk.events import SessionStarted
#connect to database
sqliteConnection = sqlite3.connect('khohangrasa.db')
cursor = sqliteConnection.cursor()
print("Database created and Successfully Connected to SQLite")
#cursor.execute("SELECT linh_kien, loai_linh_kien, gia from KHOHANG")
#record = cursor.fetchall()
#for index in record:
#    linh_kien = index[0].lower()
#    loai_linh_kien = index[1].lower()
#    gia = index[2]
#    print(linh_kien)
#    print(loai_linh_kien)
#    print(gia)

def name_cap(text):
    tarr = text.split()
    for idx in range(len(tarr)):
        tarr[idx] = tarr[idx].capitalize()
    return ' '.join(tarr)

class action_save_cust_info(Action):
    def name(self):
        return 'action_save_cust_info'

    def run(self, dispatcher, tracker, domain):
        user_id = (tracker.current_state())["sender_id"]
        print(user_id)
        cust_name = next(tracker.get_latest_entity_values("cust_name"), None)
        cust_sex = next(tracker.get_latest_entity_values("cust_sex"), None)
        bot_position = "Tecapro-Telecom"

        if (cust_sex is  None):
            cust_sex = "Quý khách"

        if (cust_sex == "anh") | (cust_sex == "chị"):
           bot_position = "em"
        elif (cust_sex == "cô") | (cust_sex == "chú"):
            bot_position = "cháu"
        else:
            cust_sex = "Quý khách"
            bot_position = "Tecapro-Telecom"

        if not cust_name:
            dispatcher.utter_template("utter_greet_name",tracker)
            return []

        print (name_cap(cust_name))
        return [SlotSet('cust_name', " "+name_cap(cust_name)),SlotSet('cust_sex', name_cap(cust_sex)),SlotSet('bot_position', name_cap(bot_position))]


class action_save_mobile_no(Action):
    def name(self):
        return 'action_save_mobile_no'

    def run(self, dispatcher, tracker, domain):
        user_id = (tracker.current_state())["sender_id"]
        print(user_id)
        mobile_no = next(tracker.get_latest_entity_values("inp_number"), None)

        if not mobile_no:
            return  [UserUtteranceReverted()]

        mobile_no = mobile_no.replace(" ","")
        #print (cust_name)
        return [SlotSet('mobile_no', mobile_no)]


#class clear cac bo nho slot cua Bot sau khi 1 messager toi
class action_reset_slot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("transfer_nick", None),SlotSet("transfer_amount", None),SlotSet("transfer_amount_unit", None)]

#### Database class

#class xu ly event loai_linh_kien
class ActionAskKnowledgeBaseLoaiLinhKien(Action):
    def name(self) -> Text:
        return "action_custom_loai_linh_kien"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        text_input = text.lower()
        cursor.execute("SELECT linh_kien, loai_linh_kien, gia from KHOHANG")
        record = cursor.fetchall()
        check = False
        for result in record:
            linh_kien = result[0].lower()
            loai_linh_kien = result[1].lower()
            #gia = str(result[2])
            if loai_linh_kien in text_input:
                check = True
                dispatcher.utter_message(loai_linh_kien+": "+linh_kien)       
        if not check:
            dispatcher.utter_message("Hiện tại trong kho không có loại linh kiện này.")
        return [SlotSet("linh_kien", loai_linh_kien)]
        
#class envent xu ly linh_kien
class ActionAskKnowledgeBaseLinhKien(Action):

    def name(self) -> Text:
        return "action_custom_linh_kien"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        text_input = text.lower()
        cursor.execute("SELECT linh_kien, loai_linh_kien, gia from KHOHANG")
        record = cursor.fetchall()
        linh_kien_slot = str(tracker.get_slot("linh_kien")).lower() #lấy ra slot được khai báo trong domain
        check = False
        for index in record:
            linh_kien = index[0].lower()
            #loai_linh_kien = index[1].lower()
            gia = str(index[2])
            if linh_kien in text_input:
                check = True
                dispatcher.utter_message(linh_kien+ " có giá: "+gia)
        if linh_kien_slot in text_input:
            check = True
            dispatcher.utter_message("Xin lỗi hình như bạn đang nhầm giữa tên 'linh kiện' với 'loại linh kiện'")
        elif not check:
            dispatcher.utter_message("Hiện tại trong kho không có loại linh kiện này.")
        return [SlotSet("linh_kien", gia)]


#python -m rasa_sdk.endpoint --actions actions
#python -m rasa_core_sdk.endpoint --actions actions
#start server rasa tai localhost: rasa run --endpoints endpoints.yml --credentials credentials.ym
#python -m rasa_core.run -d models/dialogue -u models/nlu/default/chat --port 5002 --credential credentials.yml
#python -m rasa_core.run --enable_api -d models/dialogue -u models/nlu/default/chat -o out.log 