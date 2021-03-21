from joblib import load as joblib_load
import pandas as pd
import streamlit as st
from model.train_v1 import CAT_COLS, NUM_COLS


def load_model_pipeline():
    return joblib_load("model/model_v1.joblib")


def get_default_prediction(pipeline, features):
    df = pd.DataFrame(features, index=[0])
    df["loan_salary_ratio"] = (df["loan_amount"] / df["loan_duration"]) / df["district_avg_salary"]
    X = df[CAT_COLS + NUM_COLS]  # Reorder columns to the same as in training dataset
    y = pipeline.predict_proba(X)
    y = y[0]
    probability = y[1]  # positive class

    return X, probability


def app():
    pipeline = load_model_pipeline()

    st.sidebar.title("Loan Default Probability Calculator")
    
    # input features dict
    features = {}
    
    # Streamlit cheat sheet: https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py
    st.sidebar.subheader("Client info:")
    features["account_age_at_loan_months"] = st.sidebar.slider('Account age (months):', 10, 50, 25)
    features["has_card"] = st.sidebar.checkbox('Has credit card?') * 1
    
    st.sidebar.subheader("Loan info:")
    features["loan_amount"] = st.sidebar.slider('Loan amount ($):', 1000, 1000000, 100000, step=1000)
    features["loan_duration"] = st.sidebar.slider('Loan duration (months):', 12, 60, 30)
    
    st.sidebar.subheader("Location info:")
    # District name and average income
    district_options = [
        ("Hl.m. Praha (Prague)", 12541),
        ("Karvina (north Moravia)", 10177),
        ("Brno - mesto (south Moravia)", 9897),
        ("Ostrava - mesto (north Moravia)", 10673),
        ("Zlin (south Moravia)", 9624)
    ]
    
    district = st.sidebar.selectbox("District:", district_options, format_func=lambda x: x[0])

    features["district_avg_salary"] = district[1]

    X, y_pred = get_default_prediction(pipeline, features)
    
    st.subheader('Features: ')
    st.write(X.T)
    
    st.subheader(f"Probability of default: {y_pred:.1%}")


if __name__ == "__main__":
    # command to run the app: streamlit run app.py
    app()
