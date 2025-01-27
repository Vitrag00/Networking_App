# 🌐 Network Testing App

A simple yet powerful **Streamlit-based web application** for performing various network-related tests and obtaining critical information about your network in real-time. This app is designed to provide accurate results, an intuitive user experience, and seamless deployment capabilities.

---

## ⚡ Features

1. **Public IP Detection**  
   - Get the public IP address of your device in real-time.

2. **Private IP Detection**  
   - Detect the private IP address of your local network (only available when running locally).

3. **Ping Test**  
   - Test the connectivity to a domain or IP address with detailed statistics:
     - Minimum, Average, Maximum, Median ping times
     - Jitter analysis
     - Interactive graph displaying ping over time.

4. **Speed Test**  
   - Measure your network's download and upload speeds interactively, with attention-grabbing progress messages during testing.

5. **DNS Lookup**  
   - Retrieve DNS records (A, CNAME, MX, etc.) for a domain.

6. **Geolocation**  
   - Get geolocation details of a specific IP address, including:
     - Country, Region, City
     - Latitude & Longitude
     - Internet Service Provider (ISP)

---

## 🛠️ Tech Stack

- **Python**: Core programming language
- **Streamlit**: Frontend and backend framework for web app development
- **Libraries**: 
  - `requests` for API calls
  - `ping3` for ping testing
  - `matplotlib` for plotting graphs
  - `dnspython` for DNS lookup
  - `ipwhois` for geolocation details

---

## 🚀 How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Mihit10/network-testing-app.git
