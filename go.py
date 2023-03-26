import pytchat


# For Windows
# http://stackoverflow.com/questions/1823762/sendkeys-for-python-3-1-on-windows
# https://stackoverflow.com/a/38888131

import win32api
import win32con
import win32gui
import time, sys

keyDelay = 0.1
# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
keymap = {
    "Up": win32con.VK_UP,
    "Left": win32con.VK_LEFT,
    "Down": win32con.VK_DOWN,
    "Right": win32con.VK_RIGHT,
    "b": 0x42, # ord("B"),
    "a": 0x41, # ord("A"),
    "y": 0x59, # ord("Y"),  # for DS
    "x": 0x58, # ord("X"),  # for DS
    "s": 0x53, # ord("S"),  # Start
    "e": 0x45, # ord("E"),  # Select
}

# this way has to keep window in focus
def sendKey(button):  
    win32api.keybd_event(keymap[button], 0, 0, 0)
    time.sleep(keyDelay)
    win32api.keybd_event(keymap[button], 0, win32con.KEYEVENTF_KEYUP, 0)

def SimpleWindowCheck(windowname): 
    try: 
        window = win32gui.FindWindow(windowName, None)  
    except win32gui.error: 
        try:  
            window = win32gui.FindWindow(None, windowName)
        except win32gui.error:
            return False
        else:
            return window
    else:
        return window

if __name__ == "__main__":
    windowName = "DeSmuME"
     
    chat = pytchat.create(video_id="YrsF1fGbgdk")
    
    while chat.is_alive():
        for c in chat.get().sync_items():
            key=c.message
            if(key.lower() in ['a', 'b','up','down','right','left']):
                if(key=='up'):
                    key='y'
                elif (key=='left'):
                    left='g'
                elif (key=='right'):
                    left='k'
                elif (key=='left'):
                    left='h'    
                winId = SimpleWindowCheck(windowName) 
                # winId = None 
                if not (winId): 
                    windowList = []
                    
                    def enumHandler(hwnd, list):
                        if windowName in win32gui.GetWindowText(hwnd):
                            list.append(hwnd)
                    
                    win32gui.EnumWindows(enumHandler, windowList)
                    # only the first id, may need to try the others
                    winId = windowList[0]

                    # can check with this
                    for hwnd in windowList:
                        hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
                        #print("window title/id/child id: ", win32gui.GetWindowText(hwnd), "/", hwnd, "/", hwndChild)

                win32gui.ShowWindow(winId, win32con.SW_SHOWNORMAL)
                import win32gui, win32com.client
                shell = win32com.client.Dispatch("WScript.Shell") 
                shell.SendKeys('%') #Undocks my focus from Python IDLE
                win32gui.SetForegroundWindow(winId)
                sendKey(key)