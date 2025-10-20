import streamlit as st
import requests
from datetime import datetime
import pandas as pd
'''
# TaxiFareModel front
'''


st.header("Select Ride Details")

date = st.date_input("Pickup Date", datetime.today())
time = st.time_input("Pickup Time", datetime.now().time())
pickup_datetime = datetime.combine(date, time).strftime("%Y-%m-%d %H:%M:%S")

pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=10, value=1)


url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

## Finally, we can display the prediction to the user
params = {
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}
if st.button("Predict Fare 💰"):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        prediction = data.get("prediction")

        if prediction is not None:
            st.success(f"💵 Estimated Fare: ${float(prediction):.2f}")
        else:
            st.warning("⚠️ No prediction returned from the API. Please check your inputs.")

    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Error while connecting to the API: {e}")
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {e}")
st.header("Pickup and Arrive Point")
st.map(pd.DataFrame({
    'lat': [pickup_latitude, dropoff_latitude],
    'lon': [pickup_longitude, dropoff_longitude]
}, columns=['lat', 'lon']))
