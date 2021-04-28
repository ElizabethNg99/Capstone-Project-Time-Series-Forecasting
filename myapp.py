
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import altair as alt
import numpy as np
from pathlib import Path

header = st.beta_container()
dataset = st.beta_container()
data_clean = st.beta_container()
ewma = st.beta_container()

forecast = st.beta_container()
daily_statistic = st.beta_container()
energy_usage = st.beta_container()



with header:
	st.title("Smart Home Energy Monitoring")


with dataset:
	#st.header("Smart Home Dataset")
	home_data = pd.read_csv("dataset/HomeC.csv")
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


with ewma:
	data_per_day["ewma_14"] = data_per_day["use"].ewm(span=14).mean()
	data_per_day["ewma_14"] = data_per_day["ewma_14"].shift(1)


with forecast:
	st.subheader("Forecast Home Appliances Energy Usage")
	date_input = st.date_input("Select date", datetime.date(2016, 1, 15))
	date_input = date_input.strftime("%Y-%m-%d 00:00:00")
	start_date = pd.to_datetime(date_input) - pd.DateOffset(days=14)

	data_per_day['Date'] = data_per_day.index
	data_per_day['plot'] = data_per_day['use']

	data_use = data_per_day.loc[start_date:pd.to_datetime(date_input)-pd.DateOffset(days=1),'Date':'plot']
	data_use['category'] = 'Overall energy usage history'

	data_ewma14 = data_per_day.loc[pd.to_datetime(date_input)-pd.DateOffset(days=1):date_input,['Date','ewma_14']]
	data_ewma14['category'] = 'Forecast'
	data_ewma14.loc[data_ewma14.index[0],'ewma_14'] = data_use.loc[data_use.index[-1],'plot']
	data_ewma14 = data_ewma14.rename(columns={'ewma_14':'plot'})
	
	data_concat = pd.concat([data_use, data_ewma14],axis=0)
	f_chart = pd.DataFrame(data_concat)

	line_chart = alt.Chart(f_chart).mark_line().encode(
    alt.X('Date', title='Date'),
    alt.Y('plot', title='Energy usage (kWh)'),
    color='category:N').properties(
    width=680,
    height=300)

	st.altair_chart(line_chart)


with daily_statistic:
	st.subheader("Daily Statistic for Home Appliances Energy Usage")
	d = st.date_input("Select date", datetime.date(2016, 7, 6))
	d = d.strftime("%Y-%m-%d 00:00:00")

	a = data_per_day.iloc[data_per_day.index == d].T
	a = pd.concat([a.iloc[2:11], a.iloc[22:24]], axis=0)

	fig = px.pie(a, values=d, names=a.index, title='')
	st.plotly_chart(fig)


with energy_usage:

	st.subheader("Statistic of Each Home Appliances Energy Usage Over the Year")
	appliances_list = st.selectbox("Select Appliances", ("Dishwasher", "Home office", "Wine cellar", "Garage door", "Barn", "Well", "Microwave", "Living room" ,"Kitchen", "Furnace", "Fridge"))
	appliances_chart = pd.DataFrame(data_per_day[appliances_list])
	appliances_mean = pd.DataFrame(data_per_day[appliances_list]).mean()
	st.line_chart(appliances_chart)
	st.write("Mean energy consumption for ",appliances_list,": ",appliances_mean.iloc[0],"kWh per day")

