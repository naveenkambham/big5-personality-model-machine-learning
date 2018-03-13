"""
Developer : Naveen Kambham
Description:  Unit testing for bluetooth sensor feature extractor code. Majority of the data extraction code has to be tested visually by looking at the plots distributions.
"""
#Importing the required libraries.
import unittest
import numpy as np
from FeatureExtraction import bluetooth_sensor_features_extractor
class BluetoothSensorTestCase(unittest.TestCase):
      """
      Tests for bluetooth_sensor_features_extractor.py
      """
      def test_find_contactrate_perday(self):
          """
          to test the contactrate code
          :return:
          """
          #extracting the features
          df_bluetooth=bluetooth_sensor_features_extractor.extract(r"/home/naveen/Data/Shed10/Filtered/bluetooth.csv")

          # contact patterns has to be greater than or equal to o or less than 100 max number of participants
          self.assertTrue(np.min(df_bluetooth['ContactRatePerDay'] >=0) and np.max(df_bluetooth['ContactRatePerDay'] <=100))


if __name__ == '__main__':
    unittest.main()