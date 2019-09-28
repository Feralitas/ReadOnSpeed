
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
import time

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
    old_clipboard_text = GetClipboardData( CF_UNICODETEXT );
    CloseClipboard();



    SendInput(Keyboard(VK_CONTROL),
              Keyboard(KEY_C))
    time.sleep(0.1)
    SendInput(Keyboard(VK_CONTROL, KEYEVENTF_KEYUP),
              Keyboard(KEY_C, KEYEVENTF_KEYUP))
    time.sleep(0.1)


    OpenClipboard()
    selected_text = GetClipboardData( CF_UNICODETEXT )
    SetClipboardData(CF_UNICODETEXT, old_clipboard_text)
    CloseClipboard();

    return selected_text


if __name__ == '__main__':
    print("Change to another window with selected text.")
    time.sleep(3)
    print(get_selected_text())
    print(get_handle_of_focused_window())

