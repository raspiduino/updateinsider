'''
Auto update for Windows 10 Insider
Useful for update native boot vhd/vhdx
By @raspiduino on github
Date created 19/11/2020
'''
# Many thanks whatever127 (uupdump.ml), Leonard Richardson (beautifulsoup), sysprogs.com (WinCDEmu), and other libs.

import requests
from bs4 import BeautifulSoup
import os
import admin # https://github.com/raspiduino/pythonadmin

if not admin.isUserAdmin():
    admin.runAsAdmin("python updateinsider.py")
    exit(1)

# Settings
arch = "" # Change this to fit your arch (x86, amd64, arm64)
# Change this to fit your ring:
rings = '''
retail : Normal release
rp     : Release preview
wis    : Slow rings
wif    : Fast rings (Default)
'''
ring = ""

lang = "" # Pick a language

edition = "" # Choose an edition (core, coren, professional, professionaln)

vhd = "" # Set the vhd file

driveletter = "" # Select a drive letter to mount vhd file

isodriveletter = "" # Select a drive letter to mount iso file

# Prompt for informations
arch = input("Enter your arch (x86, amd64, arm64): ")
print(rings)
ring = input("Enter your ring: ")
lang = input("Choose a language ('en-us' for example): ")
edition = input("Choose your edition (core, coren, professional, professionaln): ")
vhd = input("Enter your vhd path (please replace '\\' with '\\\\'): ")
driveletter = input("Choose a driveletter to mount vhd file (for example 'V'). You should use the same letter at all time: ")
isodriveletter = input("Choose a driveletter to mount iso (anything you want but not the existed letter): ")

# Get the version id
if ring == "wif":
	# Get the file id
	fileid = BeautifulSoup(requests.get("https://uupdump.ml/fetchupd.php?arch=" + arch + "&ring=wif&build=latest").content, 'html.parser').select("td")[0].select("a")[0]['href'][20:]
    
else:
    table = BeautifulSoup(requests.get("https://uupdump.ml/" + BeautifulSoup(requests.get("https://uupdump.ml/").content, 'html.parser').select("tr")[1 if ring == "retail" else 2 if ring == "rp" else 3].select("a")[0 if arch == "amd64" else 1 if arch == "x86" else 2]["href"]).content, 'html.parser').select("tr")
    version = []
    for i in range(1, len(table)):
    	version.append(table[i].select("i")[0].text[14:])
    fileid = table[version.index(max(version)) + 1].select("a")[0]["href"][20:]

# Copy required files
os.system("mkdir scripts\\tmp\\files")
os.system("copy scripts\\files\\*.* scripts\\tmp\\files\\")
os.system("copy scripts\\ConvertConfig.ini scripts\\tmp\\ConvertConfig.ini")

# Change the file id
open("scripts\\tmp\\uup_download_windows.tmp.cmd", "w").write(open("scripts\\uup_download_windows.cmd", "r").read().replace("id=", "id=" + fileid))

# Run the uupdump script
os.system("scripts\\tmp\\uup_download_windows.tmp.cmd") # This might take a while. Go and have a cup of coffee :D

# Mount vhd file and format it
open("scripts\\tmp\\mountvhd.tmp.txt", "w").write(open("scripts\\mountvhd.txt", "r").read().replace("file=", "file=" + vhd).replace("letter=", "letter=" + driveletter))
os.system('diskpart /s scripts\\tmp\\mountvhd.tmp.txt')

# Mount iso
os.system("start scripts\\PortableWinCDEmu-4.0.exe scripts\\tmp\\" + [f for f in os.listdir('scripts\\tmp\\') if f.endswith('.ISO')][0] + " " + isodriveletter)
os.system("timeout /t 1 >nul")

# Extract the wim file
os.system("scripts\\files\\wimlib-imagex apply " + isodriveletter + ":\\sources\\install.wim " + driveletter + ":\\") # This might take a while too!

'''
You have to set the boot flag for the vhd file
Please open Command Prompt as Admin and execute:
bcdboot V:\Windows
Replace V with the mounted vhd letter

If you want to change the name of the entry, please follow the instructions from
https://devblogs.microsoft.com/cesardelatorre/booting-natively-windows-10-from-a-vhdx-drive-file/
(Step 8)
You may need to change the default boot device too!

Restart and take a look at your new Insider version! :D
'''

# Clear temp file
os.system("rmdir /S /Q scripts\\tmp") # Comment out this line if you want to keep downloaded files
os.system("mkdir scripts\\tmp")

print("It's all done!")
print("You have installed Windows 10 " + edition + " " + lang + " (" + ring +" ring) on " + driveletter + ":\\")
print("Reboot and see your new version!")
os.system("pause")
