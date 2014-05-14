# pylint: disable=C0103,C0301

# Modules General
import os, lightpack
from sys import argv

# Modules XBMC
import xbmc, xbmcgui, xbmcaddon

__settings__ = xbmcaddon.Addon("script.lightpack")
__language__ = __settings__.getLocalizedString

lphost = __settings__.getSetting("host")
lpport = int(__settings__.getSetting("port"))
lpapikey = __settings__.getSetting("apikey")

lpack = lightpack.lightpack(lphost, lpport, lpapikey, range(1, 11))
lpack.connect()

menu = lpack.getProfiles()
del menu[-1]
menu.append(__language__(32071))
off = len(menu)-1

lpquit = False
while not lpquit:
    selected = xbmcgui.Dialog().select(__language__(32070), menu)
    if selected != -1:
        lpack.lock()
        if off == int(selected):
            lpack.turnOff()
        else:
            lpack.turnOn()
            lpack.setProfile(menu[selected])
        lpack.unlock()
    lpquit = True
lpack.disconnect()
