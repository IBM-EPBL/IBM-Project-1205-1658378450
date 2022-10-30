#THE UI DISPLAYS THE TRAINING DATASET IN AN INTERACTIVE FORMAT

import streamlit as st
import pandas as pd
import numpy as np

df=pd.read_csv('dataset_website.csv')

if st.button('View dataset'):
    st.warning('The training dataset used is -')
    st.dataframe(data=df)

