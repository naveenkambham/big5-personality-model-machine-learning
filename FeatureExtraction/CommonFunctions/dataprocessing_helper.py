"""
Developer : Naveen Kambham
Description:  This file contains data processing methods such as merging two data frames and filtering data frames.
"""

import functools as funs

import pandas as pd

import FeatureExtraction.CommonFunctions.converters as converters


def merge(df_list,merge_param_list):
    """
    method to merge the list of data frames based on list of column identifiers. This returns intersection of values
    :param df_list:
    :param merge_param_list:
    :return merged data frame:
    """

    merged = funs.reduce(lambda left, right: pd.merge(left, right,how='inner', on=merge_param_list), df_list)

    return merged

def merge_outer(df_list,merge_param_list):
    """
    method to merge the list of data frames based on list of column identifiers. This gives union of values
    :param df_list:
    :param merge_param_list:
    :return merged data frame:
    """

    merged = funs.reduce(lambda left, right: pd.merge(left, right,how='outer', on=merge_param_list), df_list)

    return merged



def filter_data_on_complaince(folder_Path,complaince_rate):
    """
    Method to filter the participants based on complaince rate
    :param folder_Path:
    :param complaince_rate:
    :return:
    """
    complaince_df=pd.read_csv(folder_Path+"complaince.csv")
    complaince_df['Percent'] = complaince_df['Percent'].apply(converters.ConvertPercent)
    complaince_df = complaince_df.loc[complaince_df.Percent >= complaince_rate]
    IDs= complaince_df.ID.unique()
    # print(IDs)
    df_apps=pd.read_csv(folder_Path+"app_usage.csv")
    df_apps = df_apps.loc[df_apps.user_id.isin(IDs)]
    df_apps = df_apps.reset_index(drop=True)
    df_apps.to_csv(folder_Path+"Filtered/app_usage.csv")


    df_battery= pd.read_csv(folder_Path+"battery_events.csv")
    df_battery= df_battery.loc[df_battery.user_id.isin(IDs)]
    df_battery = df_battery.reset_index(drop=True)
    df_battery.to_csv(folder_Path+"Filtered/battery_events.csv")


    df_bluetooth = pd.read_csv(folder_Path+"bluetooth.csv")
    df_bluetooth = df_bluetooth.loc[df_bluetooth.user_id.isin(IDs)]
    df_bluetooth = df_bluetooth.reset_index(drop=True)
    df_bluetooth.to_csv(folder_Path+"Filtered/bluetooth.csv")

    df_screen = pd.read_csv(folder_Path+"screenstate.csv")
    df_screen = df_screen.loc[df_screen.user_id.isin(IDs)]
    df_screen = df_screen.reset_index(drop=True)
    df_screen.to_csv(folder_Path+"Filtered/screenstate.csv")


    df_wifi = pd.read_csv(folder_Path+"wifi.csv")
    df_wifi = df_wifi.loc[df_wifi.user_id.isin(IDs)]
    df_wifi = df_wifi.reset_index(drop=True)
    df_wifi.to_csv(folder_Path+"Filtered/wifi.csv")
