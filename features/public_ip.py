from streamlit_javascript import st_javascript
import streamlit as st

def get_public_ip():
    # Use JavaScript to fetch the user's public IP
    ip = st_javascript("fetch('https://api64.ipify.org?format=json').then(res => res.json()).then(data => data.ip)")
    return ip

st.title("Public IP Checker")
public_ip = get_public_ip()

if public_ip:
    st.success(f"Your Public IP Address: {public_ip}")
else:
    st.error("Unable to fetch public IP address. Please check your internet connection.")
