import cv2
import sqlite3
import pyzbar.pyzbar as pyzbar
import time

scanned_student_names = []


class ScanScreen:

    def save_scanned(self):

        scanned = self.ids.scanned_name.text2

        if scanned in scanned_student_names:
            pass
        else:
            split_info = scanned.split(';')
            scanned_student_names.append(split_info)

    def scanner(self):

        cap = cv2.VideoCapture(0)
        
        names=[]
        def enterData(z):
            if z in names:
                pass
            else:
                new_z = z[2:-1]
                split_info = new_z.split(';')
                names.append(split_info)
    
        print('Reading...')
    
        def checkData(data):
            data=str(data)    
            if data in names:
                print('Already Present')
            else:
                print(data)
                enterData(data)
      
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
        
        print(names)

    # def scan(self):

    #     conn = sqlite3.connect("mybase.db")
    #     cur = conn.cursor()
        
    #     names = scanned_student_names

    #     final_names = []

    #     for items in names:
    #         a = names.index(items)
    #         b = len(items)
    #         items = items[2:(b-1)]
    #         final_names.append(items)

    #     final_names.sort()

    #     final_names2 = []

    #     for i in final_names:
    #         cname = i
    #         find = ("SELECT * FROM students WHERE student_name=? AND class_id=?")
    #         cur.execute(find,(cname,section))
    #         results = cur.fetchall()
    #         if results:
    #             s = final_names.index(i)
    #             final_names2.append(final_names[s])
    #         else:
    #             continue

    #     for names in final_names2:
    #         cur.execute('UPDATE students SET status_attendance=? WHERE class_id=? AND student_name=?', (state, section, names))
    #         conn.commit()

    #     scanned_student_names.clear()

x = ScanScreen()
x.scanner()
