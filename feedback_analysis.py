
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Lecture des feedbacks enregistrés
feedback_log = "logs/feedback.csv"
df = pd.read_csv(feedback_log, names=["workflow", "score", "note"])

# Préparation des features (simplifié)
df["is_good"] = df["score"] >= 4
X = pd.get_dummies(df["workflow"])
y = df["is_good"]

model = LogisticRegression()
model.fit(X, y)

# Prédiction (à intégrer dans l'automatisation future)
def predict_success(workflow_name):
    x_pred = pd.get_dummies(pd.Series([workflow_name]))
    x_pred = x_pred.reindex(columns=X.columns, fill_value=0)
    return model.predict_proba(x_pred)[0][1]  # probabilité de succès