
#Modules General
import os,sys,lightpack
from sys import argv

# Modules XBMC
import xbmc, xbmcgui, xbmcaddon

__settings__ = xbmcaddon.Addon("script.lightpack")

lpack = lightpack.lightpack(__settings__.getSetting("host"), int(__settings__.getSetting("port")), __settings__.getSetting("apikey"), [1,2,3,4,5,6,7,8,9,10] )
lpack.connect()
profiles = lpack.getProfiles()
del profiles[-1]
# profiles = ["profile1", "profile2", "profile3"]
profiles.append("off")

last_profile = __settings__.getSetting("last_profile")
if (last_profile == ""):
  last_profile_index = -1
else:
  last_profile_index = profiles.index(last_profile)
next_profile_index = last_profile_index + 1
if (next_profile_index > len(profiles)-1):
  next_profile_index = 0

lpack.lock()
lpack.turnOn()
next = profiles[next_profile_index]
lpack.setProfile(profiles[next_profile_index])
lpack.unlock
lpack.disconnect()
__settings__.setSetting("last_profile",profiles[next_profile_index])
xbmc.executebuiltin('Notification(%s,%s)'%("LightPack", profiles[next_profile_index]))
