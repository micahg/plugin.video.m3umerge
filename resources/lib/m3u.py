"""M3U Module"""


class M3U:

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        with open(file=self.filename, mode='r', encoding='utf-8') as file:
            # while line = file.readline() is not None:
            line_count = 0
            for line in file:
                print(f'line is "{line}')
                line_count += 1

            print(f'read {line_count} lines')
