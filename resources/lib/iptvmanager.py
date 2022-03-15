# -*- coding: utf-8 -*-
"""IPTV Manager Integration module"""

import json
import socket

from resources.lib.utils import log
from resources.lib.m3u import M3U, M3UError


class IPTVManager:
    """Interface to IPTV Manager"""

    def __init__(self, port, file):
        """Initialize IPTV Manager object"""
        self.port = port
        self.m3u = M3U(file)

    def via_socket(func):
        """Send the output of the wrapped function to socket"""

        def send(self):

            """Decorator to send over a socket"""
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('127.0.0.1', self.port))
            try:
                sock.sendall(json.dumps(func(self)).encode())
            finally:
                sock.close()

        return send

    @via_socket
    def send_channels(self):
        """Return JSON-STREAMS formatted python datastructure to IPTV Manager"""


        log('MICAHG in the send_channels')
        channels = self.m3u.parse()

        if not channels:
            log('MICAHG channels are none')
        else:
            log(f'MICAHG first channel is {channels[0]}')
        # channels = []
        # for entry in CHANNELS:
        #     channels.append(dict(
        #         id=entry.get('id'),
        #         name=entry.get('label'),
        #         logo=entry.get('logo'),
        #         stream=entry.get('url'),
        #     ))
        return dict(version=1, streams=channels)

    @via_socket
    def send_epg(self):
        """Return JSON-EPG formatted python data structure to IPTV Manager"""
        from resources.lib.tvguide import TVGuide
        return dict(version=1, epg=TVGuide().get_epg_data())