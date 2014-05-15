# pylint: disable=C0103,C0301

# Modules General
import lightpack

# Modules XBMC
import xbmc, xbmcgui, xbmcaddon

__settings__ = xbmcaddon.Addon("script.lightpack")
__language__ = __settings__.getLocalizedString


def notification(text):
    '''Send notification to XBMC'''
    text = text.encode("utf-8")
    icon = __settings__.getAddonInfo("icon")
    smallicon = icon.encode("utf-8")
    if __settings__.getSetting("notification") == 'true':
        xbmc.executebuiltin('Notification(Lightpack,"' + text + '",3000,"' + smallicon + '")')


lphost = __settings__.getSetting("host")
lpport = int(__settings__.getSetting("port"))
lpapikey = __settings__.getSetting("apikey")

lpack = lightpack.lightpack(lphost, lpport, lpapikey, range(1, 11))

if lpack.connect() == 0 and lpapikey:
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
else:
    notification(__language__(32083))

lpack.disconnect()
