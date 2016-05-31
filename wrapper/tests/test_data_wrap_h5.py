import unittest
import os
from wrapper.DataWrapH5py import Daily_DataBase, Hourly_DataBase
# import pudb



DAILY_TEST_FILE = 'test_daily.hdf5'
HOURLY_TEST_FILE = 'test_hourly.hdf5'
class Test_DataBase(unittest.TestCase):
    os.remove(DAILY_TEST_FILE)
    os.remove(HOURLY_TEST_FILE)
    daily_DB = Daily_DataBase(DAILY_TEST_FILE)
    hourly_DB = Hourly_DataBase(HOURLY_TEST_FILE)

    test_num = 666
    hourly_test_dict = {'date': test_num, 'hour': test_num, 'site': test_num,
                        'geolocation': test_num, 'temperature': test_num,
                        'humidity': test_num, 'wind_speed': test_num,
                        'rain_chance': test_num, 'rain_amt': test_num, 'cloud_cover': test_num}
    daily_test_dict = {'date': test_num, 'site': test_num, 'geolocation': test_num,
                       'high': test_num, 'low': test_num, 'midday': test_num,
                       'rain_chance': test_num, 'rain_amt': test_num, 'cloud_cover': test_num}

    full_hourly_dict = {'site': test_num, 'date': test_num,
                        'hourly': {'00': hourly_test_dict, '01': hourly_test_dict,
                                   '03': daily_test_dict}}

    def test_1_database_create(self):

        print('\n------------------------')
        print('Test database creation')
        print('------------------------')
        print('Checking intial shapes of arrays...')
        self.assertEqual(self.daily_DB.f["weather_data"].shape, (400, 9))
        self.assertEqual(self.hourly_DB.f["weather_data"].shape, (4000, 10))
        print('------------------------')

    def test_2_add_hourly_single_point(self):

        print('\n------------------------')
        print('Test hourly database insertion')
        print('------------------------')

        _n1 = self.hourly_DB.number_entries()
        print('Number of entries before insert:', _n1)

        self.hourly_DB.add_data_point(**self.hourly_test_dict)

        _n2 = self.hourly_DB.number_entries()

        print('Number of entries after insert:', _n2)

        self.assertEqual(_n2-_n1, 1)

        # print('Closing database...')
        # self.hourly_DB.f.close()
#
        # print('Reload database...')
        # self.hourly_DB = Hourly_DataBase('test_hourly.hdf5')
#
        # print('Check persistance of data...')
        # _n3 = self.hourly_DB.number_entries()
#
        # self.assertEqual(_n3, _n2)
        print('------------------------\n\n')

    def test_3_add_daily_single_point(self):

        print('\n------------------------')
        print('Test daily database insertion')
        print('------------------------')

        _n1 = self.daily_DB.number_entries()
        print('Number of entries before insert:', _n1)

        self.daily_DB.add_data_point(**self.daily_test_dict)

        _n2 = self.daily_DB.number_entries()

        print('Number of entries after insert:', _n2)

        self.assertEqual(_n2-_n1, 1)

        print('------------------------\n\n')

        # self.assertTrue('FOO'.isupper())
        # self.assertFalse('Foo'.isupper())
        # with self.assertRaises(TypeError):
            # s.split(2)

    def test_4_resize(self):

        print('\n------------------------')
        print('Test resize')
        print('------------------------')

        _cap1 = self.hourly_DB.get_capacity()
        print('Capacity before insert:', _cap1)

        # reset pointer
        self.hourly_DB.f['metadata'][0] = _cap1[0]

        _n1 = self.hourly_DB.number_entries()
        print('Number of entries before insert:', _n1)

        self.hourly_DB.add_data_point(**self.hourly_test_dict)

        _cap2 = self.hourly_DB.get_capacity()
        print('Capacity after insert:', _cap2)
        _n2 = self.hourly_DB.number_entries()
        print('Number of entries after insert:', _n2)

        self.assertEqual(_cap2[0], _cap1[0]*2)
        self.assertEqual(_n2, _n1+1)

        print('------------------------\n\n')

    def test_5_save_hourly_dict(self):
        print('\n------------------------')
        print('Test Scraping Interface')
        print('------------------------')

        _n1 = self.hourly_DB.number_entries()
        print('Number of entries before insert:', _n1)

        self.hourly_DB.save_hourly_dict(self.full_hourly_dict)

        _n2 = self.hourly_DB.number_entries()
        print('Number of entries before insert:', _n2)

        self.assertEqual(_n2, _n1+3)

if __name__ == '__main__':
    unittest.main()
