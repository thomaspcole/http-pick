#! /usr/bin/env python3

import subprocess
import argparse
from urllib.parse import urlparse
import sys
from PyQt5.QtWidgets import QApplication
from pickergui import MainWindow
from settingsgui import SettingsWindow
from util import getInstalledBrowsers, getMousePosition

#user controlled settings
ICON_SIZE = 72
DISPLAY_APP_NAME = False
INSTALLED_BROWSERS_CACHE = []


def launchBroswer(browser):
    if '/' in browser: #'Normal' launch path
        cmd = [browser, args.url]
    elif '.' in browser: #Flatpak ref
        cmd = ["flatpak", "run", browser, args.url]
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
  
if __name__ == '__main__':
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
    args = parser.parse_args()
    
    if(args.settings):
        app = QApplication(sys.argv)
        settingsWin = SettingsWindow(iconsize=ICON_SIZE)
        settingsWin.setWindowTitle("HTTP Pick - Settings")
        settingsWin.show()
        sys.exit(app.exec())
    else:
        urlparse(args.url)
        installedBrowsers = getInstalledBrowsers()

        mx,my = getMousePosition()

        app = QApplication(sys.argv)
        mainWin = MainWindow(installedBrowsers, iconsize=ICON_SIZE, displayappname=DISPLAY_APP_NAME, x=mx, y=my, callback=launchBroswer)
        mainWin.show()
        app.focusChanged.connect(mainWin.on_focusChanged)
        sys.exit(app.exec())
