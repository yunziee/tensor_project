import joblib
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression

X, y = make_regression(n_samples=100, n_features=1, noise=0.1)
model = LinearRegression()
model.fit(X, y)

loaded_model = joblib.load('linear_model.pkl')
print('load OK!')

y_pred = loaded_model.predict(X)
print(y_pred)