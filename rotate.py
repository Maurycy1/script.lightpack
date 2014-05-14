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

profiles = lpack.getProfiles()
del profiles[-1]
profiles.append(__language__(32071))
off = len(profiles)-1

last_profile = __settings__.getSetting("last_profile")
if last_profile == "":
    last_profile_index = -1
else:
    last_profile_index = profiles.index(last_profile)
next_profile_index = last_profile_index + 1
if next_profile_index > len(profiles)-1:
    next_profile_index = 0

lpack.lock()
lpack.turnOn()

if off == int(next_profile_index):
    lpack.turnOff()
else:
    lpack.turnOn()
    lpack.setProfile(profiles[next_profile_index])

lpack.unlock()
lpack.disconnect()

# Store profile name for display and notify user of profile change
__settings__.setSetting("last_profile", profiles[next_profile_index])
xbmc.executebuiltin('Notification(%s,%s)'%("LightPack", profiles[next_profile_index]))
