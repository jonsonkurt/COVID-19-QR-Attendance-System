import sqlite3
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast.kivytoast import toast

Builder.load_file('./libs/kv/login.kv')

class LoginScreen(Screen):
    # this function handles the logins of users by getting username and password
    def do_login(self, usernametext, passwordtext):
    
        useri = usernametext
        passwd = passwordtext
        conn = sqlite3.connect("mybase.db")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS accounts(account_id integer PRIMARY KEY, email_add VARCHAR(30), pass VARCHAR(30))")
        cur.execute("SELECT * FROM accounts")
        cur.fetchall()

        if(len(useri) > 0 and len(passwd) > 0):
            find = ("SELECT * FROM accounts WHERE email_add = ? AND pass = ?")
            cur.execute(find, [(useri), (passwd)])
            results=cur.fetchall()

            if results:
                for i in results:
                    key = i[0]
                    app = MDApp.get_running_app()
                    self.manager.transition.direction = "left"
                    self.manager.transition.duration = 0.5
                    app.show_screen("home_screen")
                    toast('Success. Start scanning !')
            else:
                return toast('Please enter correct email and password.')
        else:
            return toast('Please enter email and password.')

        conn.close()

        self.ids['username'].text = ""
        self.ids['password'].text = ""
