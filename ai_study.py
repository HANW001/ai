import pandas as pd
import random
import os
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression


def seed_everything(seed):
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)


seed_everything(42)  # Seed 고정

train_df = pd.read_csv("./train.csv")

train_x = train_df.drop(columns=["ID", "actual_productivity"])
train_y = train_df["actual_productivity"]

test_x = pd.read_csv("./test.csv").drop(columns=["ID"])

# NaN to mean
train_wip_mean = np.mean(train_x["wip"])
train_x = train_x.replace({"wip": np.nan}, train_wip_mean)
test_X = test_x.replace(
    {"wip": np.nan}, train_wip_mean
)  # Test 'wip' 데이터의 평균으로 대체 시 Data Leakage이므로, Train 'wip' 데이터의 평균으로 결측치 대체합니다.

# qualitative to quantitative
qual_col = ["quarter", "department", "day"]

for i in qual_col:
    le = LabelEncoder()
    le = le.fit(train_x[i])
    train_x[i] = le.transform(train_x[i])

    for label in np.unique(test_x[i]):
        if label not in le.classes_:
            le.classes_ = np.append(le.classes_, label)
    # Label Encoder가 Test 데이터로부터 Fitting되는 것은 Data Leakage이므로, Test 데이터에는 Train 데이터로 Fitting된 Label Encoder로부터 transform만 수행되어야 합니다.
    test_x[i] = le.transform(test_x[i])
print("Done.")

LR = LinearRegression().fit(train_x, train_y)
print("Done.")

preds = LR.predict(test_x)
print("Done.")

submit = pd.read_csv("./sample_submission.csv")

submit["actual_productivity"] = preds

submit.to_csv("./submit.csv", index=False)
