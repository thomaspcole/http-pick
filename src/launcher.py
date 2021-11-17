#! /usr/bin/env python3

import subprocess
import argparse
from urllib.parse import urlparse
import sys
import tkinter as tk

webBrowsers = [
    "firefox",
    "chromium",
    "google-chrome",
    "opera",
    "epiphany",
    "epiphany-browser",
    "midori",
    "vivaldi"
]

window = tk.Tk()


def http_url(url):
    if url.startswith('http://'):
        return url
    if url.startswith('https://'):
        return url
    else:
        print("Not an HTTP/HTTPS URL.")
        raise argparse.ArgumentTypeError(
            "not an HTTP/HTTPS URL: '{}'".format(url))

def getInstalledBrowsers():
    #Check with update-alternatives
    browsers = subprocess.getoutput('update-alternatives --list x-www-browser').split()
    #print(browsers)

    #Check snaps
    snaps = subprocess.getoutput('snap list | awk \'{ print $1 }\'').split()
    del snaps[0]
    snaps = ["/snap/bin/" + s for s in snaps]
    #print(snaps)

    #Check flatpaks
    #flatpaks = subprocess.getoutput('flatpak list --app | awk \'{ print $2 }\'').split()
    #print(flatpaks)

    browsers.extend(snaps)

    installedBrowsers = []
    for browser in browsers:
        for wb in webBrowsers:
            if wb in browser:
                installedBrowsers.append(browser)
    return installedBrowsers

def buttonCallback():
    print("callback ")
    global window
    window.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Handler for http/https URLs.'
    )
    parser.add_argument(
        'url',
        type=http_url,
        help="URL starting with 'http://' or 'https://'",
    )
    args = parser.parse_args()

    parsed = urlparse(args.url)
    installedBrowsers = getInstalledBrowsers()
    print(installedBrowsers)

 
    window.overrideredirect(True)
    window.wait_visibility(window)
    window.wm_attributes("-alpha", 0.5)

    for b in installedBrowsers:
        tk.Button(window, text=b, image='', command=buttonCallback).pack()

    window.mainloop()

    cmd = [browser, args.url]
    subprocess.Popen(cmd)
    sys.exit(0)