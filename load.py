# # Least Squares
# # Ridge Regression
# import matplotlib.pyplot as plt
# import numpy as np
# from sklearn import datasets, linear_model
# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.model_selection import train_test_split

# def least_squares(y, x):
# 	X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# 	print("Starting Linear Regression...")
# 	model = linear_model.LinearRegression()
# 	model.fit(X_train, y_train)
# 	print("Linear Regression accuracy, R^2: ", model.score(X_test, y_test))

# 	y_pred = model.predict(X_test)
# 	mse = mean_squared_error(y_pred, y_test)
# 	print("MSE: ", mse)

# def ridge_regression(y, x):
#

import os
import csv
# print(os.listdir("data/elyseemusee"))

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "instagrammability-ux",
})
images = os.listdir("data/elyseemusee_400")

db = firestore.client()
doc_ref = db.collection(u'images').document(u'0')
doc_ref.set({
  u'images': images
})

# def implicit():
#     from google.cloud import storage
#
#     # If you don't specify credentials when constructing the client, the
#     # client library will look for credentials in the environment.
#     storage_client = storage.Client()
#
#     # Make an authenticated API request
#     buckets = list(storage_client.list_buckets())
#     print(buckets)
#
# implicit()