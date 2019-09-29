
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
import time

from kivy.logger import Logger
from sendinput import SendInput, Keyboard, VK_CONTROL, KEY_C, KEYEVENTF_KEYUP
from getguithreadinfo import GetGUIThreadInfo
from win32clipboard import OpenClipboard, GetClipboardData, CloseClipboard, SetClipboardData, CF_TEXT, CF_UNICODETEXT

def get_handle_of_focused_window() -> int:

    a = GetGUIThreadInfo()

    #print("hwndActive", gui.hwndActive)
    #print("hwndFocus", gui.hwndFocus)
    #print("hwndCapture", gui.hwndCapture)
    #print("hwndMenuOwner", gui.hwndMenuOwner)
    #print("hwndMoveSize", gui.hwndMoveSize)
    #print("hwndCaret", gui.hwndCaret)
    return a["hwndFocus"]


def get_selected_text() -> str:
    OpenClipboard()
    old_clipboard_text = GetClipboardData( CF_TEXT);
    old_clipboard_text_unicode = old_clipboard_text.decode("utf-8", "replace")
    CloseClipboard()
    #Logger.info(f"Clip Old: {old_clipboard_text_unicode[0:20]}")



    SendInput(Keyboard(VK_CONTROL))
    time.sleep(0.1)
    SendInput(Keyboard(KEY_C))
    time.sleep(0.1)
    SendInput(Keyboard(VK_CONTROL, KEYEVENTF_KEYUP))
    time.sleep(0.1)
    SendInput(Keyboard(KEY_C, KEYEVENTF_KEYUP))
    time.sleep(0.1)


    OpenClipboard()
    selected_text = GetClipboardData(CF_TEXT)
    SetClipboardData(CF_TEXT, old_clipboard_text)
    CloseClipboard()
    selected_text_unicode = selected_text.decode("utf-8", "replace")
    #Logger.info(f"Clip New: {selected_text_unicode[0:20]}")

    return selected_text_unicode


if __name__ == '__main__':
    print("Change to another window with selected text.")
    time.sleep(3)
    print(get_selected_text())
    print(get_handle_of_focused_window())

