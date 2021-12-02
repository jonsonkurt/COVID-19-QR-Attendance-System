from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.toast.kivytoast import toast
from kivy.uix.screenmanager import Screen
from libs.baseclass import user_key, class_key
import sqlite3
from kivy.clock import Clock
from openpyxl import *
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.utils import asynckivy
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty

Builder.load_file('./libs/kv/homescreen.kv')

class HomeScreen(Screen):
    pass