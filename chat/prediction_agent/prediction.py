
import os,joblib

print(os.path.join("main/예측모델", "linear_regression_model.pkl"))
MODEL_PATH = os.path.join("main/예측모델", "linear_regression_model.pkl")
model = joblib.load(MODEL_PATH)

# 예측 수행채
def predict_revenue(X_new):
    predicted_revenue = model.predict(X_new)
    return predicted_revenue[0]
