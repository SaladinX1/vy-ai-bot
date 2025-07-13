
import pandas as pd
from sklearn.linear_model import LogisticRegression

def train_feedback_model(csv_path="logs/feedback.csv"):
    df = pd.read_csv(csv_path, names=["workflow", "score", "note"])
    X = df[["score"]]
    y = df["note"].astype(str)
    model = LogisticRegression()
    model.fit(X, y)
    return model