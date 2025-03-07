import streamlit as st
import time
from features.public_ip import get_public_ip
from features.private_ip import get_private_ip
from features.ping_test import get_computer_ping, ping_domain, is_valid_domain
import matplotlib.pyplot as plt

def add_footer():
    footer = """
    <style>
    .footer-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: transparent;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 14px;
        font-family: Arial, sans-serif;
        color: rgba(240, 240, 240, 0.6);
        border-top: 1px solid rgba(240, 240, 240, 0.2);
    }
    .footer-center {
        flex-grow: 1; /* Ensure the name stays in the center */
        text-align: center;
    }
    .footer-links {
        display: flex;
        align-items: center;
    }
    .footer-links a {
        margin-left: 15px;
        color: #1f77b4;
        text-decoration: none;
    }
    .footer-links a:hover {
        text-decoration: underline;
    }
    .footer-links img {
        width: 20px;
        height: 20px;
        vertical-align: middle;
    }
    </style>
    <div class="footer-container">
        <div></div> <!-- Empty div for alignment purposes -->
        <div class="footer-center">
            Developed by <b>Mihit Singasane</b>
        </div>
        <div class="footer-links">
            <a href="https://github.com/Mihit10" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/733/733553.png" alt="GitHub">
            </a>
            <a href="https://www.linkedin.com/in/mihit-singasane-71153128b" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/145/145807.png" alt="LinkedIn">
            </a>
            <a style="margin-right: 50px;" href="https://devfolio.co/@Mihit10" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/1177/1177568.png" alt="Devfolio">
            </a>
        </div>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)



# Streamlit App Title
def main_app():
    st.title("Network Testing App")
    st.sidebar.title("Navigation")

    # Navigation Menu
    menu = st.sidebar.selectbox(
        "Choose a Feature",
        ["Home", "Public IP", "Private IP", "Ping Test", "Speed Test", "DNS Lookup", "Geolocation"]
    )

    # Pages Placeholder
    if menu == "Home":
        st.title("Welcome to the Network Utility App!")
        st.write("""
        This app provides essential network tools:
        - Discover your public and private IP addresses.
        - Test your network speed and ping.
        - Lookup DNS records and analyze geolocation data.
        """)

    elif menu == "Public IP":
        st.header("Public IP Address")
        ip = get_public_ip()
        st.write(f"Your Public IP Address: {ip}")
    
    elif menu == "Private IP":
        st.header("Private IP Address")
        ip = get_private_ip()
        st.write(f"Your Private IP Address: {ip}")

    elif menu == "Ping Test":
        st.title("Ping Test")

        # Tabs for "Check Computer Ping" and "Ping a Domain"
        tab1, tab2 = st.tabs(["Check Computer Ping", "Ping a Domain"])

        # Tab 1: Check Computer Ping
        with tab1:
            st.subheader("Check Computer Ping")
            if st.button("Run Computer Ping Test", key="comp_ping"):
                with st.spinner("Calculating ping..."):
                    stats = get_computer_ping(count=10)

                if "error" in stats:
                    st.error(stats["error"])
                else:
                    st.success("Ping Test Completed!")
                    st.write(f"Min: {stats['min']} ms")
                    st.write(f"Avg: {stats['avg']} ms")
                    st.write(f"Max: {stats['max']} ms")
                    st.write(f"Median: {stats['median']} ms")
                    st.write(f"Jitter: {stats['jitter']} ms")

                    # Plot the results
                    st.subheader("Ping Results Graph")
                    fig, ax = plt.subplots()
                    ax.plot(stats["results"], marker="o", linestyle="-", color="green")
                    ax.set_title("Ping Over Time")
                    ax.set_xlabel("Ping Attempt")
                    ax.set_ylabel("Ping (ms)")
                    st.pyplot(fig)

        # Tab 2: Ping a Domain
        with tab2:
            st.subheader("Ping a Domain")
            domain = st.text_input("Enter a domain or IP address:", key="domain_input")
            if st.button("Run Domain Ping Test", key="domain_ping"):
                if domain:
                    with st.spinner("Validating domain..."):
                        is_valid = is_valid_domain(domain)
                    # Validate the domain
                    if not is_valid:
                        st.error("Please enter a valid domain or IP address.")
                    else:
                        with st.spinner("Pinging domain..."):
                            stats = ping_domain(domain=domain, count=10)

                        if "error" in stats:
                            st.error(stats["error"])
                        else:
                            st.success(f"Ping Test Completed for {domain}!")
                            st.write(f"Min: {stats['min']} ms")
                            st.write(f"Avg: {stats['avg']} ms")
                            st.write(f"Max: {stats['max']} ms")
                            st.write(f"Median: {stats['median']} ms")
                            st.write(f"Jitter: {stats['jitter']} ms")

                            # Plot the results
                            st.subheader("Ping Results Graph")
                            fig, ax = plt.subplots()
                            ax.plot(stats["results"], marker="o", linestyle="-", color="blue")
                            ax.set_title(f"Ping Over Time for {domain}")
                            ax.set_xlabel("Ping Attempt")
                            ax.set_ylabel("Ping (ms)")
                            st.pyplot(fig)
                else:
                    st.error("Please enter a valid domain or IP address.")
              
    elif menu == "Speed Test":
        from features.speed_test import speed_test_ui
        speed_test_ui()

    elif menu == "DNS Lookup":
        st.header("DNS Lookup")

        # User input for domain name
        domain = st.text_input("Enter the domain name:", key="dns_input")

        # Dropdown to select record type
        record_type = st.selectbox(
            "Select the DNS record type:",
            ["A", "MX", "NS", "TXT", "CNAME"],
            key="dns_record_type"
        )

        # Info about DNS record types
        with st.expander("What do these DNS record types mean?"):
            st.write("""
            - **A**: Maps a domain to an IPv4 address (e.g., `example.com -> 192.168.1.1`).
            - **MX**: Specifies the mail servers responsible for emails sent to the domain.
            - **NS**: Lists the authoritative nameservers for the domain.
            - **TXT**: Provides additional text-based information, often used for security (e.g., SPF, DKIM).
            - **CNAME**: Alias for another domain (e.g., `www.example.com -> example.com`).
            """)

        if st.button("Perform DNS Lookup", key="dns_lookup"):
            if domain:
                # Call the DNS lookup function
                from features.dns_lookup import perform_dns_lookup
                with st.spinner("Performing DNS lookup..."):
                    result = perform_dns_lookup(domain, record_type)

                # Display results
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(f"{record_type} Records for {domain}:")
                    for record in result["results"]:
                        st.write(record)
            else:
                st.error("Please enter a valid domain name.")

    elif menu == "Geolocation":
        st.header("Geolocation")

        # User input for IP address or domain
        ip_or_domain = st.text_input("Enter an IP address or domain to locate:", key="geo_input")

        if st.button("Get Geolocation", key="geo_button"):
            if ip_or_domain:
                # Call the geolocation function
                from features.geolocation import get_geolocation
                with st.spinner("Fetching geolocation data..."):
                    result = get_geolocation(ip_or_domain)

                # Display results
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(f"Geolocation Data for {ip_or_domain}:")
                    st.write(f"**IP**: {result['ip']}")
                    st.write(f"**Country**: {result['country']}")
                    st.write(f"**Region**: {result['region']}")
                    st.write(f"**City**: {result['city']}")
                    st.write(f"**Latitude**: {result['lat']}")
                    st.write(f"**Longitude**: {result['lon']}")
                    st.write(f"**ISP**: {result['isp']}")

                    # Optional: Display a map
                    import pandas as pd

                    # Create a DataFrame for the map
                    map_data = pd.DataFrame(
                        [{"latitude": result["lat"], "longitude": result["lon"]}]
                    )

                    st.map(map_data, zoom=5)
            else:
                st.error("Please enter a valid IP address or domain.")

    add_footer()





# Combine Loading Screen with Main App
def main():
    main_app()

if __name__ == "__main__":
    main()