import pydirectinput
import time
import keyboard
import pyautogui


def home():
    pyautogui.hotkey("win", "s")
    pyautogui.write("cmd")
    pyautogui.press("Enter")
    pyautogui.hotkey("win", "up")
    pyautogui.write("slmgr /ipk TX9XD-98N7V-6WMQ6-BX7FG-H8Q99")
    pyautogui.press("Enter")
    pyautogui.write("slmgr /skms kms8.msguides.com")
    pyautogui.press("Enter")
    pyautogui.write("slmgr /ato")
    pyautogui.press("Enter")
def pro():
    pyautogui.hotkey("win", "s")
    pyautogui.write("cmd")
    pyautogui.press("Enter")
    pyautogui.hotkey("win", "up")
    pyautogui.write("slmgr /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX")
    pyautogui.press("Enter")
    pyautogui.write("slmgr /skms kms8.msguides.com")
    pyautogui.press("Enter")
    pyautogui.write("slmgr /ato")
    pyautogui.press("Enter")



ver = input("enter pro or home")
if ver == "pro":
    pro()
elif ver == "home":
    home()
else:
    print("invalid version")