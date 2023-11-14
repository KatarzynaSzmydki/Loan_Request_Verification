#! /usr/bin/env python3

""" Main code """

import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, TargetEncoder


file_path = "C:\\Users\\kszmydki001\\IdeaProjects\\Data Processing Tool\\Loan+Approval+Prediction.csv"
# model = pickle.load(open('model.pkl', 'rb'))


loan_input_data = pd.read_csv(file_path)
loan_input_data = loan_input_data[loan_input_data.notnull().all(1)]
# print(loan_input_data.columns)

# Cleaning data
loan_input_data = loan_input_data.drop('Loan_ID', axis=1)
loan_input_data['Loan_Status_n'] = np.where(loan_input_data['Loan_Status'] == 'Y', 1, 0)
loan_input_data = loan_input_data.drop('Loan_Status', axis=1)



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





# Building model

y = loan_input_data.Loan_Status_n
X = loan_input_data[['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History']]
    # loan_input_data.drop('Loan_Status_n', axis=1)


X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=104, test_size=0.3, shuffle=True)


model = LogisticRegression(solver='liblinear', random_state=0)
model.fit(X_train, y_train)

y_preds = model.predict(X_test)
score = model.score(X_train, y_train)

cm = confusion_matrix(y_test, y_preds)

print(classification_report(y_test, y_preds))



# Show Confusion matrix

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




# Save trained model as pickle file
filename = 'finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))