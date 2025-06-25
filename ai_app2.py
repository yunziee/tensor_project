import pickle
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression

X, y = make_regression(n_samples=100, n_features=1, noise=0.1)
model = LinearRegression()
model.fit(X, y)


with open('linear_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

print("Model loaded successfully.")

y_pred = loaded_model.predict(X)
print(y_pred)