from unittest import TestCase
from resources.lib.m3u import M3U, M3UError, INFO_GUIDE_ID

GOOD_INFO_LINE_1 = ' tvg-id="guide id" , Title'
GOOD_INFO_LINE_2 = 'tvg-id=guide_id,Title '
GOOD_INFO_LINE_3 = 'tvg-id=guide_id, A Title '
GOOD_INFO_LINE_4 = ' tvg-id="",A Title'
GOOD_INFO_1 = 'tvg-id="guide id"'
GOOD_INFO_2 = 'tvg-id=guide_id'
GOOD_INFO_3 = 'tvg-id=""'
BAD_INFO_1 = ''
BAD_INFO_2 = ' tvg-id="guide,id", Title '
BAD_INFO_3 = ' tvg-id="guide_ID"'


class TestM3U(TestCase):

    def test_split_info_line(self):
        info, name = M3U.split_info_line(GOOD_INFO_LINE_1)
        self.assertEqual(M3U.split_info_line(GOOD_INFO_LINE_1), ('tvg-id="guide id"', 'Title'))
        self.assertEqual(M3U.split_info_line(GOOD_INFO_LINE_2), ('tvg-id=guide_id', 'Title'))
        self.assertEqual(M3U.split_info_line(GOOD_INFO_LINE_3), ('tvg-id=guide_id', 'A Title'))
        self.assertEqual(M3U.split_info_line(GOOD_INFO_LINE_4), ('tvg-id=""', 'A Title'))

    def test_read_marker_value(self):
        self.assertEqual(M3U.read_marker_value(GOOD_INFO_1, INFO_GUIDE_ID), 'guide id')
        self.assertEqual(M3U.read_marker_value(GOOD_INFO_2, INFO_GUIDE_ID), 'guide_id')
        self.assertEqual(M3U.read_marker_value(GOOD_INFO_3, INFO_GUIDE_ID), '')
        self.assertEqual(M3U.read_marker_value(BAD_INFO_1, INFO_GUIDE_ID), None)
        self.assertEqual(M3U.read_marker_value(BAD_INFO_2, INFO_GUIDE_ID), 'guide,id')
        self.assertEqual(M3U.read_marker_value(BAD_INFO_3, INFO_GUIDE_ID), 'guide_ID')
