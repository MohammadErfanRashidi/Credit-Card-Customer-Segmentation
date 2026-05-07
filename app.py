import streamlit as st
import joblib
import numpy as np
import pandas as pd
import json

# Load the dependencies 
@st.cache_resource
def load_models():
    scaler = joblib.load('model/scaler.pkl')
    kmeans = joblib.load('model/kmeans_model.pkl')
    with open('model/segment_map.json', 'r') as f:
        segment_map = json.load(f)
    return scaler, kmeans, segment_map

scaler, kmeans, segment_map = load_models()

# App title and description
st.set_page_config(page_title = 'Customer Segment Predictor', layout = 'centered')
st.title('Credit Card Customer Segment Predictor')
st.markdown('Enter the customers raw activity data to see which behavioural segment they belong to.')

# Input form
with st.form('input_form'):
    col1, col2 = st.columns(2)
    
    with col1:
        purchases = st.number_input('Total Purchases ($)', min_value = 0.0, value = 5000.0, step = 500.0)
        cash_advance = st.number_input('Total Cash Advances ($)', min_value = 0.0, value = 1000.0, step = 100.0)
        tenure = st.number_input('Tenure (months)', min_value = 1, value = 12, step = 1)

    with col2:
        oneoff_purchases = st.number_input('One-Off Purchases ($)', min_value = 0.0, value = 2000.0, step = 100.0)
        purchases_frequency = st.number_input('Purchases Frequency', min_value = 0.0, value = 0.5, step = 0.1, help = 'e.g., number of purchases per month')
        oneoff_purchases_frequency = st.number_input('One-Off Purchases Frequency', min_value = 0.0, value = 0.5, step = 0.1)

    submitted = st.form_submit_button('Predict Segment')

# Computation and prediction
if submitted:

    if purchases == 0:
        oneoff_share = 0
    else:
        oneoff_share = oneoff_purchases / purchases

    monthly_purchases = purchases / tenure
    monthly_cash_advance = cash_advance / tenure
    total_monthly_outgoings = monthly_purchases + monthly_cash_advance

    if total_monthly_outgoings == 0:
        cash_advance_ratio = 0
    else:
        cash_advance_ratio = monthly_cash_advance / total_monthly_outgoings

    # Get the feature together
    raw_features = np.array([[purchases_frequency, oneoff_share, cash_advance_ratio, oneoff_purchases_frequency]])

    # Scale
    scaled_features = scaler.transform(raw_features)

    # Predict
    cluster = kmeans.predict(scaled_features)[0]

    # Look up segment info
    segment_info = segment_map[str(cluster)]

    # Display the results
    st.success(f'### Predicted Segment: {segment_info['segment_name']}')
    st.markdown(f'**Description:** {segment_info['description']}')
    st.markdown(f'**Recommended Strategy:** {segment_info['strategy']}')

    # Optionally show intermediate values
    with st.expander("Show computed intermediate values"):
        st.write(f"• oneoff_share: {oneoff_share:.4f}")
        st.write(f"• monthly_purchases: ${monthly_purchases:.2f}")
        st.write(f"• monthly_cash_advance: ${monthly_cash_advance:.2f}")
        st.write(f"• total_monthly_outgoings: ${total_monthly_outgoings:.2f}")
        st.write(f"• cash_advance_ratio: {cash_advance_ratio:.4f}")
        st.write(f"• Scaled features: {scaled_features}")