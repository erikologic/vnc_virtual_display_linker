# vnc_virtual_display_linker
### A Python script to create a second virtual monitor for connecting with VNC

This script will let you connect an external device to your X11 server as a second monitor through VNC
i.e. use your tablet to extend your desktop

I have it working using Ubuntu 16.04

## INSTALLATION:
`pip install dotmap`  
`sudo apt install x11vnc`

then create a password!  
`x11vnc -storepasswd`

## ADB SUPPORT
If your tablet/phone is supported, you can connect to your device via an USB cable and the ADB platform but you need to install the proper tools first:  
`sudo apt install adb android-tools-adb android-tools-fastboot`

Remember to turn on USB debugging on your device!!!

A good VNC client I found is bVNC Free: https://play.google.com/store/apps/details?id=com.iiordanov.freebVNC&hl=it
