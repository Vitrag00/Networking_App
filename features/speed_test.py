import streamlit as st
from speedtest import Speedtest
import time
from collections import deque


def run_speed_test_with_dynamic_messages(message_container):
    """
    Run a speed test using the Speedtest library with dynamic messages.

    Args:
        message_container (deque): A deque to manage dynamic messages.

    Returns:
        dict: Speed test results or an error message.
    """
    try:
        # Initialize Speedtest
        update_messages(message_container, "Initializing speed test... 🚀")
        speed_test = Speedtest()

        # Find the best server with dynamic messages
        for msg in [
            "Searching for the best server... 🌐",
            "Locating the closest data center... 📍",
            "Scanning network paths... 🛠️",
        ]:
            update_messages(message_container, msg)
            time.sleep(1)

        speed_test.get_best_server()

        # Run download and upload tests with more dynamic messages
        for msg in [
            "Running download test... 📥",
            "Testing your network's limits... 🚀",
            "Checking data transfer speeds... 🔄",
            "Running upload test... 📤",
            "Finalizing your speed test... 🏁",
        ]:
            update_messages(message_container, msg)
            time.sleep(1)

        # Perform the actual download and upload speed tests
        download_speed = speed_test.download() / 1e6  # Convert to Mbps
        upload_speed = speed_test.upload() / 1e6  # Convert to Mbps
        ping = speed_test.results.ping

        # Clear all messages after the test is complete
        message_container.clear()

        # Server information
        server = speed_test.results.server

        return {
            "download_speed": round(download_speed, 2),
            "upload_speed": round(upload_speed, 2),
            "ping": round(ping, 2),
            "server": server,
        }

    except Exception as e:
        message_container.clear()
        return {"error": f"Speed test failed: {e}"}


def update_messages(message_container, new_message, max_messages=3):
    """
    Update the message container with a new message, maintaining a max limit.

    Args:
        message_container (deque): The deque storing messages.
        new_message (str): The new message to add.
        max_messages (int): The maximum number of messages to show.
    """
    if len(message_container) >= max_messages:
        message_container.popleft()  # Remove the oldest message
    message_container.append(new_message)

    # Display messages in Streamlit
    st.session_state.message_placeholder.empty()  # Clear placeholder
    for message in message_container:
        st.session_state.message_placeholder.write(message)  # Write each message


def speed_test_ui():
    """
    Streamlit UI for Speed Test with dynamic message management.
    """
    st.title("Speed Test")

    # Create a deque to manage the dynamic messages
    message_container = deque()

    # Add a placeholder for messages in the session state
    if "message_placeholder" not in st.session_state:
        st.session_state.message_placeholder = st.empty()

    if st.button("Run Speed Test"):
        with st.spinner("Running speed test... This may take a few seconds."):
            result = run_speed_test_with_dynamic_messages(message_container)

        # Clear messages and display results
        st.session_state.message_placeholder.empty()

        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Speed Test Completed! 🎉")
            st.write(f"**Download Speed**: {result['download_speed']} Mbps")
            st.write(f"**Upload Speed**: {result['upload_speed']} Mbps")
            st.write(f"**Ping**: {result['ping']} ms")
            st.write(f"**Server**: {result['server']['host']} ({result['server']['country']})")

            # Optional: Add a visualization (e.g., bar chart)
            st.subheader("Speed Test Results")
            st.bar_chart(
                {
                    "Download Speed (Mbps)": [result["download_speed"]],
                    "Upload Speed (Mbps)": [result["upload_speed"]],
                    "Ping (ms)": [result["ping"]],
                }
            )
