from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.toast.kivytoast import toast
from xlsxwriter.workbook import Workbook
from datetime import date
import sqlite3

def export_dialog(self):
    self.dialog1 = None
    if not self.dialog1:
        self.dialog1 = MDDialog(
            title="Export Attendance to Excel?",
            text="Exporting the attendance record for this day to excel will reset the current attendance list. Are you sure you want to proceed?",
            buttons=[
                MDFillRoundFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    md_bg_color='#f5f5f5',
                    text_color='#07575B',
                    on_release=lambda x:self.dialog1.dismiss()
                ),
                MDFillRoundFlatButton(
                    text="Proceed",
                    theme_text_color="Custom",
                    md_bg_color='#07575B',
                    text_color='#FFFFFF',
                    on_release=lambda x:export_to_excel(self)
                ),
            ],
        )
    self.dialog1.open() 

    def export_to_excel(self):
    
        conn = sqlite3.connect("mybase.db")
        curr = conn.cursor()

        title = str(date.today()) + "-Attendance-Record" + ".xlsx"
        workbook = Workbook(title)
        worksheet = workbook.add_worksheet()

        mysel = curr.execute("""SELECT 
                            full_name, 
                            course_section,
                            student_number,
                            contact_number,
                            time_in
                            FROM present_students 
                            ORDER BY course_section, full_name ASC""")

        result2 = curr.fetchall()
        
        text_format = workbook.add_format({'bold': True, 'align': 'center'})
        text_format2 = workbook.add_format({'align': 'center'})

        worksheet.set_column(0, 0, 35)
        worksheet.set_column(1, 1, 25)
        worksheet.set_column(2, 3, 20)
        worksheet.set_column(4, 4, 10)

        worksheet.write('A1', 'Student Name', text_format)
        worksheet.write('B1', 'Course and Section', text_format)
        worksheet.write('C1', 'Student Number', text_format)
        worksheet.write('D1', 'Contact Number', text_format)
        worksheet.write('E1', 'Time In', text_format)
        
        for i, row in enumerate(result2, 1):
            for j, value in enumerate(row):
                worksheet.write(i, j, value, text_format2)
        
        workbook.close()

        curr.execute("DELETE FROM present_students")
        conn.commit()

        conn.close()
        self.dialog1.dismiss()
        toast('Attendance record exported.')
