import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Taxi Fare Predictor", page_icon="🚕", layout="centered")

st.title("🚖 Taxi Fare Prediction App")
st.markdown("Enter your ride details below to estimate your taxi fare!")

st.markdown("---")


st.header("📋 Ride Details")

col1, col2 = st.columns(2)

with col1:
    date = st.date_input("Pickup Date", datetime.today())
    time = st.time_input("Pickup Time", datetime.now().time())

with col2:
    passenger_count = st.slider("👥 Number of Passengers", 1, 8, 1)

pickup_datetime = datetime.combine(date, time).strftime("%Y-%m-%d %H:%M:%S")

st.subheader("📍 Locations")

pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.768817)

st.markdown("### 🗺️ Trip Map")
map_data = pd.DataFrame({
    "lat": [pickup_latitude, dropoff_latitude],
    "lon": [pickup_longitude, dropoff_longitude]
})
st.map(map_data)

url = 'https://taxifare.lewagon.ai/predict'

if st.button("💰 Predict Fare"):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    try:
        response = requests.get("https://taxifare.lewagon.ai/predict", params=params)
        response.raise_for_status()

        result = response.json()
        st.write("📦 API Response:", result)

        prediction = result.get("fare")

        if prediction is not None:
            st.success(f"💵 Estimated Fare: **${prediction:.2f}**")
        else:
            st.warning("⚠️ No prediction returned from the API. Please check your inputs.")

    except Exception as e:
        st.error(f"An error occurred while connecting to the API: {e}")

st.markdown("---")
