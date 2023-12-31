#! /usr/bin/env python3

""" module: actions """
import json

import requests
import pickle

# ========================================================================


import os
from datetime import datetime
from azure.storage.filedatalake import (
    DataLakeServiceClient
)
from azure.storage.blob import BlobServiceClient

from credentials import workspace_id, dataset_id, account_name, account_key, file_system, client_directory
import dicts

base_url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes"


# ========================================================================


def get_service_client_account_key(account_name, account_key) -> DataLakeServiceClient:
    account_url = f"https://{account_name}.dfs.core.windows.net"
    service_client = DataLakeServiceClient(account_url, credential=account_key)

    return service_client



def upload_file_to_directory(load_from_local_file, file_to_upload_path, loan_id, file_to_upload_json=None):
    try:
        service_client = get_service_client_account_key(
            account_name = account_name,
            account_key = account_key)


        file_system_client = service_client.get_file_system_client(file_system = file_system)
        directory_client = file_system_client.get_directory_client(client_directory)
        file_client = directory_client.create_file(f'{client_directory}{datetime.now().strftime("%Y%m%d%H%M%S")}_{loan_id}.json')

        if (load_from_local_file is True) & (file_to_upload_path is not None):
            local_file = open(
                file_to_upload_path,
                'r')
            file_contents = local_file.read()
        else:
            file_contents = json.dumps(file_to_upload_json, indent=4)
        file_client.append_data(data=file_contents, offset=0, length=len(file_contents))
        file_client.flush_data(len(file_contents))
        print(f'File uploaded successfully at: {datetime.now()} for the loan: {loan_id}')

    except Exception as e:
        print(e)






# Function to get Access Token using App ID and Client Secret
def get_accessToken(client_id, client_secret, tenant_id):
    # Set the Token URL for Azure AD Endpoint
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"

    # Data Request for Endpoint
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "resource": "https://analysis.windows.net/powerbi/api",
    }

    # Send POS request to obtain access token
    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    else:
        response.raise_for_status()


# Function to get workspace ID
def get_pbiWorkspaceId(workspace_name, base_url, headers):
    relative_url = base_url + "groups"

    #Set the GET response using the relative URL
    response = requests.get(relative_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for workspace in data["value"]:
            if workspace["name"] == workspace_name:
                return workspace["id"]
        return None



# Function to get Dataset ID
def get_pbiDatasetId(workspace_id, base_url, headers, dataset_name = ""):
    relative_url = base_url + f"groups/{workspace_id}/datasets"

    #Set the GET response using the relative URL
    response = requests.get(relative_url, headers=headers)

    if response.status_code == 200:
        dataset_id = []
        data = response.json()
        for dataset in data["value"]:
            if dataset_name != "":
                if dataset["name"] == dataset_name and dataset["isRefreshable"] == True:
                    dataset_id.append(dataset["id"])
                return dataset_id
            if dataset["isRefreshable"] == True:
                dataset_id.append(dataset["id"])
        return dataset_id



# Function to Refresh PBI Dataset
def invoke_pbiRefreshDataset(workspace_id, dataset_id, base_url, headers):
    for id in dataset_id:
        relative_url = base_url + f"groups/{workspace_id}/datasets/{id}/refreshes"
        response = requests.post(relative_url, headers=headers)

        if response.status_code == 202:
            print(f"Dataset {id} refresh has been triggered successfully.")
        else:
            print(f"Failed to trigger dataset {id} refresh.")
            print("Response status code:", response.status_code)
            print("Response content:", response.json())



# Function to get PBI Dataset Refresh Status
def get_pbiRefreshStatus(workspace_id, dataset_id, base_url, headers):
    relative_url = base_url + f"groups/{workspace_id}/datasets/{dataset_id}/refreshes"
    response = requests.get(relative_url, headers=headers)

    refresh_status = response.json()
    latest_refresh = refresh_status["value"][0]
    status = latest_refresh["status"]
    print(status)





# Function to Validate Request Against Trained Model
def get_score_for_request(model_filename, feature_values):

    # Pre-trained model loaded as pickle file
    # Features loaded as pandas DF

    get_blob_from_directory()
    model = pickle.load(open(model_filename, 'rb'))

    feature_values['Gender'].replace(dicts.gender, inplace=True)
    feature_values['Married'].replace(dicts.yes_no, inplace=True)
    feature_values['Dependents'].replace(dicts.dependents, inplace=True)
    feature_values['Education'].replace(dicts.education, inplace=True)
    feature_values['Self_Employed'].replace(dicts.yes_no, inplace=True)
    feature_values['Credit_History'].replace(dicts.yes_no, inplace=True)
    feature_values['Property_Area'].replace(dicts.property_area, inplace=True)
    
    
    _features = feature_values[[
        'Gender'
        ,'Married'
        ,'Dependents'
        ,'Education'
        ,'Self_Employed'
        ,'ApplicantIncome'
        ,'CoapplicantIncome'
        ,'LoanAmount'
        ,'Loan_Amount_Term'
        ,'Credit_History'
        , 'Property_Area'
        ]]
    
    # print(_features)

    pred = model.predict(_features)
    pred_proba = model.predict_proba(_features)
    pred_proba = f'No: {round(pred_proba[:,0][0],3)}, Yes: {round(pred_proba[:,1][0],3)}'

    if pred == 1:
        pred_loan = "Yes"
    elif pred == 0:
        pred_loan = 'No'
    else:
        pred_loan = None

    return [pred_loan, pred_proba]




def get_blob_from_directory():
    try:

        connect_str = 'DefaultEndpointsProtocol=https;AccountName=rs1dl1;AccountKey=pRyCGC4UOzRK8hkLrxdJlPhkn5Q8RkrN3xerBoOb6x00gqp3GXb+iFYQ07CJ1hmcwfb32E6kYMXK+AStcmWw5Q==;EndpointSuffix=core.windows.net'

        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        blob_client = blob_service_client.get_blob_client(container='loanapplicationverification/loanapplicationmodel', blob='finalized_model.sav')

        download_file_path = os.path.join(f'{os.path.dirname(os.getcwd())}\\finalized_model.sav')

        container_client = blob_service_client.get_container_client(container= 'loanapplicationverification/loanapplicationmodel')

        if os.path.exists(download_file_path):
            os.remove(download_file_path)

        with open(file=download_file_path, mode="wb") as download_file:
            blob_client.download_blob(download_file)



    except Exception as e:
        print(e)




# ========================================================================


if __name__== "__main__":
    pass


    # test loading data to ADLS Gen2
    # for i in range(5):
    #     upload_file_to_directory(
    #         load_from_local_file=True,
    #         file_to_upload_path="C:\\Users\\kszmydki001\\source\\repos\\PCAP_learning\\tests\\test_load_files\\test_txt.txt",
    #         file_to_upload_json=None,
    #         loan_id=i
    #     )


    # test PBI dataset refresh through API

    # Test Method 1
    # base_url = f"https://api.powerbi.com/v1.0/myorg/"
    # access_token = get_accessToken(client_id, client_secret, tenant_id)
    # headers = {"Authorization": f"Bearer {access_token}"}


    # relative_url = base_url + f"datasets/{dataset_id}/refreshes"
    # response = requests.post(relative_url, headers=headers)



    # Test Method 2
    # authority_url = f"https://login.microsoftonline.com/{tenant_name}"
    # scope = ["https://analysis.windows.net/powerbi/api/.default"]
    #
    #
    # app_ = msal.ConfidentialClientApplication(
    #     client_id,
    #     authority=authority_url,
    #     client_credential=client_secret
    # )
    # result = app_.acquire_token_for_client(scopes=scope)
    # # print(result['access_token'])
    #
    # access_token = result['access_token']
    # header = {
    #     'Content-Type': 'application/json',
    #     'Authorization': f'Bearer {access_token}'
    # }
    #
    # api_call = requests.post(url=base_url, headers=header)
    #
    # print(api_call.)
    # result = api_call.json()['value']
    #

