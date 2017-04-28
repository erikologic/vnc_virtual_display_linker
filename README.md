# vnc_virtual_display_linker
### A Python script to create a second virtual monitor for connecting with VNC

This script will let you connect an external device to your X11 server as a second monitor through VNC  
i.e. use your tablet to extend your desktop

I have it working using Ubuntu 16.04 and an Android tablet

## INSTALLATION:
`pip install dotmap`  
`sudo apt install x11vnc`

then create a password!  
`x11vnc -storepasswd`

## USAGE
- place the script anywhere
- you might have to grant exec permissions: `chmod +x vnc_virtual_display_linker.py`
- launch the script `./vnc_virtual_display_linker.py`
- press `s` to start the VNC server with the default configuration
- `ctrl-c` to stop the server
- follow the instructions on the screen for more functionalities

Once the server has started, on your device:
- launch a VNC client like bVNC Free: https://play.google.com/store/apps/details?id=com.iiordanov.freebVNC&hl=it
- configure the ip address of the server and the password you used while installing x11vnc
- connect and enjoy your second screen!

## ADB SUPPORT
You should be able to connect most Android tablets/phones with an USB cable to the VNC server thanks to the ADB platform.

First, you need to install the proper tools:  
`sudo apt install adb android-tools-adb android-tools-fastboot`

Then you have to:
- connect your device (i.e. the tablet) to the PC with an USB cable 
- turn on USB debugging on your device
- activate the ADB support in the vnc_virtual_display_linker menu
- connect with your device to `localhost` as server address
