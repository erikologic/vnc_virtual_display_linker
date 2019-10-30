#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#title           :vnc_virtual_display_linker.py
#description     :This program creates a second screen and start a VNC sever offering it
#author          :
#date            :
#version         :0.1
#usage           :vnc_virtual_display_linker.py
#notes           :
#python_version  :2.7.6
#=======================================================================

## README !!!
## This script will let you connect an external device
## to your X11 server as a second monitor thorugh VNC

## i.e. use your tablet to extend your desktop
## I have it working using Ubuntu 16.04

## INSTALLATION:
## $ pip install dotmap
## $ sudo apt install x11vnc
## then create a password!
## $ x11vnc -storepasswd

## If your tablet/phone is supported, you can connect to your
## device via an USB cable and the ADB platform
## but you need to install the proper tools first:
## $ sudo apt install adb android-tools-adb android-tools-fastboot

## Remember to turn on USB debugging on your device
## A good VNC client I found is bVNC Free

# =======================
#      CONFIGURATION
# =======================
PC_MONITOR_WIDTH = 1920
PC_MONITOR_LENGTH = 1080
VIRTUAL_MONITOR_WIDTH = 1280
VIRTUAL_MONITOR_LENGTH = 800


# =======================

# Import the modules needed to run the script.
import sys, os, subprocess, re, types

# Main definition - constants
menu_actions  = {}

# =======================
#      CLASSES
# =======================
class ScreenManager:
    def __init__(self):
        self.is_landscape = True

        self.conf = types.SimpleNamespace()
        self.conf.pc_monitor = types.SimpleNamespace(width = PC_MONITOR_WIDTH, length = PC_MONITOR_LENGTH)
        self.conf.virtual_monitor = types.SimpleNamespace(width = VIRTUAL_MONITOR_WIDTH, length = VIRTUAL_MONITOR_LENGTH)
        self.conf.state = types.SimpleNamespace(is_monitor_created = False, xrandr_mode=types.SimpleNamespace())

        self.new_monitor()

    def new_monitor(self):
        orientation = self.get_orientation()
        conf = self.conf

        if orientation == 'landscape':
            self.set_xrandr_mode_and_x11vnc_clip(conf.virtual_monitor.width, conf.virtual_monitor.length)
        else:
            self.set_xrandr_mode_and_x11vnc_clip(conf.virtual_monitor.length, conf.virtual_monitor.width)

        conf.state.xrandr_mode.alias = self.get_xrandr_mode_alias(conf.state.xrandr_mode.data)

        os.system("xrandr --newmode " + conf.state.xrandr_mode.data + " -hsync +vsync")
        os.system("xrandr --addmode VIRTUAL1 " + conf.state.xrandr_mode.alias)
        os.system("xrandr --output VIRTUAL1 --mode " + conf.state.xrandr_mode.alias)
        os.system('xrandr')

        self.conf.state.is_monitor_created = True

    def delete_monitor(self):
        conf = self.conf

        os.system("xrandr --output VIRTUAL1 --off")
        os.system("xrandr --delmode VIRTUAL1 " + conf.state.xrandr_mode.alias)
        os.system('xrandr')
        self.conf.state.is_monitor_created = False

    def start_vnc(self):
        os.system("x11vnc -usepw -nocursorshape -nocursorpos -noxinerama -solid -repeat -forever -clip " + self.conf.state.x11vnc_clip)

    def toggle_orientation(self):
        self.delete_monitor()
        self.is_landscape = False if self.is_landscape else True
        self.new_monitor()

    def get_orientation(self):
        return "landscape" if self.is_landscape else "portrait"

    def configure_resolution(self):
        os.system('clear')
        self.conf.pc_monitor.width  = self.configure_resolution_helper('Your monitor resolution width', self.conf.pc_monitor.width)
        self.conf.pc_monitor.length = self.configure_resolution_helper('Your monitor resolution length', self.conf.pc_monitor.length)
        self.conf.virtual_monitor.width  = self.configure_resolution_helper('Virtual monitor resolution width', self.conf.virtual_monitor.width)
        self.conf.virtual_monitor.length = self.configure_resolution_helper('Virtual monitor resolution length', self.conf.virtual_monitor.length)

    def adb_port_forwarding(self):
        os.system('adb reverse tcp:5900 tcp:5900')

    # PRIVATE
    def get_xrandr_mode_data(self, width, length):
        for line in subprocess.check_output("gtf {0} {1} 60".format(width, length), shell=True, universal_newlines=True).split("\n"):
            if "Mode" in line:
                return re.sub(r'Modeline (.*)-HSync.*', r'\1', line).strip()

    def get_xrandr_mode_alias(self, mode_data):
        return re.sub(r'.*(".*").*', r'\1', mode_data)

    def get_clip_param(self, width, length, pc_monitor_width):
        return "{0}x{1}+{2}+0".format(width, length, pc_monitor_width)

    def set_xrandr_mode_and_x11vnc_clip(self, width, length):
        self.conf.state.xrandr_mode.data = self.get_xrandr_mode_data( width, length)
        self.conf.state.x11vnc_clip =      self.get_clip_param(       width, length, self.conf.pc_monitor.width)

    def configure_resolution_helper(self, text, var):
        print(text + " [" +  str(var) + ']:')
        choice = input(" >>  ").strip()
        return choice if choice != '' else var

# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    screen_manager = ScreenManager()
    while True:
        os.system('clear')

        print("WELCOME TO THE AUTOMAGICALLY 2ND DISPLAY LINKER")
        print("Current status:")
        print("\tResolutions:")
        print("\tYour monitor:\t" + str(screen_manager.conf.pc_monitor.width) + 'x' + str(screen_manager.conf.pc_monitor.length))
        print("\tVirtual:\t" + str(screen_manager.conf.virtual_monitor.width) + 'x' + str(screen_manager.conf.virtual_monitor.length))
        print()
        print("\tOrientation: " + screen_manager.get_orientation())
        print("\tCreated 2nd monitor: " + str(screen_manager.conf.state.is_monitor_created))
        print()
        print("Please choose an action:")
        print("N. New monitor")
        print("D. Delete monitor")
        print("T. Toggle landscape / portrait")
        print("S. Start VNC")
        print("C. Configure the resolution of the monitors")
        print("A. Activate ADB port forwarding")
        print("Q. Quit")

        while True:
            choice = input(" >>  ").lower()
            if choice == 'q':
                sys.exit()
            else:
                try:
                    func = getattr(screen_manager, menu_actions[choice])
                    func()
                    print("\n\n\nPress ENTER to continue")
                    input()
                    break
                except KeyError:
                    print("Invalid selection, please try again.\n")
# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    's': 'start_vnc',
    't': 'toggle_orientation',
    'n': 'new_monitor',
    'd': 'delete_monitor',
    'c': 'configure_resolution',
    'a': 'adb_port_forwarding',
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
