"""
Developer : Naveen Kambham
Description:  Unit testing for battery sensor feature extractor code. Majority of the data extraction code has to be tested visually by looking at the plots distributions.
"""
#Importing the required libraries.
import unittest
import numpy as np
from FeatureExtraction import battery_sensor_features_extractor



class BatterySensorTestCase(unittest.TestCase):
      """
      Tests for battery_sensor_features_extractor.py
      """
      def test_TakeMostProbableTimeInStudy(self):
          """
          to test the most probable time functionality
          :return:
          """
          #case 1 multiple values in each day
          result= battery_sensor_features_extractor.TakeMostProbableTimeInStudy([1,1,1,1,2,2,3,3,3,3,3,3,3,3],[1,2,0])
          self.assertEqual(result,3)

          # case 2 only one value in a day
          result = battery_sensor_features_extractor.TakeMostProbableTimeInStudy(
              [1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3], [1])
          self.assertEqual(result, 4)

          # case 3 only one value in a day and it is not exists in the study times so far seen
          result = battery_sensor_features_extractor.TakeMostProbableTimeInStudy(
              [1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3], [0])
          self.assertEqual(result, 0)

      def test_extract(self):
          """
          testing the feature extractor code
          :return:
          """
          #extracting the features
          df_battery=battery_sensor_features_extractor.extract(r"/home/naveen/Data/Shed10/Filtered/battery_events.csv")

          # charging should atleast be greater than 0
          self.assertTrue(np.min(df_battery['Battery_Charging_Duration'] >=0))
          self.assertTrue(np.min(df_battery['CharginTimeDaily'] >=0) and np.max(df_battery['CharginTimeDaily'] <=24))


if __name__ == '__main__':
    unittest.main()