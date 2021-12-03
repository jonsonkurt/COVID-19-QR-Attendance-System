# Sets the window size
from kivy.config import Config
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty

from libs.baseclass import login, navigation_layout, homescreen, about, help

# this class serves as the main class that runs the system
class MyApp(MDApp):
    title="QR Code-Based Attendance System"

    current_index = NumericProperty()

    def show_screen(self, name):

        self.root.current = 'nav_screen'
        self.root.get_screen('nav_screen').ids.manage.current = name
        return True

    def build(self):

        self.icon = 'qr_attendance.ico'
        #self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Blue"
        # self.theme_cls.accent_palette = "Blue"
        screen = Builder.load_file("main.kv")
        return screen

if __name__ == '__main__':
    MyApp().run()