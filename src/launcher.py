#! /usr/bin/env python3

import subprocess
import argparse
from urllib.parse import urlparse
import sys
from PyQt5.QtWidgets import QApplication
from pickergui import MainWindow
from util import getInstalledBrowsers, getMousePosition

#user controlled settings
ICON_SIZE = 72
DISPLAY_APP_NAME = True
INSTALLED_BROWSERS_CACHE = []


def launchBroswer(browser):
    if '/' in browser: #'Normal' launch path
        cmd = [browser, args.url]
    elif '.' in browser: #Flatpak ref
        cmd = ["flatpak", "run", browser, args.url]
    print(cmd)
    subprocess.Popen(cmd)
    sys.exit(0)

def http_url(url):
    if url.startswith('http://'):
        return url
    if url.startswith('https://'):
        return url
    else:
        print("Not an HTTP/HTTPS URL.")
        raise argparse.ArgumentTypeError(
            "not an HTTP/HTTPS URL: '{}'".format(url))

def settings():
    print("Settings flag used. Opening configuration window")

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
        settings()
    else:
        urlparse(args.url)
        installedBrowsers = getInstalledBrowsers()

        mx,my = getMousePosition()

        app = QApplication(sys.argv)
        mainWin = MainWindow(installedBrowsers, iconsize=ICON_SIZE, displayappname=DISPLAY_APP_NAME, x=mx, y=my, callback=launchBroswer)
        mainWin.show()
        app.focusChanged.connect(mainWin.on_focusChanged)
        app.exec()
