from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.toast.kivytoast import toast
from kivy.lang.builder import Builder
import sqlite3

Builder.load_file('./libs/kv/add_student.kv')

class AddStudent(BoxLayout):

    # This function lets user to add new class
    def save_student(self, name, section, stud_num, contact):

        student_name = name
        course_section = section
        student_number = stud_num
        contact_number = contact


        if student_name == "" and course_section == "" and student_number == "" and contact_number == "":
            return toast('Please fill up the text fields.')
        elif student_name == "":
            return toast('Enter student name.')
        elif course_section == "":
            return toast('Enter course and section.')
        elif student_number == "":
            return toast('Enter student number.')
        elif contact_number == "":
            return toast('Enter contact number.')
        else:
            conn = sqlite3.connect("mybase.db")
            cur = conn.cursor()

            cur.execute("""CREATE TABLE IF NOT EXISTS student_list(
                stud_id INTEGER PRIMARY KEY, 
                full_name TEXT, 
                course_section TEXT, 
                student_number INTEGER, 
                contact_number INTEGER)""")
            cur.execute("""INSERT INTO student_list(
                full_name, 
                course_section, 
                student_number, 
                contact_number) VALUES(?,?,?,?)""", 
                (student_name.upper(), course_section.upper(), int(student_number), int(contact_number)))

            conn.commit()
            conn.close()

            self.ids['student_name'].text = ""
            self.ids['section_name'].text = ""
            self.ids['student_num'].text = ""
            self.ids['contact_num'].text = ""

            return toast('Student has been added to the list.')

def add_student_dialog(self):
    self.dialog1 = None
    if not self.dialog1:
        self.dialog1 = MDDialog(
            title="Add a Student:",
            type="custom",
            content_cls=AddStudent(),
        )
    self.dialog1.open()
