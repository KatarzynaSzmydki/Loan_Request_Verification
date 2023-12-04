#! /usr/bin/env python3

""" module: load_data """

import pyodbc as odbc
import pandas as pd
from datetime import datetime

from credentials import conn_string

# ========================================================================


sql_query_create_LoanApplications_Processed = '''
            DROP TABLE IF EXISTS LoanApplications_Processed ;
            CREATE TABLE LoanApplications_Processed  (
                [Gender] NVARCHAR(20)
                , [Married] NVARCHAR(10)
                , [Dependents] NVARCHAR(10)
                , [Education] NVARCHAR(20)
                , [Self_Employed] NVARCHAR(10)
                , [ApplicantIncome] FLOAT
                , [CoapplicantIncome] FLOAT
                , [LoanAmount]  FLOAT
                , [Loan_Amount_Term] SMALLINT
                , [Credit_History] NVARCHAR(10)
                , [Property_Area] NVARCHAR(10)
                , [Loan_ID] NVARCHAR(50)
                , [Loan_Status] NVARCHAR(20)
                , [ApplicationDateTime] NVARCHAR(20)
                , [RecordDateTime] BIGINT
                , [LastRecordUpdateDateTime] BIGINT
            );
            '''


sql_query_create_LoanApplications = '''
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
                , [Credit_History] NVARCHAR(10)
                , [Property_Area] NVARCHAR(10)
                , [Loan_ID] NVARCHAR(50)
                , [Loan_Status] NVARCHAR(20) NULL
                , [ApplicationDateTime] NVARCHAR(20)
                , [RecordDateTime] BIGINT
                , [LastRecordUpdateDateTime] BIGINT
                , [model_pred] NVARCHAR(10)
                , [model_pred_proba] NVARCHAR(50)
                , [ApplicationDate] AS CAST(ApplicationDateTime AS DATE)
            );
            '''



def create_table(sql_query_create_tables):

    # Create table
    conn = odbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(sql_query_create_tables)
    cursor.commit()
    print(f'Table created at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')



def load_data(table_to_load_to, _features):
    # _features string
    sql_query_insert_data = f'INSERT INTO {table_to_load_to} VALUES (\'{_features}\')'

    conn = odbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(sql_query_insert_data)
    cursor.commit()
    print(f'Data loaded at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')



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

    df = pd.DataFrame.from_records(dataset, columns=[col[0] for col in cursor.description])
    print(f'Data fetched at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    return df


def get_all_data(table):
    # Get all data from table
    sql_query_get_data = f'''
        SELECT * FROM {table} 
        ORDER BY CASE WHEN Loan_Status = '0' THEN 0 ELSE 1 END ASC, LastRecordUpdateDateTime DESC
            '''
    conn = odbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(sql_query_get_data)
    dataset = cursor.fetchall()

    # df = pd.DataFrame.from_records(dataset, columns=[col[0] for col in cursor.description])
    print(f'Data fetched at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
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
    print(f'Data deleted at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')



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
    print(f'Record deleted at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')




def update_loan_request(_features):

    sql_query_update_data = f'''
        UPDATE LoanApplications
        SET 
            [Gender] = '{_features[1]}'
            , [Married] = '{_features[2]}'
                , [Dependents] = '{_features[3]}'
                , [Education] = '{_features[4]}'
                , [Self_Employed] = '{_features[5]}'
                , [ApplicantIncome] = '{_features[6]}'
                , [CoapplicantIncome] = '{_features[7]}'
                , [LoanAmount]  = '{_features[8]}'
                , [Loan_Amount_Term] = '{_features[9]}'
                , [Credit_History] = '{_features[10]}'
                , [Property_Area] = '{_features[11]}'
                , [Loan_Status] = '{_features[12]}'
                , [LastRecordUpdateDateTime] = '{_features[13]}'
                , [model_pred] = '{_features[14]}'
                , [model_pred_proba] = '{_features[15]}'
                
        WHERE [Loan_ID] = '{_features[0]}'
            '''

    conn = odbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(sql_query_update_data)
    cursor.commit()
    print(f'Record {_features[0]} updated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')




def batch_load_data(table_to_load_to, _features):
    # _features string
    sql_query_insert_data = f'INSERT INTO {table_to_load_to} VALUES (\'{_features}\')'

    conn = odbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute(sql_query_insert_data)
    cursor.commit()
    print(f'Data loaded at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')




if __name__== "__main__":

    pass

    # Create table
    # create_table(sql_query_create_LoanApplications)

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

    # load_data('LoanApplications',_features)


    # Test deleting data
    # delete_data(where_clause="Credit_History not in ('0','1')")


    # Test getting data
    # dataset = get_data()
    # print(dataset)