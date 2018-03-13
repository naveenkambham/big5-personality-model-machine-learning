"""
Developer : Naveen Kambham
Description:  Unit testing for battery sensor feature extractor code. Majority of the data extraction code has to be tested visually by looking at the plots distributions.
"""
#Importing the required libraries.
import unittest
import numpy as np
from FeatureExtraction import screenstate_sensor_features_extractor
class ScreenStateSensorTestCase(unittest.TestCase):
      """
      Tests for screenstate_sensor_features_extractor.py
      """
      def test_get_activephone_usage(self):
          """
          to test the get_activephone_usage functionality
          :return:
          """
          #extracting the features
          df_get_activephone_usage=screenstate_sensor_features_extractor.extract(r"/home/naveen/Data/Shed10/Filtered/battery_events.csv")

          # ON and OFF should be between 0 and 100
          self.assertTrue((df_get_activephone_usage['ScreenState_ON'] / (df_get_activephone_usage['ScreenState_ON'] +df_get_activephone_usage['ScreenState_OFF']) >=0))
          self.assertTrue((df_get_activephone_usage['ScreenState_OFF'] / (
          df_get_activephone_usage['ScreenState_ON'] + df_get_activephone_usage['ScreenState_OFF']) <= 100))


          #assert for some random participants
          if(len(df_get_activephone_usage >=100)):
             self.assertTrue((df_get_activephone_usage.loc[50,'ScreenState_ON'] == (
              df_get_activephone_usage.loc[50, 'ScreenState_ON'] + df_get_activephone_usage.loc[50,'ScreenState_OFF'] - df_get_activephone_usage.loc[50,'ScreenState_OFF']) >= 0))

             self.assertTrue((df_get_activephone_usage.loc[25, 'ScreenState_ON'] == (
                 df_get_activephone_usage.loc[25, 'ScreenState_ON'] + df_get_activephone_usage.loc[
                     25, 'ScreenState_OFF'] - df_get_activephone_usage.loc[25, 'ScreenState_OFF']) >= 0))


if __name__ == '__main__':
    unittest.main()