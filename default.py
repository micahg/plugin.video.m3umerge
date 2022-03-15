import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
from xbmcvfs import translatePath
import inputstreamhelper
import routing

from resources.lib.iptvmanager import IPTVManager
from resources.lib.utils import log, fetch_playlist

plugin = routing.Plugin()

@plugin.route('/iptv/channels')
def iptv_channels():
    """Send a list of IPTV channels."""
    log(f'MICAHG IN THE CHANNELS REQ')
    playlist = xbmcaddon.Addon().getSettingString('playlist')
    log(f'MICAH playlist is {playlist}')
    if not playlist:
        log('Unable to get playlist... please update configuration', True)
        return

    log(f'Fetching playlist {playlist}')
    # not actually a file but a
    file = fetch_playlist(playlist)

    port = int(plugin.args.get('port')[0])
    IPTVManager(port, file).send_channels()

@plugin.route('/')
def main_menu():
    log(f'MICAHG IN THE MAIN MENU')
    xbmcplugin.setContent(plugin.handle, 'videos')
    xbmcplugin.endOfDirectory(plugin.handle)

if __name__ == '__main__':
    plugin.run()
