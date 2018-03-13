"""
Developer : Naveen Kambham
Description:  Unit testing for wifi sensor feature extractor code. Majority of the data extraction code has to be tested visually by looking at the plots distributions.
"""
#Importing the required libraries.
import unittest
import numpy as np
from FeatureExtraction import wifi_sensor_features_extractor
class WiFiSensorTestCase(unittest.TestCase):
      """
      Tests for wifi_sensor_features_extractor.py
      """
      def test_find_get_campus_entry_leave_times(self):
          """
          to test the get_campus_entry_leave_times code
          :return:
          """
          #extracting the features
          df_entry_leave_timeinschool=wifi_sensor_features_extractor.get_campus_entry_leave_times(r"/home/naveen/Data/Shed10/Filtered/wifi.csv")

          # contact patterns has to be greater than or equal to o or less than 24.0 hours
          self.assertTrue(np.min(df_entry_leave_timeinschool['EntryTime'] >=0) and np.max(df_entry_leave_timeinschool['EntryTime'] <=24))
          self.assertTrue(np.min(df_entry_leave_timeinschool['LeavingTime'] >= 0) and np.max( df_entry_leave_timeinschool['LeavingTime'] <= 24))
          self.assertTrue(np.min(df_entry_leave_timeinschool['Time_In_School'] >= 0) and np.max(df_entry_leave_timeinschool['Time_In_School'] <= 24))

          #Take some random participants and check time_in_school == leavetime - entrytime
          if(len(df_entry_leave_timeinschool) >=100):
             self.assertTrue(df_entry_leave_timeinschool.loc[100,'Time_In_School'] == df_entry_leave_timeinschool.loc[100,'LeavingTime'] - df_entry_leave_timeinschool.loc[100,'EntryTime'])
             self.assertTrue(df_entry_leave_timeinschool.loc[75, 'Time_In_School'] == df_entry_leave_timeinschool.loc[
                 75, 'LeavingTime'] - df_entry_leave_timeinschool.loc[75, 'EntryTime'])
             self.assertTrue(df_entry_leave_timeinschool.loc[25, 'Time_In_School'] == df_entry_leave_timeinschool.loc[
                 25, 'LeavingTime'] - df_entry_leave_timeinschool.loc[25, 'EntryTime'])
             self.assertTrue(df_entry_leave_timeinschool.loc[0, 'Time_In_School'] == df_entry_leave_timeinschool.loc[
                 0, 'LeavingTime'] - df_entry_leave_timeinschool.loc[0, 'EntryTime'])
             self.assertTrue(df_entry_leave_timeinschool.loc[50, 'Time_In_School'] == df_entry_leave_timeinschool.loc[
                 50, 'LeavingTime'] - df_entry_leave_timeinschool.loc[50, 'EntryTime'])

      def test_get_diff_wifi_seen(self):
          """
                   to test the test_get_diff_wifi_seen code
                   :return:
                   """
          # extracting the features
          df_test_get_diff_wifi_seen = wifi_sensor_features_extractor.test_get_diff_wifi_seen(
              r"/home/naveen/Data/Shed10/Filtered/wifi.csv")

          # contact patterns has to be greater than or equal to o or less than 24.0 hours
          self.assertTrue(np.min(df_test_get_diff_wifi_seen['WifiCountPerDay'] >= 0) and np.max(
              df_test_get_diff_wifi_seen['WifiCountPerDay'] <= 500))




if __name__ == '__main__':
    unittest.main()