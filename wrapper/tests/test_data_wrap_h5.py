import os
import unittest
from wrapper.DataWrapH5py import Daily_DataBase

class Test_DataBase(unittest.TestCase):

    def test_1_daily_create(self):
        daily_DB = Daily_DataBase()
        self.assertTrue(os.path.exists(daily_DB.f))

    # def test_isupper(self):
        # self.assertTrue('FOO'.isupper())
        # self.assertFalse('Foo'.isupper())
#
    # def test_split(self):
        # s = 'hello world'
        # self.assertEqual(s.split(), ['hello', 'world'])
        # # check that s.split fails when the separator is not a string
        # with self.assertRaises(TypeError):
            # s.split(2)

if __name__ == '__main__':
    unittest.main()
