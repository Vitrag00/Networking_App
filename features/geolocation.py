import requests

def get_geolocation(ip_or_domain):
    """
    Get geolocation data for a given IP address or domain.

    Args:
        ip_or_domain (str): The IP address or domain to lookup.

    Returns:
        dict: Geolocation data or an error message.
    """
    try:
        # API endpoint for geolocation
        api_url = f"http://ip-api.com/json/{ip_or_domain}"

        # Make a request to the API
        response = requests.get(api_url, timeout=10)
        data = response.json()

        # Check for errors in the response
        if data["status"] != "success":
            return {"error": "Unable to retrieve geolocation data. Please check the input."}

        # Return the geolocation details
        return {
            "ip": data.get("query", "N/A"),
            "country": data.get("country", "N/A"),
            "region": data.get("regionName", "N/A"),
            "city": data.get("city", "N/A"),
            "lat": data.get("lat", "N/A"),
            "lon": data.get("lon", "N/A"),
            "isp": data.get("isp", "N/A"),
        }

    except requests.RequestException as e:
        return {"error": f"An error occurred while fetching geolocation data: {e}"}
