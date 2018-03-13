"""
Developer : Naveen Kambham
Description:  This file contains the code to create a data set from a folder path with multiple sensor data.
It extracts data from sensors and then merges multiple features into a single sample.
"""

import FeatureExtraction.CommonFunctions.dataprocessing_helper as dataprocess
import FeatureExtraction.battery_sensor_features_extractor as battery
import FeatureExtraction.bluetooth_sensor_features_extractor as bluetooth
import FeatureExtraction.screenstate_sensor_features_extractor as screen
import FeatureExtraction.wifi_sensor_features_extractor as wifi


class DataSet(object):

    def __init__(self, path, balance=0.0):
        """Return object for Dataset"""
        self.path = path

    def extract_features(self):
        """
        method to extract the features from battery, bluetooth and wifi sensors
        expects file name on the Dataset object.
        """

        folder_Path = self.path
        if folder_Path=="":
            print("need to set the file name to create data set")
            return
        ################ Battery Sensor #################

        print("Extracting Battery Sensor Features ------------------------5%")
        df_battery= battery.extract(folder_Path+ "battery_events.csv")
        df_battery.to_csv(folder_Path+'battery_events_processed.csv')
        print("Number of Features extracted from Battery Sensor are:",len(df_battery))

        ################ Bluetooth Sensor #################

        print("Extracting Bluetooth Sensor Features ------------------------20%")
        df_bluetooth = bluetooth.extract(folder_Path + "bluetooth.csv")
        df_bluetooth.to_csv(folder_Path+'bluetooth_processed.csv')
        print("Number of Features extracted from Bluetooth Sensor are",len(df_bluetooth))


        ################ Screen Sensor #################

        print("Extracting Screen State Sensor Features ------------------------40%")
        df_screen = screen.main(folder_Path + "screenstate.csv")
        df_screen.to_csv(folder_Path+'screenstate_processed.csv')
        print("Number of Features extracted from Screen State Sensor are:",len(df_screen))


        ################ WiFi Sensor #################


        print("Extracting WiFi Features ------------------------60%")
        df_wifi = wifi.main(folder_Path + "wifi.csv")
        df_wifi.to_csv(folder_Path+'wifi_processed.csv')
        print("Number of Features extracted from WiFi Sensor are:",len(df_wifi))

        #Merging the features on ID and Date
        print("Extracting Features Done, Merging the Features ------------------------90%")
        dfs = [df_battery,df_bluetooth,df_screen,df_wifi]
        merged_features= dataprocess.merge(dfs, ['ID', 'Date'])

        print("Feature Extraction Finished, total number of samples are:",len(merged_features))

        print("Saving a copy at",folder_Path+'FeaturesExtraction.csv')
        merged_features.to_csv(folder_Path+'FeaturesExtraction.csv')

        return merged_features


