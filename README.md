# 🏹 Artemis - Minecraft Username Sniper

High performance, low latency username sniper written in Python.

## ⭐ Features

- **High-Performance Multi-Threading:**  
  Leverage Python’s [threading](https://docs.python.org/3/library/threading.html) module to dispatch multiple HTTP requests concurrently.

- **Secure Socket Communication:**  
  Establish robust, SSL-wrapped connections using Python’s [socket](https://docs.python.org/3/library/socket.html) and [ssl](https://docs.python.org/3/library/ssl.html) modules.

- **Custom Countdown Timer:**  
  Synchronize network requests with a built-in timer, utilizing [time](https://docs.python.org/3/library/time.html) and [datetime](https://docs.python.org/3/library/datetime.html).

- **Accurate Network Latency Measurement:**  
  Calculate ping delays by measuring round-trip times via raw socket calls.

- **Discord Webhook Integration:**  
  Receive real-time notifications on successful operations via [discord_webhook](https://github.com/lovvskillz/python-discord-webhook).

- **Comprehensive Account Authentication:**  
  Supports multiple account types through [msmcauth](https://pypi.org/project/msmcauth/), with a fallback to Mojang authentication for seamless access.

## 📦 Installation

### ⚙️ Prerequisites

- Python 3.x
- pip

### 📦 Installing Dependencies

From the project root, run:
```sh
pip install -r requirements.txt
```

### 🛠️ Cloning the Repository

Clone the repository using:
```sh
git clone https://github.com/your-username/Artemis-Sniper.git
cd Artemis-Sniper
```

## 🚀 Usage

1. **Configure Your Accounts:**  
   Populate the `accounts.txt` file with your account credentials in the `email:password` format.

2. **Launch Artemis:**  
   Execute the script:
   ```sh
   python artemis.py
   ```

3. **Follow the On-Screen Prompts:**  
   - Enter the target Minecraft username when prompted.
   - Provide a custom network offset or press Enter to use the auto-detected value.
   - The tool will authenticate your accounts, initialize threads, and dispatch the name change request precisely at droptime.

## 💡 How It Works

1. **Dependency Management:**  
   Upon startup, the script checks for and installs any missing dependencies automatically.

2. **Robust Authentication:**  
   Authenticate using [msmcauth](https://pypi.org/project/msmcauth/) with a fallback to Mojang authentication to ensure continuous operation.

3. **Latency Calculation:**  
   The tool pings the Minecraft API to accurately measure network latency, optimizing request timing.

4. **Synchronized Execution:**  
   A countdown timer orchestrates the simultaneous launch of multiple threads.

5. **Efficient Name Change Process:**  
   At the scheduled droptime, threads send requests to Minecraft's API to update your username. 