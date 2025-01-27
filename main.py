import streamlit as st
import time
from features.public_ip import get_public_ip
from features.private_ip import get_private_ip
from features.ping_test import get_computer_ping, ping_domain, is_valid_domain
import matplotlib.pyplot as plt

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
        st.write("Welcome to the Network Testing App! Select a feature from the sidebar.")
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
        st.write("Feature: Geolocation Mapping")


# Combine Loading Screen with Main App
def main():
    main_app()

if __name__ == "__main__":
    main()