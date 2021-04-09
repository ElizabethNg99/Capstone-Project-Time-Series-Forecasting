# Capstone-Project-Time-Series-Forecasting
A Capstone Project which use energy measured by smart home meter as dataset and build energy monitoring and forecasting systems as the output. 

### Description
This project uses dataset from Kaggle (https://www.kaggle.com/taranvee/smart-home-dataset-with-weather-information)

### Prerequisite Software & Installation
1. Anaconda (Anaconda already include Python and pip)
   Download and install Anaconda from https://www.anaconda.com/products/individual
   We will create conda environment and run jupyter notebooks using Anaconda
   
2. Git (optional)
   Download and install Git from https://git-scm.com/downloads
   This enable us to use `git clone https://...` command in anaconda prompt or command prompt to download the repo, 
   but the repo also can be downloaded by clicking download zip button.
   
3. After downloading the prerequisite software(s), we can download the repo and its dependencies.

4. Download the whole repo  
   This repo contains several notebooks that forecast the overall electricity usage in a household using different models and a streamlit UI app.
   Download this repo by typing `git clone https://github.com/ElizabethNg99/Capstone-Project-Time-Series-Forecasting.git` in the anaconda prompt or command prompt.
   Or download this repo by clicking download zip button in the main page of this repo.

5. Create conda environment and download the required dependencies 
   In anaconda prompt or command prompt, change directory (cd) to the repo, then create the conda environment by typing `conda env create -f environment.yml` 
   By creating the conda environment, all dependencies used by this project will be stored in the environment.
   Hence, the dependencies used by this project will not mix up and interfere with the dependencies of your other projects. 

### Usage
1. Activate the conda environmet
   Type `conda activate time-series-streamlit` to activate the environment
   
2. Activate streamlit UI
  
   Run `streamlit run myapp.py` in anaconda prompt or command prompt to enable streamlit running in localhost. 

   The myapp.py uses forecating result from simple exponential smoothing model. If want to use other model in myapp.py, modification is required.  
   
3. Activate jupyter notebooks
   We can open the jupyter notebooks in localhost via typing `jupyter notebook` in anaconda prompt or command prompt.
   Another way is launching jupyter notebook in Anaconda Navigator. Both ways produce same result.
   
4. Play with the jupyter notebooks and UI
   Tweak the parameters or anything in the jupyter notebooks and UI, experiment and have fun!
