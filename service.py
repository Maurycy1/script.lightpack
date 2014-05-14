
#Modules General
import os,lightpack
import time
from sys import argv

# Modules XBMC
import xbmc, xbmcgui, xbmcaddon

__settings__ = xbmcaddon.Addon( "script.lightpack" )
__language__ = __settings__.getLocalizedString

#########################################################################################################
## BEGIN
#########################################################################################################
def notification(text):
	import os.path
	text = text.encode('utf-8')
	icon=__settings__.getAddonInfo( "icon" )
	smallicon = icon.encode( "utf-8" )
	if (__settings__.getSetting("notification")  == 'true'):
		xbmc.executebuiltin('Notification(Lightpack,'+text+',3000,' + smallicon + ')')

def setProfile(enable, profile):
	if (enable == 'true'):
		notification(__language__(32082)%profile)
		lpack.turnOn()
		lpack.setProfile(profile)
# if no default leave set as is
#	else:
#		notification(__language__(32081))
#		lpack.turnOff()

print "service Lightpack"
notification(__language__(32080))
print "service Lightpack connect"
lpack = lightpack.lightpack(__settings__.getSetting("host"), int(__settings__.getSetting("port")), __settings__.getSetting("apikey"), [1,2,3,4,5,6,7,8,9,10] )
lpack.connect()
oldstatus = -1
while (not xbmc.abortRequested):
	newstatus = 0
	player = xbmc.Player()
	audioIsPlaying = player.isPlayingAudio()
	videoIsPlaying = player.isPlayingVideo()
	if videoIsPlaying:
		newstatus = 1
	if audioIsPlaying:
		newstatus = 2
	if (oldstatus!=newstatus):
		oldstatus = newstatus
		lpack.lock()
		if (newstatus == 0):
			setProfile(__settings__.getSetting("default_enable"),__settings__.getSetting("default_profile"))
		if (newstatus == 1):
			setProfile(__settings__.getSetting("video_enable"),__settings__.getSetting("video_profile"))
		if (newstatus == 2):
			setProfile(__settings__.getSetting("audio_enable"),__settings__.getSetting("audio_profile"))
		lpack.unlock()
	time.sleep(1)
	
# set off
notification(__language__(32081))
print "set status off for Lightpack"
#lpack = lightpack.lightpack(__settings__.getSetting("host"), int(__settings__.getSetting("port")), __settings__.getSetting("apikey"), [1,2,3,4,5,6,7,8,9,10] )
#lpack.connect()
lpack.lock()
lpack.turnOff()
lpack.unlock
lpack.disconnect()
