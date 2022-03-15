import requests


def fetch_playlist(playlist):
    resp = requests.get(playlist)
    if not resp.status_code == 200:
        log(f'Unable to fetch playlist. Status {resp.status_code}, {resp.content}', True)
        return None

    return resp.raw


def log(msg, error = False):
    """
    Log an error
    @param msg The error to log
    @param error error severity indicator
    """
    try:
        import xbmc
        full_msg = "plugin.video.cbc: {}".format(msg)
        xbmc.log(full_msg, level=xbmc.LOGERROR if error else xbmc.LOGINFO)
    except ModuleNotFoundError:
        print(msg)