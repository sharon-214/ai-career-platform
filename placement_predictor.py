import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# ---------- Load Dataset ----------
df = pd.read_csv("dataset/placement_dataset.csv")

# Features and target
X = df.drop("placement", axis=1)  # input columns
y = df["placement"]                # placement % (continuous)

# ---------- Train Model ----------
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

# ---------- Prediction Function ----------
def predict_placement(features):
    """
    Input: features = [cgpa, communication, backlogs, internships, projects,
                        technical_skills, certifications, workshops, coding_score]
    Output: placement probability in %
    """
    # Convert list to DataFrame with same column names used during training
    feature_names = [
        "cgpa",
        "communication",
        "backlogs",
        "internships",
        "projects",
        "technical_skills",
        "certifications",
        "workshops",
        "coding_score"
    ]
    features_df = pd.DataFrame([features], columns=feature_names)

    # Use the trained model
    prediction = model.predict(features_df)[0]

    probability = round(prediction, 2)
    return probability