import win32gui
import win32con
from windowSniffer import windowSniffer

def focus(hwnd):
    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        return True
    except Exception as e:
        print(f"Friday: couldnt focus window: {e}")
        return False
    
def find(app):
    windows = windowSniffer()#retrieve window list
    for window in windows:
        if app.lower() in window["title"].lower(): #check if app name is in title
            return window["hwnd"] #return the hwnd of the window
    return None

def minimize(app):
    hwnd = find(app)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        return True 
    return False

def maximize(app):
    hwnd = find(app)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        return True 
    return False

