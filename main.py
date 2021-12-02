# Sets the window size
from kivy.config import Config
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty

from libs.baseclass import login, navigation_layout

colors = {
    "Teal": {
        "50": "07575B",
        "100": "07575B",
        "200": "07575B",
        "300": "07575B",
        "400": "07575B",
        "500": "07575B",
        "600": "07575B",
        "700": "07575B",
        "800": "07575B",
        "900": "07575B",
        "A100": "07575B",
        "A200": "07575B",
        "A400": "07575B",
        "A700": "07575B",
    },
    "Blue": {
        "50": "e3f3f8",
        "100": "b9e1ee",
        "200": "91cee3",
        "300": "72bad6",
        "400": "62acce",
        "500": "589fc6",
        "600": "5191b8",
        "700": "487fa5",
        "800": "426f91",
        "900": "35506d",
        "A100": "b9e1ee",
        "A200": "91cee3",
        "A400": "62acce",
        "A700": "487fa5",
}
}


# this class serves as the main class that runs the system
class MyApp(MDApp):
    title="QR Code-Based Attendance System"

    current_index = NumericProperty()

    def show_screen(self, name):

        self.root.current = 'nav_screen'
        self.root.get_screen('nav_screen').ids.manage.current = name
        return True

    def build(self):

        #self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Teal"
        # self.theme_cls.accent_palette = "Blue"
        screen = Builder.load_file("main.kv")
        return screen

if __name__ == '__main__':
    MyApp().run()