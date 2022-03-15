"""M3U Module"""

from resources.lib.utils import log

DIRECTIVE_PREFIX = '#'
DIRECTIVE_HEADER = '#EXTM3U'
DIRECTIVE_INFO = '#EXTINF:'
DIRECTIVE_GROUP = '#EXTGRP'

INFO_GUIDE_ID = 'tvg-id'
INFO_GROUP_TITLE = 'group-title'
INFO_NAME = 'tvg-name'
INFO_LOGO = 'tvg-logo'


class M3UError(Exception):

    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def get_message(self):
        return self.message


class M3U:
    """
    M3U Class.

    Parses M3U junk... a lot of this was copied from pvr.iptvsimple
    """
    # def __init__(self, filename):
    def __init__(self, file):
        self.file = file

    def parse(self):
        all_channels = []
        channels_by_id = {}
        total_raw_channels = 0
        # for channel in M3U.generate_channels(self.filename):
        for channel in M3U.generate_channels(self.file):
            total_raw_channels += 1
            if INFO_GUIDE_ID in channel:
                guide_id = channel[INFO_GUIDE_ID]
                if guide_id in channels_by_id:
                    existing_channel = channels_by_id[guide_id]
                    existing_channel['url'].extend(channel['url'])
                else:
                    channels_by_id[guide_id] = channel
                    all_channels.append(channel)
            else:
                all_channels.append(channel)

        # log(f'MICAH total raw channels: {total_raw_channels}')
        # log(f'MICAH total channels: {len(all_channels)}')
        # log(f'MICAH channels with Guide ID {len(channels_by_id.items())}')
        return all_channels

    @staticmethod
    def generate_channels(file):

        # with open(file=filename, mode='r', encoding='utf-8') as file:
        # ensure the header is right
        first_line = file.readline()
        log(f'MICAHG first line is {first_line}')
        if not first_line.startswith(DIRECTIVE_HEADER):
            raise M3UError('Missing M3U header')

        # loop over ever line, once we hit one that does not start with '#'
        # assume that is the actual stream URL
        channel = {}
        for line in file:
            if line[0] == DIRECTIVE_PREFIX:
                if line.startswith(DIRECTIVE_GROUP):
                    # TODO handle group
                    continue
                elif not line.startswith(DIRECTIVE_INFO):
                    continue

                info, name = M3U.split_info_line(line)
                for tag in INFO_GROUP_TITLE, INFO_GUIDE_ID, INFO_NAME, INFO_LOGO:
                    value = M3U.read_marker_value(info, tag)
                    if value and not value.isspace():
                        channel[tag] = value
                channel['name'] = name

            else:
                channel['url'] = [(channel['name'], line.strip())]
                yield channel
                channel = {}

    @staticmethod
    def split_info_line(line):
        # first shorten by any commas
        last_comma_idx = 0
        try:
            last_comma_idx = line.rindex(',')
        except ValueError:
            pass

        last_quote_idx = 0
        try:
            last_quote_idx = line.rindex('"')
        except ValueError:
            pass

        # find the first comma after the last quote
        if last_quote_idx:
            try:
                last_comma_idx = line.index(',', last_quote_idx)
            except ValueError:
                last_comma_idx = last_quote_idx

        return (line[0:last_comma_idx].strip(), line[last_comma_idx+1:].strip())

    @staticmethod
    def read_marker_value(info, marker):
        """
        Read EXTINF marker values
        :param info: the info portion of the line to parse
        :param marker: the marker to search for
        :return: None if the marker is not found, otherwise, the value
        """
        try:
            idx = info.index(f'{marker}=') + len(marker) + 1
        except ValueError:
            return None

        # deal with quotes
        end = '"' if info[idx] == '"' else ' '
        if end == '"':
            idx += 1

        if idx >= len(info):
            return None

        try:
            end_idx = info.index(end, idx)
        except ValueError:
            end_idx = len(info)

        return info[idx:end_idx]
