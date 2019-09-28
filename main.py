#!/usr/bin/env python

from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.logger import Logger
import datetime
import win32gui
import win32con
import win32api
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
import random
from kivy.config import Config
import win32com.client
Config.set('graphics', 'fullscreen', 'fake')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '300')
Config.set('graphics', 'left', '300')


from main_spritz import fastReader
import sys
import fileinput

from mouseInterfaces import start_mouse_event_listener_thread, time_message, velocity

class MyBackground(Widget):
    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        with self.canvas:
            self.bg = Rectangle(source='water.png', pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)
        self.layout = AnchorLayout(anchor_x='center', anchor_y='center')

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

class TDE(Widget):  # Text display engine
    def __init__(self, **kwargs):
        super(TDE, self).__init__(**kwargs)
        with self.canvas:
            Color(0, 0, 0, 0)  # green; colors range from 0-1 instead of 0-255
            pos_hint = {'center_x': .5, 'center_y': .5}
            self.pos = self.center_x - 50, self.center_y - 50
            self.rect = Rectangle(pos=self.pos, size=self.size)
            self.outTxt = Label(text='Init', markup=True, pos_hint={'center_x':.5, 'center_y':.5})
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.i = 0


        article = ""
        for line in fileinput.input("dummy_long.txt", openhook=fileinput.hook_encoded("utf-8")):
            article += line #to_unicode

        self.reader = fastReader()
        self.reader.prepareNewText(article)
        self.reader.setWheelSpeed(900)
        self.nextValidCall = 0
        self.time_last_scroll_event = 0
        self.is_scrolling = False


    def _update_rect(self):
        self.rect.size = self.parent.size
        self.outTxt.pos = self.parent.center
        self.outTxt.pos_hint={'center_x':.5, 'center_y':.5}
    
    def setToMiddle(self):
        self.rect.size = self.parent.size
        self.outTxt.pos = self.parent.center
        self.outTxt.pos_hint = {'center_x': .5, 'center_y': .5}

    def callbackWriteText(self, label):
        self.i=self.i+1
        if self.is_scrolling:
            if time_message - self.time_last_scroll_event < 0.03:
                Logger.info("Scroll: Scrolling stopped")
                self.is_scrolling = False
        else:
            if time_message != self.time_last_scroll_event:
                Logger.info("Scroll: Scrolling started")
                self.is_scrolling = True
        self.time_last_scroll_event = time_message

        if self.i > self.nextValidCall:
            (word, durationInSec) = self.reader.getNextWord()
            self.outTxt.text = '[size=32][color=000000][font=RobotoMono-Regular]'+word+'[/font][/color][/size]'  #datetime.datetime.now()
            self.nextValidCall=self.i+durationInSec*1000
        self.setToMiddle()



class ReadOnSpeedApp(App):

    def callbackWriteText(self, label):
        self.i=self.i+1
        label.text = '[size=32][color=ff3333]Hello[/color] [color=3333ff]World[/color][/size][size=62]' + str(self.i) + '[/size]'  #datetime.datetime.now()
        self.textGen.callbackWriteText(label)
    # Set alpha between 0 and 1. 0 no opacity, 1 invisible
    def makeItTransparent(self, alpha):
        alpha = int((1-alpha) * 255)
        handle = win32gui.FindWindow(None, "ReadOnSpeedApp")
        # Make it a layered window
        win32gui.SetWindowLong(handle, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(handle, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # make it transparent (alpha between 0 and 255)
        win32gui.SetLayeredWindowAttributes(handle, win32api.RGB(0, 0, 0), alpha, win32con.LWA_ALPHA)
    
    def makeItForeground(self):
        handle = win32gui.FindWindow(None, "ReadOnSpeedApp")
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(handle)

    def PositionToMouse(self):
        handle = win32gui.FindWindow(None, "ReadOnSpeedApp")
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        flags, hcursor, (x,y) = win32gui.GetCursorInfo()
        win32gui.SetWindowPos(handle, win32con.HWND_TOP, x-250, y-210, 500, 200, win32con.SWP_SHOWWINDOW)

    def build(self):
        ##Experiment
        parent = MyBackground()
        ##Exp End

        self.i = 0
        label = Label(text='Init', markup=True)
        self.title = 'ReadOnSpeedApp'
        
        # Creating all the necessary timers and so on


        self.textGen = TDE()
        parent.add_widget(self.textGen)

        Clock.schedule_interval(lambda dt: self.callbackWriteText(label), 0.001)
        Clock.schedule_once(lambda dt: self.makeItTransparent(alpha=0.0), 0.1)
        Clock.schedule_once(lambda dt: self.textGen.setToMiddle(), 0.2)
        Clock.schedule_interval(lambda dt: self.PositionToMouse(),0.1)
        # Get the window
        return parent


start_mouse_event_listener_thread()

try:
    ReadOnSpeedApp().run()
except KeyboardInterrupt:
    Logger.info("main: Ctrl+C detected. Terminate!")


exit()
# hello world text
l = Label(text='Hello world')

# unicode text; can only display glyphs that are available in the font
l = Label(text=u'Hello world ' + unichr(2764))

# multiline text
l = Label(text='Multi\nLine')

# size
l = Label(text='Hello world', font_size='20sp')



btn = Button(text='Hello World')
layout.add_widget(btn)