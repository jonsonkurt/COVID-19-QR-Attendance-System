from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.toast.kivytoast import toast
from kivy.uix.screenmanager import Screen
from libs.baseclass import user_key, class_key
import sqlite3
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty
from datetime import date, datetime
import winsound

Builder.load_file('./libs/kv/homescreen.kv')

scanned_student_names = [""]
scanned_student_names2 = [""]
scanned_student_names3 = [""]

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

        if scanned == scanned_student_names[-1]:
            pass
        if scanned == "":
            pass
        else:
            scanned_student_names.append(scanned)
            new_z = scanned[2:-1]
            split_info = new_z.split(';')
            if split_info != scanned_student_names2[-1]:
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
            if scanned_student_names2[-1] != scanned_student_names3[-1] and scanned_student_names2[-1] not in scanned_student_names3:
                scanned_student_names3.append(scanned_student_names2[-1])
                num = str(scanned_student_names3[-1][0])
                temp = str(scanned_student_names3[-1][6])
                ti = str(scanned_student_names3[-1][8])
                self.time_out = "00:00:00"
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
                    time_in VARCHAR(30),
                    time_out VARCHAR(30))""")
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
            elif scanned_student_names2[-1] != scanned_student_names3[-1] and scanned_student_names2[-1] in scanned_student_names3:
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
                now = datetime.now()
                to = str(now.strftime("%H:%M:%S"))
                self.qr_day = day
                self.time_in = ti
                self.time_out = to

                conn = sqlite3.connect("mybase.db")
                cur = conn.cursor()
                find = ("SELECT * FROM student_list WHERE student_number = ?")
                cur.execute(find, [(self.student_number)])
                results = cur.fetchall()

                self.student_cs = str(results[0][2])
                student_key = results[0][0]
                self.student_name = results[0][1]
                student_contact = results[0][4]

                cur.execute('UPDATE present_students SET time_out=? WHERE student_number=?', (self.time_out, self.student_number))
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
