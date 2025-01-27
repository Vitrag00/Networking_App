from ping3 import ping
import statistics
import time
import streamlit as st
import matplotlib.pyplot as plt
import socket



def is_valid_domain(domain):
    """
    Validate the domain or IP address.

    Args:
        domain (str): The domain or IP to validate.

    Returns:
        bool: True if the domain is valid, False otherwise.
    """
    try:
        # Check if the domain can be resolved
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def get_user_ping(host="google.com", count=4, delay=1):
    """
    Perform a ping test using the ping3 library.

    Args:
        host (str): The domain or IP to ping.
        count (int): Number of ping attempts.
        delay (int): Delay in seconds between ping attempts.

    Returns:
        dict: Ping statistics (min, max, avg, median, jitter, and results for graphing) or an error message.
    """
    try:
        results = []
        for _ in range(count):
            try:
                response_time = ping(host, timeout=2)  # Ping with a 2-second timeout
                if response_time is not None:
                    results.append(response_time * 1000)  # Convert seconds to milliseconds
            except Exception as e:
                st.warning(f"Ping attempt failed: {e}")
                results.append(None)

            time.sleep(delay)  # Introduce delay between attempts

        # Filter out failed pings (None values)
        results = [r for r in results if r is not None]

        if results:
            # Calculate statistics
            stats = {
                "min": round(min(results), 2),
                "max": round(max(results), 2),
                "avg": round(statistics.mean(results), 2),
                "median": round(statistics.median(results), 2),
                "jitter": round(statistics.stdev(results), 2) if len(results) > 1 else 0.0,
                "results": results,  # For graphing purposes
            }
            return stats
        else:
            return {"error": "No valid ping responses received. The host may be unreachable or ICMP packets are blocked."}

    except Exception as e:
        return {"error": f"An error occurred: {e}"}


def get_computer_ping(count=4):
    """
    Perform a ping test for the user's computer.

    Args:
        count (int): Number of ping attempts.

    Returns:
        dict: Ping statistics for a standard server (google.com) or an error message.
    """
    return get_user_ping(host="google.com", count=count)


def ping_domain(domain, count=4):
    """
    Perform a ping test for a user-provided domain.

    Args:
        domain (str): The domain or IP to ping.
        count (int): Number of ping attempts.

    Returns:
        dict: Ping statistics for the given domain or an error message.
    """
    return get_user_ping(host=domain, count=count)


