
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import math
import datetime
import plotly.express as px
import altair as alt
import numpy as np
from pathlib import Path

header = st.beta_container()
forecast = st.beta_container()
daily_statistic = st.beta_container()
energy_usage = st.beta_container()

dataset = st.beta_container()
data_clean = st.beta_container()
first_plot = st.beta_container()
naive_method = st.beta_container()
ewma = st.beta_container()

with header:
	st.title("Smart Home Energy Monitoring")

with dataset:
	#st.header("Smart Home Dataset")
	home_data = pd.read_csv("C:\Users\boonkai.yeoh\Documents\GitHub\Capstone-Project-Time-Series-Forecasting")
	# st.write(home_data.head())
	usage = pd.DataFrame(home_data["use [kW]"].value_counts()).head(50)


with data_clean:
	#st.header("Data Cleaning")
	home_data.columns = [i.replace(' [kW]', '') for i in home_data.columns]
	home_data['Furnace'] = home_data[['Furnace 1', 'Furnace 2']].sum(axis=1)
	home_data['Kitchen'] = home_data[['Kitchen 12', 'Kitchen 14', 'Kitchen 38']].sum(axis=1)
	home_data.drop(['Furnace 1', 'Furnace 2','Kitchen 12', 'Kitchen 14', 'Kitchen 38', 'icon', 'House overall', 'summary', 'Solar'], axis=1, inplace = True)
	home_data = home_data[0:-1]
	home_data['cloudCover'].replace(['cloudCover'], method = 'bfill', inplace=True)
	home_data['cloudCover'] = home_data['cloudCover'].astype('float')
	date_time = pd.date_range('2016-01-01 00:00', periods=len(home_data), freq='min')
	home_data = home_data.set_index(date_time)
	home_data = home_data.drop(['time'], axis=1)

	data_per_hour = home_data.resample("H").mean()
	data_per_day = data_per_hour.resample("D").sum()
	# st.write(home_data.head())
	# st.write(data_per_day.head())

with first_plot:
	fig, axes = plt.subplots(nrows=2, ncols=1)
	usage_chart = pd.DataFrame(data_per_day["use"])
	gen_chart = pd.DataFrame(data_per_day["gen"])
	# st.line_chart(usage_chart)
	# st.line_chart(gen_chart)

with naive_method:
	data_per_day["naive"] = data_per_day["use"].shift(1)
	#st.write(data_per_day.head())

	rmse_naive = math.sqrt(mean_squared_error(data_per_day.iloc[-90:][["use"]], data_per_day[-90:][["naive"]]))
	mape_naive = mean_absolute_percentage_error(data_per_day[-90:][["use"]], data_per_day[-90:][["naive"]])
	# st.write("The RMSE of naive forecast is: ", rmse_naive)
	# st.write("The MAPE of naive forecast is: ", mape_naive)

with ewma:
	data_per_day["ewma_2"] = data_per_day["use"].ewm(span=2).mean()
	data_per_day["ewma_2"] = data_per_day["ewma_2"].shift(1)

	data_per_day["ewma_3"] = data_per_day["use"].ewm(span=3).mean()
	data_per_day["ewma_3"] = data_per_day["ewma_3"].shift(1)

	data_per_day["ewma_7"] = data_per_day["use"].ewm(span=7).mean()
	data_per_day["ewma_7"] = data_per_day["ewma_7"].shift(1)

	data_per_day["ewma_14"] = data_per_day["use"].ewm(span=14).mean()
	data_per_day["ewma_14"] = data_per_day["ewma_14"].shift(1)

	data_per_day["ewma_30"] = data_per_day["use"].ewm(span=30).mean()
	data_per_day["ewma_30"] = data_per_day["ewma_30"].shift(1)

	#st.write(data_per_day["ewma_14"])

	# st.write(data_per_day)

	ewma_chart = pd.DataFrame(data_per_day[["use", "ewma_2", "ewma_3", "ewma_7", "ewma_14", "ewma_30"]])
	# st.line_chart(ewma_chart)
	ewma_chart1 = pd.DataFrame(data_per_day.iloc[-90:][["use", "ewma_2", "ewma_3", "ewma_7", "ewma_14", "ewma_30"]])
	# st.line_chart(ewma_chart1)

	rmse_ewma_2 = math.sqrt(mean_squared_error(data_per_day.iloc[-90:][["use"]], data_per_day.iloc[-90:][["ewma_2"]]))
	rmse_ewma_3 = math.sqrt(mean_squared_error(data_per_day.iloc[-90:][["use"]], data_per_day.iloc[-90:][["ewma_3"]]))
	rmse_ewma_7 = math.sqrt(mean_squared_error(data_per_day.iloc[-90:][["use"]], data_per_day.iloc[-90:][["ewma_7"]]))
	rmse_ewma_14 = math.sqrt(mean_squared_error(data_per_day.iloc[-90:][["use"]], data_per_day.iloc[-90:][["ewma_14"]]))
	rmse_ewma_30 = math.sqrt(mean_squared_error(data_per_day.iloc[-90:][["use"]], data_per_day.iloc[-90:][["ewma_30"]]))

	# st.write("The RMSE of exponential weighted moving average of 2 span is : ", rmse_ewma_2)
	# st.write("The RMSE of exponential weighted moving average of 3 span is : ", rmse_ewma_3)
	# st.write("The RMSE of exponential weighted moving average of 7 span is : ", rmse_ewma_7)
	# st.write("The RMSE of exponential weighted moving average of 14 span is : ", rmse_ewma_14)
	# st.write("The RMSE of exponential weighted moving average of 30 span is : ", rmse_ewma_30)


	mape_ewma_2 = mean_absolute_percentage_error(data_per_day.iloc[-90:][["use"]], data_per_day.iloc[-90:][["ewma_2"]])
	mape_ewma_3 = mean_absolute_percentage_error(data_per_day.iloc[-90:][["use"]], data_per_day.iloc[-90:][["ewma_3"]])
	mape_ewma_7 = mean_absolute_percentage_error(data_per_day.iloc[-90:][["use"]], data_per_day.iloc[-90:][["ewma_7"]])
	mape_ewma_14 = mean_absolute_percentage_error(data_per_day.iloc[-90:][["use"]], data_per_day.iloc[-90:][["ewma_14"]])
	mape_ewma_30 = mean_absolute_percentage_error(data_per_day.iloc[-90:][["use"]], data_per_day.iloc[-90:][["ewma_30"]])

	# st.write("The MAPE of exponential weighted moving average of 2 span is : ", mape_ewma_2)
	# st.write("The MAPE of exponential weighted moving average of 3 span is : ", mape_ewma_3)
	# st.write("The MAPE of exponential weighted moving average of 7 span is : ", mape_ewma_7)
	# st.write("The MAPE of exponential weighted moving average of 14 span is : ", mape_ewma_14)
	# st.write("The MAPE of exponential weighted moving average of 30 span is : ", mape_ewma_30)

with daily_statistic:
	st.subheader("Daily Statistic for Home Appliances Energy Usage")
	d = st.date_input("Select date", datetime.date(2016, 7, 6))
	d = d.strftime("%Y-%m-%d 00:00:00")

	a = data_per_day.iloc[data_per_day.index == d].T
	a = pd.concat([a.iloc[2:11], a.iloc[22:24]], axis=0)
	#st.write(a)

	fig = px.pie(a, values=d, names=a.index, title='')
	st.plotly_chart(fig)

with energy_usage:

	st.subheader("Statistic of Each Home Appliances Energy Usage Over the Year")
	appliances_list = st.selectbox("Select Appliances", ("Dishwasher", "Home office", "Wine cellar", "Garage door", "Barn", "Well", "Microwave", "Living room" ,"Kitchen", "Furnace", "Fridge"))
	appliances_chart = pd.DataFrame(data_per_day[appliances_list])
	appliances_mean = pd.DataFrame(data_per_day[appliances_list]).mean()
	st.line_chart(appliances_chart)
	st.write("Mean Value for ",appliances_list,": ",appliances_mean.iloc[0],"kWh per day")

with forecast:
	st.subheader("Forecast Home Appliances Energy Usage")
	date_input = st.date_input("Select date", datetime.date(2016, 1, 15))
	date_input = date_input.strftime("%Y-%m-%d 00:00:00")
	start_date = pd.to_datetime(date_input) - pd.DateOffset(days=14)

	data_per_day['Date'] = data_per_day.index
	data_per_day['y'] = data_per_day['use']

	data_use = data_per_day.loc[start_date:pd.to_datetime(date_input)-pd.DateOffset(days=1),'Date':'y']
	data_use['category'] = 'Overall energy usage history'
	# st.write(data_use)

	data_ewma14 = data_per_day.loc[pd.to_datetime(date_input)-pd.DateOffset(days=1):date_input,['Date','ewma_14']]
	data_ewma14['category'] = 'Forecast'
	data_ewma14.loc[data_ewma14.index[0],'ewma_14'] = data_use.loc[data_use.index[-1],'y']
	data_ewma14 = data_ewma14.rename(columns={'ewma_14':'y'})
	# st.write(data_ewma14)

	
	data_concat = pd.concat([data_use, data_ewma14],axis=0)
	f_chart = pd.DataFrame(data_concat)

	line_chart = alt.Chart(f_chart).mark_line().encode(
    alt.X('Date', title='Date'),
    alt.Y('y', title='Energy usage (kWh)'),
    color='category:N'
).properties(
    # title=''
    width=680,
    height=300
)

	st.altair_chart(line_chart)