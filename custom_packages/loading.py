#! /usr/bin/env python3

""" module: load_data """

import pyodbc as odbc
import pandas as pd
import struct
from datetime import datetime

from credentials import conn_string

# ========================================================================


def create_table():

    # Create table
    sql_query_create_tables = '''
            DROP TABLE IF EXISTS LoanApplications ;
            CREATE TABLE LoanApplications  (
                [Gender] NVARCHAR(20)
                , [Married] NVARCHAR(10)
                , [Dependents] NVARCHAR(10)
                , [Education] NVARCHAR(20)
                , [Self_Employed] NVARCHAR(10) 
                , [ApplicantIncome] FLOAT
                , [CoapplicantIncome] FLOAT
                , [LoanAmount]  FLOAT
                , [Loan_Amount_Term] SMALLINT
                , [Credit_History] SMALLINT
                , [Property_Area] NVARCHAR(20)
                , [Loan_ID] NVARCHAR(50)
                , [ApplicationDateTime] NVARCHAR(20)
                , [RecordDateTime] BIGINT
                , [model_pred] NVARCHAR(10)
                , [model_pred_proba] NVARCHAR(50)
            );
            '''


    conn = odbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(sql_query_create_tables)
    cursor.commit()
    print(f'Table created at: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}')



def load_data(_features):
    # _features string
    sql_query_insert_data = f'INSERT INTO LoanApplications VALUES (\'{_features}\')'

    conn = odbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(sql_query_insert_data)
    cursor.commit()
    print(f'Data loaded at: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}')



def get_data(loan_id):
    # Get data from table
    sql_query_get_data = f'''
        SELECT * FROM LoanApplications 
        WHERE [Loan_ID] = '{loan_id}' 
            '''
    conn = odbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(sql_query_get_data)
    dataset = cursor.fetchall()
    # columns = [column[0] for column in cursor.description]
    print(f'Data fetched at: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}')
    return dataset


def get_all_data():
    # Get all data from table
    sql_query_get_data = f'''
        SELECT * FROM LoanApplications 
        ORDER BY RecordDateTime DESC
            '''
    conn = odbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(sql_query_get_data)
    dataset = cursor.fetchall()
    # columns = [column[0] for column in cursor.description]
    print(f'Data fetched at: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}')
    return dataset



def delete_data(where_clause):
    # Delete data from table
    sql_query_delete_data = f'''
        DELETE FROM LoanApplications
        WHERE {where_clause} 
            '''
    conn = odbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(sql_query_delete_data)
    cursor.commit()
    print(f'Data deleted at: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}')



def delete_loan_request(loan_id):
    # Delete record from table
    sql_query_delete_data = f'''
        DELETE FROM LoanApplications
        WHERE [Loan_ID] = '{loan_id}'
            '''
    conn = odbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(sql_query_delete_data)
    cursor.commit()
    print(f'Record deleted at: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}')






if __name__== "__main__":

    pass

    # Create table
    # create_table()

    # Test loading
    # Loan_ID = 'LP-3221050401389918522429'
    # Gender = 'Male'
    # Married = 'Yes'
    # Dependents = ''
    # Education = 'Graduate'
    # Self_Employed = 'Yes'
    # ApplicantIncome = ''
    # CoapplicantIncome = ''
    # LoanAmount = ''
    # Loan_Amount_Term = ''
    # Credit_History = 'Yes'
    # Property_Area = 'Urban'
    # ApplicationDateTime = '2023-11-08 14:28:32'
    #
    # _features = [Loan_ID,Gender,Married,Dependents,Education,Self_Employed,ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area,ApplicationDateTime]
    # _features = "\', \'".join(_features)

    # load_data(_features)


    # Test deleting data
    # delete_data(where_clause="Credit_History not in ('0','1')")


    # Test getting data
    # dataset = get_data()
    # print(dataset)