# UpdateInsider - An easier way to update your 'native boot' Windows (Insider)
## What is this?
UpdateInsider is an easier way to update your 'native boot' Windows (Insider) installations. You probably see thing like this when trying to update your Windows:
<br>![alt](https://www.tenforums.com/attachments/tutorials/244305d1566646745-native-boot-virtual-hard-disk-how-upgrade-windows-vhd-no-upgrade.jpg)
<br>So with this script, you can update your Windows easily without that error and without putting the vhd into a vm! 
<br>The installation process takes around <b>2hr and 15min</b> (tested on Windows 10 with Pentium Dual-Core T4300, 2GB ram, SSD) and your process maybe quicker depends on your machine.

## How this works?
The Python script will find the lastest update available using uupdump.ml, then download the packages and convert them into iso by uupdump tools. The iso will be mounted and extract to vhd/vhdx file. Reboot and you will have a new installation!

## Requirement
- Python 3.7 ()
