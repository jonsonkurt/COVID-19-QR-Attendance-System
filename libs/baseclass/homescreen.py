from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.toast.kivytoast import toast
from kivy.uix.screenmanager import NoTransition, Screen
from libs.baseclass import user_key, class_key
import sqlite3
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.utils import asynckivy
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
import cv2
import pyzbar.pyzbar as pyzbar
import time
import winsound

Builder.load_file('./libs/kv/homescreen.kv')

scanned_student_names = []

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1500  # Set Duration To 1000 ms == 1 second

class HomeScreen(Screen):

    student_number = StringProperty()
    student_name = StringProperty()
    student_cs = StringProperty()
    time_in = StringProperty()
    time_out = StringProperty()
    student_temperature = StringProperty()

    def on_enter(self):

        if len(scanned_student_names) != 0:
            num = str(scanned_student_names[0][0])
            name = str(scanned_student_names[0][1])
            temp = str(scanned_student_names[0][6])
            ti = str(scanned_student_names[0][8])
            self.student_number = num
            self.student_name = name
            self.student_temperature = temp
            self.time_in = ti
        else:
            self.student_number = "000000000"
            self.student_name = "------"
            self.student_cs = "------"
            self.student_temperature = "--"
            self.time_in = "00:00:00"
            self.time_out = "00:00:00"

    def scan(self):

        cap = cv2.VideoCapture(0)
        
        names=[]
    
        def checkData(data):
            data=str(data)    
            if data in names:
                pass
                print('Already Scanned')
            else:
                winsound.Beep(frequency, duration)
                print(data)
                names.append(data)
                new_z = data[2:-1]
                split_info = new_z.split(';')
                scanned_student_names.append(split_info)
      
        while True:
            _, frame = cap.read() 
            decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                checkData(obj.data)
                time.sleep(1)
           
            cv2.imshow("Frame", frame)

            if cv2.waitKey(1)& 0xFF == ord('s'):
                cv2.destroyAllWindows()
                break
        
        print(scanned_student_names)
        app = MDApp.get_running_app()
        app.show_screen("about_app")
        app.show_screen("home_screen")

        # time.sleep(3)
        HomeScreen.refresh(self)

    # def try1(self):
    #     if len(scanned_student_names) != 0:
    #         num = str(scanned_student_names[0][0])
    #         # print(num)
    #         # HomeScreen.refresh(self)
    #         self.ids.home_screen.stud_num.clear()
    #         return num
    #     else:
    #         num = '000000000'
    #         return num