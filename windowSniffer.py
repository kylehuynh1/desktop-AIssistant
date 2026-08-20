import win32gui

def callback(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd): #check if window is visible
        title = win32gui.GetWindowText(hwnd) #pull the title of the window by using corresponding hwnd (numbers)
        if(title): #check if title is empty or not
            windows.append({
                "hwnd": hwnd, #id
                "title": title #name
            }) #add to list if not empty

def windowSniffer():
    windows = [] #populate with detected windows running
    win32gui.EnumWindows(callback, windows)

    return windows #return list
