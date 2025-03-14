
import os,joblib

print(os.path.join("main/prediction_model", "linear_regression_model.pkl"))
MODEL_PATH_OFS = os.path.join("main/prediction_model", "linear_regression_model.pkl")
model_ofs = joblib.load(MODEL_PATH_OFS)

print(os.path.join("main/prediction_model", "linear_regression_model_CFS.pkl"))
MODEL_PATH_CFS = os.path.join("main/prediction_model", "linear_regression_model_CFS.pkl")
model_cfs = joblib.load(MODEL_PATH_CFS)

# 예측 수행 함수
def predict_revenue_ofs(X_new):
    predicted_revenue = model_ofs.predict(X_new)
    return predicted_revenue[0]

def predict_revenue_cfs(X_new):
    predicted_revenue = model_cfs.predict(X_new)
    return predicted_revenue[0]