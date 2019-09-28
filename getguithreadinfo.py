import ctypes

################ Winapi simple types ##############

DWORD = ctypes.c_ulong # typedef unsigned long DWORD; (32bit unsigned)
                       # typedef void *PVOID;
                       # typedef PVOID HANDLE;
HWND = ctypes.c_void_p # typedef HANDLE HWND;
LONG = ctypes.c_long   # typedef long LONG; (32bit signed)


WORD = ctypes.c_ushort
ULONG_PTR = ctypes.POINTER(DWORD)

#########################################################
################ Structs GetGUIThreadInfo  ##############

#typedef struct tagRECT {
#  LONG left;
#  LONG top;
#  LONG right;
#  LONG bottom;
#} RECT, *PRECT, *NPRECT, *LPRECT;

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", LONG),
        ("top", LONG),
        ("right", LONG),
        ("bottom", LONG)
    ]
#typedef struct tagGUITHREADINFO {
#  DWORD cbSize;
#  DWORD flags;
#  HWND  hwndActive;
#  HWND  hwndFocus;
#  HWND  hwndCapture;
#  HWND  hwndMenuOwner;
#  HWND  hwndMoveSize;
#  HWND  hwndCaret;
#  RECT  rcCaret;
#} GUITHREADINFO, *PGUITHREADINFO, *LPGUITHREADINFO;

class GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("flags", DWORD),
        ("hwndActive", HWND),
        ("hwndFocus", HWND),
        ("hwndCapture", HWND),
        ("hwndMenuOwner", HWND),
        ("hwndMoveSize", HWND),
        ("hwndCaret", HWND),
        ("rcCaret", RECT)
        ]
PGUITHREADINFO = ctypes.POINTER(GUITHREADINFO)

#BOOL GetGUIThreadInfo(
#  DWORD          idThread,
#  PGUITHREADINFO pgui
#);
fGetGUIThreadInfo = ctypes.windll.user32.GetGUIThreadInfo
fGetGUIThreadInfo.restype = ctypes.c_bool
fGetGUIThreadInfo.argtypes = [ctypes.c_ulong, PGUITHREADINFO]

def GetGUIThreadInfo():
    gui = GUITHREADINFO(cbSize=ctypes.sizeof(GUITHREADINFO))
    if not fGetGUIThreadInfo(0, ctypes.byref(gui)):
        err_no = ctypes.GetLastError()
        raise WindowsError(err_no, ctypes.FormatError(err_no))
    return {
        "flags": gui.flags,
        "hwndActive": gui.hwndActive,
        "hwndFocus": gui.hwndFocus,
        "hwndCapture": gui.hwndCapture,
        "hwndMenuOwner": gui.hwndMenuOwner,
        "hwndMoveSize": gui.hwndMoveSize,
        "hwndCaret": gui.hwndCaret,
        "rcCaret": [gui.rcCaret.left, gui.rcCaret.top, gui.rcCaret.right, gui.rcCaret.bottom]
    }