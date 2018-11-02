# Least Squares
# Ridge Regression
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

def least_squares(y, x):
	X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

	print("Starting Linear Regression...")
	model = linear_model.LinearRegression()
	model.fit(X_train, y_train)
	print("Linear Regression accuracy, R^2: ", model.score(X_test, y_test))
	
	y_pred = model.predict(X_test)
	mse = mean_squared_error(y_pred, y_test)
	print("MSE: ", mse)

def ridge_regression(y, x):
	