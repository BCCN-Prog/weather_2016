import unittest
from wrapper.DataWrapH5py import Daily_DataBase, Hourly_DataBase

class Test_DataBase(unittest.TestCase):
    daily_DB = Daily_DataBase('test_daily.hdf5')
    hourly_DB = Hourly_DataBase('test_hourly.hdf5')

    def test_1_daily_create(self):
        self.assertEqual(self.daily_DB.f["weather_data"].shape, (400, 9))

    def test_2_hourly_create(self):
        self.assertEqual(self.hourly_DB.f["weather_data"].shape, (4000, 10))

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
