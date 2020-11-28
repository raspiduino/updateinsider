# UpdateInsider - An easier way to update your 'native boot' Windows (Insider)
## What is this?
UpdateInsider is an easier way to update your 'native boot' Windows (Insider) installations. You probably see thing like this when trying to update your Windows:
<br>![alt](https://www.tenforums.com/attachments/tutorials/244305d1566646745-native-boot-virtual-hard-disk-how-upgrade-windows-vhd-no-upgrade.jpg)
<br>So with this script, you can update your Windows easily without that error and without putting the vhd into a vm! 
<br>The installation process takes around <b>2hr and 15min</b> (tested on Windows 10 with Pentium Dual-Core T4300, 2GB ram, SSD) and your process maybe quicker depends on your machine.
<br>Support for both x86, amd64 and arm64 (aarch64)
<br><b>Tip:</b> You can use this to quickly test <i>Windows for Arm</i> on QEMU without install it (really long time!)

## How this works?
The Python script will find the lastest update available using uupdump.ml, then download the packages and convert them into iso by uupdump tools. The iso will be mounted and extract to vhd/vhdx file. Reboot and you will have a new installation!

## Requirement
- Python 3.7 (require bs4 and requests). You can use the portable version from <a href="https://github.com/raspiduino/updateinsider/releases">Release</a>
- Windows 8 and later (Fixing bugs on Windows 7)
- 16GB of free space to convert (not include the vhd size). It will be freed after use.
- A network connection

## Installation and usage
Before do this, <b>make sure</b> that your cmd is run as <b>Administrator</b>
You must have a created vhd.
- Normal install (if you have installed Python yet)
```bat
git clone git://github.com/raspiduino/updateinsider.git
cd updateinsider
updateinsider.py
```
- Portable version: Download from <a href="https://github.com/raspiduino/updateinsider/releases">Release</a> page and unzip it then run
```bat
python.exe updateinsider.py
```

<br>After starting the script, it will ask for the following info:
|Setting|Description|
|-------|-----------|
|<i>arch</i>|The architecture you want to download and install to the VHD (it can be <b>x86</b>, <b>amd64</b> or <b>arm64</b> (aarch64))|
|<i>rings</i>|The rings you want to download (it can be <b>retail</b> (Normal release, auto choose the lastest version), <b>rp</b>) (Release preview), <b>wis</b> (Slow ring) or <b>wif</b> (Fast ring))|
|<i>lang</i>|Pick a language (get a list of language from uupdump.ml). Example: <b><i>en-us</i></b> should be a great start!|
|<i>edition</i>|Pick <b><i>1</i></b> edition (it can be <b>core</b>, <b>coren</b>, <b>professional</b>, <b>professionaln</b>). For arm64 it can <b><i>only</i></b> be <b>core</b> and <b>professional</b>!|
|<i>vhd</i>|Enter your vhd/vhdx file path. <b><i>Remember</i></b> to replace "\" by "\\"!|
|<i>driveletter</i>|Choose a drive letter to mount your vhd/vhdx file. It should be only one letter for all the time you run this script. Example: 'V'|
|<i>isodriveletter</i>|Choose a drive letter to mount iso file. It doesn't matter, so pick up one randomly!|

## Warnings
- When you run this scripts, it will format your vhd, so if you need to keep your files stored in that vhd, saved it to another drive. (We are working to do this automaticly)
- For some reason if the console is closed when the script is running (like electricity went out), please check the root of current drive if there is a folder called <b><i>MountUUP</i></b>. If this folder exists, run cmd as Administrator and do the following:
```bat
dism /Unmount-image /MountDir:MountUUP /Discard
```
<br>Then delete the tmp folder in scripts folder and restart the script.

## Credits
Special thanks to:
- <a href="https://github.com/whatever127">whatever127</a> and other <i>uupdump</i> contributors (<a href="https://uupdump.ml">uupdump.ml</a>)
- Leonard Richardson and other BeautifulSoup contributors (<a href="https://pypi.org/project/beautifulsoup4/">BeautifulSoup4</a>)
- <a href="https://sysprogs.com">sysprogs.com</a> (WinCDEmu)
- And other libs...

## License
Under <a href="https://github.com/raspiduino/updateinsider/blob/master/LICENSE">GPL-v3</a>

## Todo
Auto backup files before installing to vhd/vhdx, then restore it after installed.
