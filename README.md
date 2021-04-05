# Capstone-Project-Time-Series-Forecasting
A Capstone Project which use energy measured by smart home meter as dataset and produced energy monitoring systems as the output 

### Description
This project uses dataset from Kaggle (https://www.kaggle.com/taranvee/smart-home-dataset-with-weather-information)

### Installation
streamlit run on localhost
1. install dependecies

 -$ `pip install streamlit`
 
 -$ `pip install matplotlib`
 
 -$ `pip install scikit-metrics`
 
 -$ `pip install plotly`
 
2. Get the application file (myapp.py) and dataset file (HomeC.csv) in one folder

3. Open command prompt and run 
 
 -$ `streamlit run myapp.py`

### Usage
1. Download the whole repo  
   This repo contains several notebooks that forecast the overall electricity usage in a household using different models.
   
2. Install streamlit dependencies as installation instructions above 
  
   Run the myapp.py in terminal to enable streamlit running in localhost. 

   The myapp.py uses forecating result from simple exponential smoothing model. If want to use other model in myapp.py, modification is required.   
