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
Config.set('graphics', 'borderless', 'true')
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
        if len(sys.argv) > 1:
            self.reader.setWheelSpeed(int(sys.argv[1]))
        else:
            self.reader.setWheelSpeed(300)
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
            if len(word) > 0:
                self.outTxt.text = '[size=32][color=000000][font=RobotoMono-Regular]'+word+'[/font][/color][/size]'  #datetime.datetime.now()
            self.nextValidCall=self.i+durationInSec*1000
        self.setToMiddle()



class ReadOnSpeedApp(App):

    def callbackWriteText(self, label):
        if self.StatusOfApp == 1:
            self.textGen.callbackWriteText(label)
    
    def getHandleOfThisWindow(self):
        if self.handle == 0:
            self.handle = win32gui.FindWindow(None, "ReadOnSpeedApp")
        return self.handle

    def makeItTransparent(self, alpha):# Set alpha between 0 and 1. 0 no opacity, 1 invisible
        alpha = int((1-alpha) * 255)
        win32gui.SetWindowLong(self.getHandleOfThisWindow(), win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.getHandleOfThisWindow(), win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)   # Make it a layered window
        win32gui.SetLayeredWindowAttributes(self.getHandleOfThisWindow(), win32api.RGB(0, 0, 0), alpha, win32con.LWA_ALPHA)        # make it transparent (alpha between 0 and 255)
    
    def makeItForeground(self):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(self.getHandleOfThisWindow())

    def PositionToMouse(self):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        flags, hcursor, (x,y) = win32gui.GetCursorInfo()
        win32gui.SetWindowPos(self.getHandleOfThisWindow(), win32con.HWND_TOP, x - 250, y - 210, 500, 200, win32con.SWP_SHOWWINDOW)
        self.makeItForeground()
    
    def hibernate(self):
        win32gui.ShowWindow(self.getHandleOfThisWindow(), 0)
        self.StatusOfApp = 0

    def startUp(self):
        win32gui.ShowWindow(self.getHandleOfThisWindow(),1)
        self.PositionToMouse()
        self.makeItTransparent(.2)
        self.StatusOfApp = 1

    def waitForWakeUpCall(self):
        if self.StatusOfApp == 0:
            wakeUpKey = {
           0x10: 'shift',
           0x20: 'space'}
            for i in range(1, 256):
                if win32api.GetAsyncKeyState(i):
                    if i in wakeUpKey:
                        self.startUp()
        if self.StatusOfApp == 1:
            shutDownKey = {
           0x10: 'shift',
           0x20: 'space'}
            for i in range(1, 256):
                if win32api.GetAsyncKeyState(i):
                    if i in shutDownKey:
                        self.hibernate()



    def build(self):
        ##Experiment
        self.handle = 0  #init
        self.StatusOfApp = 0
        parent = MyBackground()
        ##Exp End

        self.i = 0
        label = Label(text='Init', markup=True)
        self.title = 'ReadOnSpeedApp'
        
        # Creating all the necessary timers and so on


        self.textGen = TDE()
        parent.add_widget(self.textGen)

        Clock.schedule_interval(lambda dt: self.callbackWriteText(label), 0.001)
        Clock.schedule_once(lambda dt: self.hibernate(), 0.2) # initialiying the hibernate after start up
        Clock.schedule_interval(lambda dt: self.waitForWakeUpCall(),0.1) #This loop is always listening for a wake up or suspend.
        # Get the window
        return parent


start_mouse_event_listener_thread()

try:
    ReadOnSpeedApp().run()
except KeyboardInterrupt:
    Logger.info("main: Ctrl+C detected. Terminate!")

exit()