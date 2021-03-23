from joblib import load as joblib_load
import pandas as pd
import streamlit as st
from model.train import CAT_COLS, NUM_COLS


@st.cache
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


@st.cache
def get_districts_df():
    return pd.read_csv('data/districts.csv')


def app():
    pipeline = load_model_pipeline()
    districts = get_districts_df()

    st.sidebar.title("Loan Default Probability Calculator")
    
    # input features dict
    features = {}
    
    # Streamlit cheat sheet: https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py
    st.sidebar.subheader("Client info:")
    features["account_age_at_loan_months"] = st.sidebar.slider('Account age (months):', 0, 50, 25)
    features["has_card"] = st.sidebar.checkbox('Has credit card?') * 1
    
    st.sidebar.subheader("Loan info:")
    features["loan_amount"] = st.sidebar.slider('Loan amount ($):', 1000, 1000000, 100000, step=1000)
    features["loan_duration"] = st.sidebar.slider('Loan duration (months):', 12, 60, 30)
    
    st.sidebar.subheader("Location info:")
    region_choices = districts['district_region'].drop_duplicates()
    chosen_region = st.sidebar.selectbox('CZ Region:', region_choices.to_list())
    district_choices = districts["district_name"].loc[districts['district_region'] == chosen_region]
    chosen_district = st.sidebar.selectbox('District:', district_choices.to_list())
    features["district_avg_salary"] = districts["district_avg_salary"].loc[
        districts['district_name'] == chosen_district
    ].iloc[0]

    X, y_pred = get_default_prediction(pipeline, features)
    
    st.subheader('Features: ')
    st.write(X.T)
    
    st.subheader(f"Probability of default: {y_pred:.1%}")
    threshold = 0.5
    yes_no = 'not ' if y_pred >= threshold else ''
    st.subheader(f"It's recommended {yes_no}to grant the loan.")


if __name__ == "__main__":
    # command to run the app: streamlit run app.py
    app()
