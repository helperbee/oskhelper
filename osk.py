import ctypes
import time
from ctypes import wintypes


DEBUG_PRINT = True
#AUTO_OSK = True #Opens OSK if it's not currently open. cba

WM_PARENTNOTIFY = 0x0210
WM_MOUSEACTIVATE = 0x0021
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
HTCLIENT = 1  
MAX_CLASS_NAME = 256

WM_GETMINMAXINFO = 0x0024
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004

EnumWindows = ctypes.windll.user32.EnumWindows
EnumChildWindows = ctypes.windll.user32.EnumChildWindows
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetClassName = ctypes.windll.user32.GetClassNameW
SendMessageW = ctypes.windll.user32.SendMessageW
PostMessageW = ctypes.windll.user32.PostMessageW
SetWindowPos = ctypes.windll.user32.SetWindowPos

def enum_windows_proc(hwnd, lParam):
    buffer = wintypes.WCHAR * 256
    wnd_caption = buffer()
    GetWindowText(hwnd, wnd_caption, 256)
    if wnd_caption.value == "On-Screen Keyboard":
        class_name = buffer()
        GetClassName(hwnd, class_name, 256)
        if class_name.value == "OSKMainClass":
            ctypes.cast(lParam, ctypes.POINTER(wintypes.HWND))[0] = hwnd
            return False
    return True

def find_osk_window():
    hwnd = wintypes.HWND()
    lParam = ctypes.pointer(hwnd)
    EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)(enum_windows_proc), lParam)
    return hwnd.value

def enum_child_windows_proc(hwnd, lParam):
    child_windows.append(hwnd)
    class_name = wintypes.CHAR * MAX_CLASS_NAME
    wnd_class = class_name()
    GetClassName(hwnd, wnd_class, MAX_CLASS_NAME)
    class_name_str = wnd_class.value.decode('utf-8')
    child_window_info.append((hwnd, class_name_str))
    return True

def get_child_windows(parent_hwnd):
    global child_windows
    global child_window_info
    child_windows = []
    child_window_info = []
    EnumChildWindows(parent_hwnd, ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)(enum_child_windows_proc), 0)
    return child_window_info

def pprint(str):
    if DEBUG_PRINT:
        print(str)

def key_press(key):
    osk_hwnd = find_osk_window()
    if key not in Keys:
        print('Key not supported add it yourself.')
        return
    key = Keys[key]
    if not osk_hwnd:
        pprint("OSK window not found. Please open OSK if you'd like to use this functionality")
        return

    child_windows_info = get_child_windows(osk_hwnd)
    if not child_windows_info:
        pprint("No child windows found.")
        return

    child_hwnd, _ = child_windows_info[0]



    pprint(f'\'{key.key}\' key is being pressed.')
    lParamMouseActivate = (HTCLIENT << 16) | (WM_LBUTTONDOWN & 0xFFFF)
    SendMessageW(child_hwnd, WM_MOUSEACTIVATE, child_hwnd, lParamMouseActivate)

    lParam = (key.y << 16) | (key.x & 0xFFFF)

    PostMessageW(child_hwnd, WM_LBUTTONDOWN, 0, lParam)
    time.sleep(0.1)
    PostMessageW(child_hwnd, WM_LBUTTONUP, 0, lParam)

class Key:
    def __init__(self, key, x, y):
        self.key = key
        self.x = x
        self.y = y
Keys = {}

Keys['esc'] = Key("escape", 10, 36)
Keys['`'] = Key("`", 35, 36)
Keys['1'] = Key("1", 60, 36)
Keys['2'] = Key("2", 85, 36)
Keys['3'] = Key("3", 105, 36)
Keys['4'] = Key("4", 126, 36)
Keys['5'] = Key("5", 146, 36)
Keys['6'] = Key("6", 166, 36)
Keys['7'] = Key("7", 186, 36)
Keys['8'] = Key("8", 206, 36)
Keys['9'] = Key("9", 226, 36)
Keys['0'] = Key("0", 246, 36)
Keys['-'] = Key("hyphen", 266, 36)
Keys['='] = Key("equals", 286, 36)
Keys['backspace'] = Key("backspace", 316, 36)


Keys['tab'] = Key("tab", 15, 57)
Keys['q'] = Key("q", 45, 57)
Keys['w'] = Key("w", 65, 57)
Keys['e'] = Key("e", 85, 57)
Keys['r'] = Key("r", 105, 57)
Keys['t'] = Key("t", 125, 57)
Keys['y'] = Key("y", 145, 57)
Keys['u'] = Key("u", 165, 57)
Keys['i'] = Key("i", 185, 57)
Keys['o'] = Key("o", 215, 57)
Keys['p'] = Key("p", 240, 57)
Keys['['] = Key("[", 270, 57)
Keys[']'] = Key("]", 285, 57)
Keys['\\'] = Key("\\", 305, 57)
Keys['del'] = Key("del", 327, 58)

    
Keys['a'] = Key("a", 55, 79)
Keys['s'] = Key("s", 75, 79)
Keys['d'] = Key("d", 95, 79)
Keys['f'] = Key("f", 115, 79)
Keys['g'] = Key("g", 135, 79)
Keys['h'] = Key("h", 160, 79)
Keys['j'] = Key("j", 180, 79)
Keys['k'] = Key("k", 205, 79)
Keys['l'] = Key("l", 230, 79)
Keys[';'] = Key("semicolon", 255, 79)
Keys['\''] = Key("apostrophe", 280, 79)
Keys['enter'] = Key("enter", 315, 79)


Keys['z'] = Key("z", 66, 100)
Keys['x'] = Key("x", 86, 100)
Keys['c'] = Key("c", 106, 100)
Keys['v'] = Key("v", 126, 100)
Keys['b'] = Key("b", 151, 100)
Keys['n'] = Key("n", 177, 100)
Keys['m'] = Key("m", 200, 100)
Keys[','] = Key(",", 223, 100)
Keys['.'] = Key(".", 246, 100)
Keys['/'] = Key("/", 265, 100)


def write(line):
    for l in line:
        if l in Keys:
            key_press(Keys[l])
        else:
            pprint(f"'{l}' key isnt supported currently.")


if __name__ == "__main__":
    time.sleep(2)
    #try to ensure the dimensions match the predefined key coordinates
    new_width = 100 #smaller than possible but this is fine
    new_height = 100
    SetWindowPos(find_osk_window(), None, 0, 0, new_width, new_height, SWP_NOMOVE | SWP_NOZORDER)

    #write('`1234567890-=')
    #write('asdfghjkl;\'')
    #write('qwertyuiop[]\\')
    #write('zxcvbnm,./')
    key_press('esc')
