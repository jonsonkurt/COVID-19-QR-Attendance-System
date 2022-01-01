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
from datetime import date
import winsound

Builder.load_file('./libs/kv/homescreen.kv')

scanned_student_names = []
scanned_student_names2 = []
scanned_student_names3 = []

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second

class HomeScreen(Screen):

    student_number = StringProperty()
    student_pic = StringProperty()
    student_name = StringProperty()
    student_cs = StringProperty()
    qr_day = StringProperty()
    time_in = StringProperty()
    time_out = StringProperty()
    student_temperature = StringProperty()

    qr_text = StringProperty()

    # this function prevent scanning duplicate student QR code
    def save_scanned(self):

        scanned = self.ids.scanned_name.text2

        if scanned in scanned_student_names:
            pass
        if scanned == "":
            pass
        else:
            scanned_student_names.append(scanned)
            new_z = scanned[2:-1]
            split_info = new_z.split(';')
            if split_info not in scanned_student_names2:
                scanned_student_names2.append(split_info)

                app = MDApp.get_running_app()
                app.show_screen("blank")
                app.show_screen("home_screen")
                winsound.Beep(frequency, duration)
            else:
                toast('Already Scanned')

            print(scanned_student_names2)

    def on_enter(self):

        if len(scanned_student_names2) != 0:
            if scanned_student_names2[-1] not in scanned_student_names3:
                scanned_student_names3.append(scanned_student_names2[-1])
                num = str(scanned_student_names3[-1][0])
                temp = str(scanned_student_names3[-1][6])
                ti = str(scanned_student_names3[-1][8])
                self.student_number = num
                self.student_pic = num
                self.student_temperature = temp
                today = date.today()
                day = today.strftime("%A, %B %d, %Y")
                day2 = today.strftime("%B %d, %Y")
                self.qr_day = day
                self.time_in = ti

                conn = sqlite3.connect("mybase.db")
                cur = conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS student_list(stud_id INTEGER PRIMARY KEY, full_name TEXT, course_section TEXT, student_number INTEGER, contact_number INTEGER)")
                find = ("SELECT * FROM student_list WHERE student_number = ?")
                cur.execute(find, [(self.student_number)])
                results = cur.fetchall()

                self.student_cs = str(results[0][2])
                student_key = results[0][0]
                self.student_name = results[0][1]
                student_contact = results[0][4]

                cur.execute("""CREATE TABLE IF NOT EXISTS present_students(
                    stud_id INTEGER, 
                    full_name TEXT, 
                    course_section TEXT, 
                    student_number INTEGER, 
                    contact_number INTEGER,
                    attendance_day  VARCHAR(30),
                    time_in VARCHAR(30))""")
                cur.execute(
                    """INSERT INTO present_students(
                        stud_id, 
                        full_name, 
                        course_section, 
                        student_number, 
                        contact_number,
                        attendance_day, 
                        time_in) 
                        VALUES(?,?,?,?,?,?,?)""", 
                    (student_key, self.student_name, self.student_cs, self.student_number, student_contact, day2, self.time_in))
                conn.commit()
                conn.close()
            else:
                toast('Already Scanned')

        else:
            self.student_number = "000000000"
            self.student_pic = "Student_Vector"
            self.student_name = "------"
            self.student_cs = "------"
            self.student_temperature = "--"
            self.qr_day = "---"
            self.time_in = "00:00:00"
            self.time_out = "00:00:00"

    # def scan(self):

    #     cap = cv2.VideoCapture(0)
        
    #     names=[]
    
    #     def checkData(data):
    #         data=str(data)    
    #         if data in names:
    #             pass
    #             print('Already Scanned')
    #         else:
    #             winsound.Beep(frequency, duration)
    #             print(data)
    #             names.append(data)
    #             new_z = data[2:-1]
    #             split_info = new_z.split(';')
    #             scanned_student_names.append(split_info)
      
    #     while True:
    #         _, frame = cap.read() 
    #         decodedObjects = pyzbar.decode(frame)
    #         for obj in decodedObjects:
    #             checkData(obj.data)
    #             time.sleep(1)
           
    #         cv2.imshow("Frame", frame)

    #         if cv2.waitKey(1)& 0xFF == ord('s'):
    #             cv2.destroyAllWindows()
    #             break

    #     print(scanned_student_names)
    #     app = MDApp.get_running_app()
    #     app.show_screen("about_app")
    #     app.show_screen("home_screen")

        # time.sleep(3)
        # HomeScreen.refresh(self)

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