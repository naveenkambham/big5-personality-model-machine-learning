#Author: Naveen Kambham
#Purpose: Thesis Project
#Main Functionality: This python file contains funcationality to fetch data from a remote server

'''Importing the required libraries'''
import pandas as pd
import numpy as np
import mysql.connector


def ConnectToDb_Return_Df_table(id,pwd,host,db_name,table_name):
    """
    This method will Connect to Data base and return the requested table in the form of a dataframe
    Better to make it a singleton to ensure multiple db connections are not spawned
    :param id:
    :param pwd:
    :param host:
    :param db_name:
    :param table_name:
    :return:
    """
    #making connection object
    conn = mysql.connector.connect(
         user=id,
         password=pwd,
         host=host,
         database=db_name)
    #Starting cursor
    cur = conn.cursor()
    # query = ("SELECT * FROM "+ tableName+" limit 2")
    #Preparing query with the give table name
    query = ("SELECT * FROM "+ table_name)

    #Reading the query result to a dataframe
    df =pd.read_sql_query(query,conn)
    conn.close()
    return df







