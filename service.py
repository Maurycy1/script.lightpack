# pylint: disable=C0103,C0301

# Modules General
import os, time, lightpack
from sys import argv

# Modules XBMC
import xbmc, xbmcgui, xbmcaddon

__settings__ = xbmcaddon.Addon("script.lightpack")
__language__ = __settings__.getLocalizedString

lphost = __settings__.getSetting("host")
lpport = int(__settings__.getSetting("port"))
lpapikey = __settings__.getSetting("apikey")

def notification(text):
    '''Send notification to XBMC'''
    import os.path
    text = text.encode("utf-8")
    icon = __settings__.getAddonInfo("icon")
    smallicon = icon.encode("utf-8")
    if __settings__.getSetting("notification") == 'true':
        xbmc.executebuiltin('Notification(Lightpack,' + text + ',3000,' + smallicon + ')')

def setProfile(enable, profile):
    '''Set Lightpack profile'''
    if enable == 'true':
        notification(__language__(32082)%profile)
        lpack.turnOn()
        lpack.setProfile(profile)
    else:
        notification(__language__(32081))
        lpack.turnOff()

print "service Lightpack"
notification(__language__(32080))
print "service Lightpack connect"

lpack = lightpack.lightpack(lphost, lpport, lpapikey, range(1, 11))
lpack.connect()

oldstatus = -1
while not xbmc.abortRequested:
    newstatus = 0
    player = xbmc.Player()
    audioIsPlaying = player.isPlayingAudio()
    videoIsPlaying = player.isPlayingVideo()
    if videoIsPlaying:
        newstatus = 1
    if audioIsPlaying:
        newstatus = 2
    if oldstatus != newstatus:
        oldstatus = newstatus
        lpack.lock()
        if newstatus == 0:
            setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("default_profile"))
        if newstatus == 1:
            setProfile(__settings__.getSetting("video_enable"), __settings__.getSetting("video_profile"))
        if newstatus == 2:
            setProfile(__settings__.getSetting("audio_enable"), __settings__.getSetting("audio_profile"))
        lpack.unlock()
    time.sleep(1)

# set off
notification(__language__(32081))
print "set status off for Lightpack"
lpack.lock()
lpack.turnOff()
lpack.unlock()
lpack.disconnect()
