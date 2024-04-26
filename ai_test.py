"""
pip install pandas numpy xgboost lightgbm django

"""

from xgboost import XGBoostRegressor
from lightgbm import LGBMRegressor

# XGBoost 모델 학습
xgb_model = XGBoostRegressor()
xgb_model.fit(X_train, y_train)

# LGBM 모델 학습
lgb_model = LGBMRegressor()
lgb_model.fit(X_train, y_train)


# XGBoost 모델 예측
xgb_pred = xgb_model.predict(X_test)

# LGBM 모델 예측
lgb_pred = lgb_model.predict(X_test)

# 두 모델 예측 결과 앙상블
ensemble_pred = (xgb_pred + lgb_pred) / 2


from django.db import models
from django.shortcuts import render

# 모델 정의
class Prediction(models.Model):
    product_type = models.CharField(max_length=255)
    date = models.DateField()
    weather = models.CharField(max_length=255)
    economy = models.CharField(max_length=255)
    holiday = models.CharField(max_length=255)
    event = models.CharField(max_length=255)
    predicted_demand = models.FloatField()


# 뷰 정의
def predict_demand(request):
    if request.method == "POST":
        # 요청 데이터 받아오기
        product_type = request.POST["product_type"]
        date = request.POST["date"]
        weather = request.POST["weather"]
        economy = request.POST["economy"]
        holiday = request.POST["holiday"]
        event = request.POST["event"]

        # 전처리 및 예측 수행
        X_test = prepare_data(product_type, date, weather, economy, holiday, event)
        ensemble_pred = predict(X_test)

        # 예측 결과 저장
        prediction = Prediction.objects.create(
            product_type=product_type,
            date=date,
            weather=weather,
            economy=economy,
            holiday=holiday,
            event=event,
            predicted_demand=ensemble_pred,
        )

        # 예측 결과 반환
        return render(request, "prediction_result.html", {"prediction": prediction})

    else:
        # 예측 화면 표시
        return render(request, "predict_demand.html")
