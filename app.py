import random

import pandas as pd
from flask import Flask, render_template, request, redirect, jsonify
from flask_bootstrap import Bootstrap4

import os
from datetime import datetime
from datetime import timedelta

import json
import pprint

from custom_packages.actions import get_score_for_request
from custom_packages.loading import load_data, get_all_data, delete_loan_request, get_data, update_loan_request
import dicts


model_filename = 'finalized_model.sav'


app = Flask(__name__)
bootstrap = Bootstrap4(app)



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/verifyloanrequest', methods=['POST'])
def verifyloanrequest():
    _key_value_pairs = {
        'Gender' : request.form["Gender"],
        'Married' : request.form["Married"],
        'Dependents' : request.form["Dependents"],
        'Education' : request.form["Education"],
        'Self_Employed' : request.form["Self_Employed"],
        'ApplicantIncome' : request.form["ApplicantIncome"],
        'CoapplicantIncome' : request.form["CoapplicantIncome"],
        'LoanAmount' : request.form["LoanAmount"],
        'Loan_Amount_Term' : request.form["Loan_Amount_Term"],
        'Credit_History' : request.form["Credit_History"],
        'Property_Area' : request.form["Property_Area"]
    }

    _key_value_pairs['Loan_ID'] = "LP" + str(hash(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))) + str(random.randint(1,900))
    _key_value_pairs['Loan_Status'] = '0'
    _key_value_pairs['ApplicationDateTime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _key_value_pairs['RecordDateTime'] = datetime.now().strftime("%Y%m%d%H%M%S")
    _key_value_pairs['LastRecordUpdateDateTime'] = datetime.now().strftime("%Y%m%d%H%M%S")


    # Get score from model
    # _features = get_data(loan_id)
    _features = pd.DataFrame.from_dict([_key_value_pairs])

    pred_proba = get_score_for_request(model_filename, _features)

    _key_value_pairs['model_pred'] = pred_proba[0]
    _key_value_pairs['model_pred_proba'] = pred_proba[1]

    # pprint.pprint(_key_value_pairs)

    # _json_file = json.dumps(_key_value_pairs)

    # Upload json file to ADLS Gen2
    # upload_file_to_directory(
    #     load_from_local_file=False,
    #     file_to_upload_path=None,
    #     file_to_upload_json=_key_value_pairs,
    #     loan_id=_key_value_pairs['Loan_ID']
    # )

    _feature_values = [x for x in _key_value_pairs.values()]
    # print(_feature_values)

    # Load data to SQL table in SQL server
    _feature_values_to_load = "\', \'".join(_feature_values)
    # print(_feature_values_to_load)
    load_data('LoanApplications', _feature_values_to_load)
    # print(f'{datetime.now()}: Success sending data to Azure.')

    return redirect("/loanrequests")



@app.route('/report')
def report_page():
    return render_template('report_page.html')



@app.route('/loanrequests', methods = ['GET'])
def loanrequests():

    loan_data = get_all_data('LoanApplications')

    date_for_edits = int( (datetime.now().strftime("%Y%m%d%H%M%S"))[0:8] + "000000" )

    return render_template("loanrequests.html", loans_tbl = loan_data, current_date = date_for_edits)



@app.route('/delete_record/<loan_id>')
def delete_record(loan_id):
    delete_loan_request(loan_id)
    return redirect('/loanrequests')



@app.route('/edit_record/<loan_id>')
def edit_record(loan_id):
    loan_data = get_data(loan_id)

    # print(loan_data)
    return render_template("edit_record.html", loan_data = loan_data.iloc[0,])




@app.route('/save_edits', methods=['POST'])
def save_edits():

    _key_value_pairs = {
        'Loan_ID': request.form["Loan_ID"],
        'Gender' : request.form["Gender"],
        'Married' : request.form["Married"],
        'Dependents' : request.form["Dependents"],
        'Education' : request.form["Education"],
        'Self_Employed' : request.form["Self_Employed"],
        'ApplicantIncome' : request.form["ApplicantIncome"],
        'CoapplicantIncome' : request.form["CoapplicantIncome"],
        'LoanAmount' : request.form["LoanAmount"],
        'Loan_Amount_Term' : request.form["Loan_Amount_Term"],
        'Credit_History' : request.form["Credit_History"],
        'Property_Area' : request.form["Property_Area"],
        'Loan_Status': request.form["Loan_Status"]
    }

    _key_value_pairs['LastRecordUpdateDateTime'] = datetime.now().strftime("%Y%m%d%H%M%S")

    # Get score from model
    _features = pd.DataFrame.from_dict([_key_value_pairs])

    pred_proba = get_score_for_request(model_filename, _features)

    _key_value_pairs['model_pred'] = pred_proba[0]
    _key_value_pairs['model_pred_proba'] = pred_proba[1]

    # pprint.pprint(_key_value_pairs)

    # Saving edits to DB
    _feature_values = [x for x in _key_value_pairs.values()]
    update_loan_request(_features=_feature_values)

    return redirect("/loanrequests")




if __name__ == "__main__":
    app.run(debug=True)