import subprocess
from pynput.mouse import Controller


KNOWN_WEB_BROWSERS = [
    "firefox",
    "chromium",
    "google-chrome",
    "opera",
    "epiphany",
    "epiphany-browser",
    "midori",
    "vivaldi"
]

def getInstalledBrowsers():
    browsers = subprocess.getoutput('update-alternatives --list x-www-browser').split()

    snaps = subprocess.getoutput('snap list | awk \'{ print $1 }\'').split()
    del snaps[0]
    snaps = ["/snap/bin/" + s for s in snaps]

    flatpaks = subprocess.getoutput('flatpak list --app | awk \'{ print $2 }\'').split()

    browsers.extend(snaps)
    browsers.extend(flatpaks)

    installedBrowsers = []
    for browser in browsers:
        for wb in KNOWN_WEB_BROWSERS:
            if wb in browser:
                installedBrowsers.append(browser)
    return installedBrowsers

def getMousePosition():
    mouse = Controller()
    return mouse.position