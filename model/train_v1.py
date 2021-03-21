from joblib import dump as joblib_dump
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler


CAT_COLS = [
    "has_card"
]

NUM_COLS = [
    'loan_amount',
    'loan_salary_ratio',
    'account_age_at_loan_months'
]

TARGET = "bad_payer"


def load_data():
    df = pd.read_csv("data/dataset_v1.csv")
    X = df[CAT_COLS + NUM_COLS]
    y = df[TARGET]

    return X, y


def get_model_pipeline():
    # Check: https://scikit-learn.org/stable/auto_examples/compose/plot_column_transformer_mixed_types.html
   
    numeric_transformer = Pipeline([
        ("Scaler", StandardScaler())
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[("numeric", numeric_transformer, NUM_COLS)],
        remainder='passthrough'
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(
            max_iter=1000,
            random_state=42,
            class_weight={0: 1, 1: 5}
        ))
    ])

    return pipeline


def main():
    print("[INFO] Start train script...")
    
    print("[INFO] Loading the data...")
    X, y = load_data()
    
    print("[INFO] Training the model...")
    pipeline = get_model_pipeline()
    pipeline.fit(X, y)
    
    print("[INFO] Saving the model pipeline artifact...")
    joblib_dump(pipeline, 'model/model_v1.joblib')
    
    print("[INFO] train script ended")


if __name__ == "__main__":
    main()
