'''
Auto update for Windows 10 Insider
Useful for update native boot vhd/vhdx
By @raspiduino on github
Date created 19/11/2020
'''
# Many thanks whatever127 (uupdump.ml), Leonard Richardson (beautifulsoup) and other libs.

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


# Prompt for informations
print("Welcome to Updateinsider! Please read readme.md in the repo carefully before using this script!")
arch = input("Enter your arch (x86, amd64, arm64): ")
print(rings)
ring = input("Enter your ring: ")
lang = input("Choose a language ('en-us' for example): ")
edition = input("Choose your edition (core, coren, professional, professionaln): ")
vhd = input('Enter your vhd path (please remove the quotation marks ("")): ')
driveletter = input("Choose a driveletter to mount vhd file (for example 'V'). You should use the same letter at all time: ")

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

'''
New feature added on 29/11/2020
Auto try again if the exitcode not 0 (error occurred)
Reason? If you has an error (when running os.system),
it won't catch and stop. The script will continue to 
run and delete the create file and you have to start again!
'''

exitcode = -1
while exitcode != 0:
	exitcode = 0
	
	# Copy required files
	exitcode += os.system("mkdir scripts\\tmp")
	exitcode += os.system("xcopy /E scripts\\files scripts\\tmp")

# Change the file id
open("scripts\\tmp\\uup_download_windows.tmp.cmd", "w").write(open("scripts\\uup_download_windows.cmd", "r").read().replace("id=", "id=" + fileid))

# Run the uupdump script
exitcode = os.system("scripts\\tmp\\uup_download_windows.tmp.cmd") # This might take a while. Go and have a cup of coffee :D

# Edit the mountvhd script
open("scripts\\tmp\\mountvhd.tmp.txt", "w").write(open("scripts\\mountvhd.txt", "r").read().replace("file=", "file=" + vhd).replace("letter=", "letter=" + driveletter))

exitcode = -1
while exitcode != 0:
	exitcode = 0
	
	# Mount vhd file and format it
	exitcode += os.system('diskpart /s scripts\\tmp\\mountvhd.tmp.txt')

os.system("timeout /t 1 >nul")

exitcode = -1
while exitcode != 0:
	# Extract the wim file
	exitcode = os.system("scripts\\wimlib-imagex apply scripts\\tmp\\ISOFOLDER\\sources\\install.wim " + driveletter + ":\\") # This might take a while too!

'''
You have to set the boot flag for the vhd file (NOT for ARM64 if you are not on a ARM machine!!!)
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
