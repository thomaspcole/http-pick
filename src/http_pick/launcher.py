#! /usr/bin/env python3

import subprocess
import argparse
from urllib.parse import urlparse
import sys
from PyQt5.QtWidgets import QApplication
from http_pick.pickergui import MainWindow
from http_pick.settingsgui import SettingsWindow
from http_pick.util import getInstalledBrowsers, getMousePosition

#user controlled settings
ICON_SIZE = 72
DISPLAY_APP_NAME = False
INSTALLED_BROWSERS_CACHE = []


def launchBroswer(browser):
    if '/' in browser: #'Normal' launch path
        cmd = [browser, url]
    elif '.' in browser: #Flatpak ref
        cmd = ["flatpak", "run", browser, url]
    subprocess.Popen(cmd)
    quit()

def http_url(url):
    if url.startswith('http://'):
        return url
    if url.startswith('https://'):
        return url
    else:
        print("Not an HTTP/HTTPS URL.")
        raise argparse.ArgumentTypeError(
            "not an HTTP/HTTPS URL: '{}'".format(url))

def main():
    args=sys.argv[1:]
    parser = argparse.ArgumentParser(
        description='Handler for http/https URLs.'
    )
    parser.add_argument(
        '-u',
        '--url',
        type=http_url,
        help="URL starting with 'http://' or 'https://'",
    )
    parser.add_argument(
        '-s',
        '--settings',
        action='store_true',
        help="Show settings window",
    )
    args = parser.parse_args(args)
    
    if(args.settings):
        app = QApplication(sys.argv)
        settingsWin = SettingsWindow(iconsize=ICON_SIZE)
        settingsWin.setWindowTitle("HTTP Pick - Settings")
        settingsWin.show()
        sys.exit(app.exec())
    elif(args.url != None):
        urlparse(args.url)
        installedBrowsers = getInstalledBrowsers()

        global url
        url = args.url
        mx,my = getMousePosition()

        app = QApplication(sys.argv)
        mainWin = MainWindow(installedBrowsers, iconsize=ICON_SIZE, displayappname=DISPLAY_APP_NAME, x=mx, y=my, callback=launchBroswer)
        mainWin.show()
        app.focusChanged.connect(mainWin.on_focusChanged)
        sys.exit(app.exec())
    else:
        parser.print_help()
        sys.exit(0)
  
if __name__ == '__main__':
    main()    
