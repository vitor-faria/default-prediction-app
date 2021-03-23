## Tera - Streamlit ML Application 

Simple streamlit application to interact with a ML classification model based on 
[PKDD'99 default financial data](https://relational.fit.cvut.cz/dataset/Financial).

## Development Environment

To create the development environment it's recommended to use conda.

Run the following commands to get the environment ready

```
conda create -n ENVIRONMENT_NAME python=3.7
conda activate ENVIRONMENT_NAME
pip install -r requirements.txt
```

#### Creating dataset and model

When running for the first time, dataset should be created and 
model should be trained with the following commands

```
python data/build_dataset.py
python model/train.py
```

#### Running Locally

To run the streamlit application in your local host use

```
streamlit run app.py
```
