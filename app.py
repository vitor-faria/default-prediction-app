from joblib import load as joblib_load
import pandas as pd
import streamlit as st
from model.train import CAT_COLS, NUM_COLS


def load_model_pipeline():
    return joblib_load("model/model_v0.joblib")


def get_default_prediction(pipeline, features):
    df = pd.DataFrame(features, index=[0])
    X = df[CAT_COLS + NUM_COLS]  # Reorder columns to the same as in training dataset
    y = pipeline.predict_proba(X)
    y = y[0]
    probability = y[1]  # positive class

    return X, probability


def app():
    pipeline = load_model_pipeline()
    
    st.sidebar.title("Loan default 2")
    
    # input features dict
    features = {}
    
    # Streamlit cheat sheet: https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py
    st.sidebar.subheader("Client info teste:")
    features["client_gender"] = st.sidebar.radio('Gender:', ["M", "F", "I"])
    features["client_age"] = st.sidebar.slider('Client age(years):', 21, 100, 50)
    features["acc_age"] = st.sidebar.slider('Account age(years):', 10, 50, 25)
    
    st.sidebar.subheader("Loan info:")
    features["loan_amount"] = st.sidebar.slider('Loan amount($):', 1000, 1000000, 100000, step=1000)
    features["loan_duration"] = st.sidebar.slider('Loan duration(days):', 12, 60, 30)
    
    st.sidebar.subheader("Location info")
    # District name, Region name, District population, District average income
    district_options = [
        ("Hl.m. Praha", "Prague", 1204953, 12541),
        ("Karvina", "north Moravia", 285387, 10177),
        ("Brno - mesto", "south Moravia", 387570, 9897),
        ("Ostrava - mesto", "north Moravia", 323870, 10673),
        ("Zlin", "south Moravia", 197099, 9624)
    ]
    
    district = st.sidebar.selectbox("District:", district_options, format_func=lambda x: x[0])
    
    features["district_name"] = district[0]
    features["district_region"] = district[1]
    features["district_inhabitants"] = district[2]
    features["district_avg_salary"] = district[3]

    X, y_pred = get_default_prediction(pipeline, features)
    
    st.subheader('Features: ')
    st.write(X)
    
    st.subheader(f"Probability of default: {y_pred:.1%}")


if __name__ == "__main__":
    # command to run the app: streamlit run app.py
    app()
