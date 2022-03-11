"""M3U Module"""


DIRECTIVE_PREFIX = '#'
DIRECTIVE_HEADER = '#EXTM3U'
DIRECTIVE_INFO = '#EXTINF:'

INFO_GUIDE_ID = 'tvg-id='




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
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        for channel in M3U.generate_channels(self.filename):
            print(f'Micah channel is "{channel}"')

    @staticmethod
    def generate_channels(filename):

        with open(file=filename, mode='r', encoding='utf-8') as file:
            # while line = file.readline() is not None:

            # ensure the header is right
            if not file.readline().startswith(DIRECTIVE_HEADER):
                raise M3UError('Missing M3U header')

            # loop over ever line, once we hit one that does not start with '#'
            # assume that is the actual stream URL
            for line in file:
                if line[0] == DIRECTIVE_PREFIX:
                    if not line.startswith(DIRECTIVE_INFO):
                        continue
                    print(f'info is {line.strip()}')

                    # how we going to do this? ok, format is either x="y" or x=y\
                    # so, find the value that comes after =, and if its not " then
                    # search for space
                    guide_id = M3U.read_marker_value(line, INFO_GUIDE_ID)
                    if not guide_id:
                        raise M3UError('Invalid guide ID')
                    print(f'Micah got "{guide_id}"')
                else:
                    yield {'url': line.strip()}

    @staticmethod
    def read_marker_value(line, marker):
        try:
            idx = line.index(marker) + len(marker)
        except ValueError:
            return None

        # deal with quotes
        end = '"' if line[idx] == '"' else ' '
        if end == '"':
            idx += 1

        if idx >= len(line):
            return None

        end_idx = line.index(end, idx)

        return line[idx:end_idx]
