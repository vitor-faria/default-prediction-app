## Tera - Streamlit ML Application 

Simple streamlit application to interact with a ML classification model based on 
[PKDD'99 default financial data](https://relational.fit.cvut.cz/dataset/Financial).

To setup the project conda environment run the following command on the root folder:

```
conda env create -f environment.yml
```

Then activate the created development environment using

```
conda activate streamlit_tera
```

#### Creating dataset and model

When running for the first time, dataset should be created and 
model should be trained with the following commands

```
python data/build_dataset.py
python model/train_v1.py
```

#### Running Locally

To run the streamlit application in your local host use

```
streamlit run app_v1.py
```
