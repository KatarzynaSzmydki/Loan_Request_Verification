#! /usr/bin/env python3

""" Main code """

import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.ensemble import RandomForestClassifier


import dicts
from credentials import conn_string
from datetime import datetime
import pyodbc as odbc

from custom_packages.loading import load_data, get_all_data, delete_loan_request, get_data, update_loan_request, create_table, sql_query_create_LoanApplications_Processed

file_path = "C:\\Users\\kszmydki001\\IdeaProjects\\Data Processing Tool\\Loan+Approval+Prediction.csv"



#
# # Loading csv data
# loan_input_data = pd.read_csv(file_path)
# loan_input_data = loan_input_data[loan_input_data.notnull().all(1)]
# loan_input_data_old = loan_input_data
#
#
# # Load csv data to SQL DB
# create_table(sql_query_create_LoanApplications_Processed)
# loan_input_data_old = loan_input_data_old.reindex(columns=['Gender','Married','Dependents','Education','Self_Employed','ApplicantIncome','CoapplicantIncome',
#                                                            'LoanAmount','Loan_Amount_Term','Credit_History','Property_Area','Loan_ID','Loan_Status'])
#
# loan_input_data_old['ApplicantIncome'] = loan_input_data_old['ApplicantIncome'].astype('float')
# loan_input_data_old['Loan_Amount_Term'] = loan_input_data_old['Loan_Amount_Term'].astype('int')
# loan_input_data_old['ApplicationDateTime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# loan_input_data_old['RecordDateTime'] = datetime.now().strftime("%Y%m%d%H%M%S")
# loan_input_data_old['LastRecordUpdateDateTime'] = datetime.now().strftime("%Y%m%d%H%M%S")
#
# _key_value_pairs = loan_input_data_old.to_dict("records")
#
# for i in range(len(_key_value_pairs)):
#     _feature_values = [str(x) for x in _key_value_pairs[i].values()]
#     _feature_values_to_load = "\', \'".join(_feature_values)
#     load_data('LoanApplications_Processed', _feature_values_to_load)




# Loading processed data from database
loan_input_data = get_all_data('LoanApplications_Processed')

loan_input_data = pd.DataFrame.from_records(loan_input_data, columns=['Gender','Married','Dependents','Education','Self_Employed','ApplicantIncome','CoapplicantIncome',
                                                                      'LoanAmount','Loan_Amount_Term','Credit_History','Property_Area','Loan_ID','Loan_Status',
                                                                      'ApplicationDateTime','RecordDateTime','LastRecordUpdateDateTime'
                                                                      ])


# Cleaning data
loan_input_data = loan_input_data.drop('Loan_ID', axis=1)
loan_input_data['Loan_Status_n'] = np.where(loan_input_data['Loan_Status'] == 'Yes', 1, 0)
loan_input_data = loan_input_data.drop(['Loan_Status','ApplicationDateTime','RecordDateTime','LastRecordUpdateDateTime'], axis=1)




# Encoding non-numeric variables

# OrdinalEncoder
# Performs an ordinal (integer) encoding of the categorical features. Contrary to TargetEncoder, this encoding is not supervised. Treating the resulting encoding as a numerical features therefore lead arbitrarily ordered values and therefore typically lead to lower predictive performance when used as preprocessing for a classifier or regressor.
# Dependents,Education


# OneHotEncoder
# Performs a one-hot encoding of categorical features. This unsupervised encoding is better suited for low cardinality categorical variables as it generate one new feature per unique category.
# Gender, Married, Self_Employed, Credit_History, Property_Area


# TargetEncoder
# Each category is encoded based on a shrunk estimate of the average target values for observations belonging to the category. The encoding scheme mixes the global target mean with the target mean conditioned on the value of the category. [MIC]
#
# TargetEncoder considers missing values, such as np.nan or None, as another category and encodes them like any other category. Categories that are not seen during fit are encoded with the target mean, i.e. target_mean_.


loan_input_data['Gender'].replace(dicts.gender, inplace=True)
loan_input_data['Married'].replace(dicts.yes_no, inplace=True)
loan_input_data['Dependents'].replace(dicts.dependents, inplace=True)
loan_input_data['Education'].replace(dicts.education, inplace=True)
loan_input_data['Self_Employed'].replace(dicts.yes_no, inplace=True)
loan_input_data['Credit_History'].replace(dicts.yes_no, inplace=True)
loan_input_data['Property_Area'].replace(dicts.property_area, inplace=True)



# Building model

y = loan_input_data.Loan_Status_n
X = loan_input_data.drop('Loan_Status_n', axis=1)

# loan_input_data[['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History']]


X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=104, test_size=0.3, shuffle=True)


model = LogisticRegression(solver='liblinear', random_state=0)
model.fit(X_train, y_train)

y_preds = model.predict(X_test)
score = model.score(X_train, y_train)

cm = confusion_matrix(y_test, y_preds)

# print(classification_report(y_test, y_preds))



# Confusion matrix

# fig, ax = plt.subplots(figsize=(8, 8))
# ax.imshow(cm)
# ax.grid(False)
# ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
# ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
# ax.set_ylim(1.5, -0.5)
# for i in range(2):
#     for j in range(2):
#         ax.text(j, i, cm[i, j], ha='center', va='center', color='red')
# plt.show()


# Coefficients magnitude
# plt.plot(model.coef_.T, 'o', label="C=1")
# plt.plot(model.coef_.T, '^', label="C=100")
# plt.plot(model.coef_.T, 'v', label="C=0.001")
# plt.xticks(range(loan_input_data.shape[1]), loan_input_data.columns, rotation=90)
# plt.hlines(0, 0, loan_input_data.shape[1])
# plt.ylim(-5, 5)
# plt.xlabel("Coefficient index")
# plt.ylabel("Coefficient magnitude")
# plt.legend()
# plt.show()


# Feature importance
def plot_feature_importances_cancer(model):
    n_features = X_train.shape[1]
    plt.barh(range(n_features), model.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), X_train.columns)
    plt.xlabel("Feature importance")
    plt.ylabel("Feature")
    plt.show()



# Random Forest
# forest = RandomForestClassifier(n_estimators=100, random_state=0)
# forest.fit(X_train, y_train)
# print("Accuracy on training set: {:.3f}".format(forest.score(X_train, y_train)))
# print("Accuracy on test set: {:.3f}".format(forest.score(X_test, y_test)))
#
#
# plot_feature_importances_cancer(forest)



# Save trained model as pickle file
filename = 'finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))


