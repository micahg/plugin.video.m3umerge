from unittest import TestCase
from resources.lib.m3u import M3U, M3UError, INFO_GUIDE_ID

GOOD_INFO_1 = ' tvg-id="guide id" '
GOOD_INFO_2 = 'tvg-id=guide_id'
GOOD_INFO_3 = 'tvg-id=guide_id '


class TestM3U(TestCase):
    def test_parse(self):
        pass

    def test_generate_channels(self):
        pass

    def test_read_marker_value(self):
        self.assertEqual(M3U.read_marker_value(GOOD_INFO_1, INFO_GUIDE_ID), 'guide id')
        self.assertEqual(M3U.read_marker_value(GOOD_INFO_2, INFO_GUIDE_ID), 'guide_id')
        self.assertEqual(M3U.read_marker_value(GOOD_INFO_3, INFO_GUIDE_ID), 'guide_id')
