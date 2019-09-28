from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import datetime
import win32gui
import win32con
import win32api


class ReadOnSpeedApp(App):

    def callbackWriteText(self, label):
        self.i=self.i+1
        label.text = '[size=32][color=ff3333]Hello[/color] [color=3333ff]World[/color][/size][size=62]' + str(self.i) + '[/size]'  #datetime.datetime.now()
    
    # Set alpha between 0 and 1. 0 no opacity, 1 invisible
    def makeItTransparent(self, alpha):
        alpha = int((1-alpha) * 255)
        handle = win32gui.FindWindow(None, "ReadOnSpeedApp")
        # Make it a layered window
        win32gui.SetWindowLong(handle, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(handle, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # make it transparent (alpha between 0 and 255)
        win32gui.SetLayeredWindowAttributes(handle, win32api.RGB(0, 0, 0), alpha, win32con.LWA_ALPHA)
        
    def build(self):
        self.i = 0
        label = Label(text='Init', markup=True)
        #Clock.schedule_once(lambda dt: self.show_marks(label), 1)
        Clock.schedule_interval(lambda dt: self.callbackWriteText(label), 0.001)
        Clock.schedule_once(lambda dt: self.makeItTransparent(alpha=0.2), 0.1)
        # Get the window
        
        return label

ReadOnSpeed().run()

exit()
# hello world text
l = Label(text='Hello world')

# unicode text; can only display glyphs that are available in the font
l = Label(text=u'Hello world ' + unichr(2764))

# multiline text
l = Label(text='Multi\nLine')

# size
l = Label(text='Hello world', font_size='20sp')