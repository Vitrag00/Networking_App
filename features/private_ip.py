import socket
import streamlit as st
import os

def get_private_ip():
    try:
        # Check if the app is running locally
        if os.getenv("STREAMLIT_SERVER_RUN_ON_SERVER") is None:
            hostname = socket.gethostname()
            private_ip = socket.gethostbyname(hostname)
            return private_ip
        else:
            return "ONLINE"
    except Exception as e:
        return f"Error occurred: {e}"

st.title("Private IP Checker")
private_ip = get_private_ip()

if private_ip.startswith("127."):
    st.error("Private IP is not accessible by online services due to browser and network security restrictions. Please run this app locally to retrieve your private IP.")
else:
    st.success(f"Your Private IP Address: {private_ip}")
