# Network Monitoring System

## **Project Overview**
This project is a **network monitoring system** that continuously checks internet connectivity and logs connection issues. The system is designed to work with **embedded Linux** and can be configured as a **systemd service** to run automatically on startup.

## **Features**
- Periodically pings well-known DNS servers (**Google, OpenDNS, Cloudflare**) to check connectivity.
- Logs network status changes (**online, outage, unreachable**).
- Saves logs in a structured format in `network.log`.
- Can be managed as a **systemd service** to ensure automatic execution at boot.

---

## **Project Structure**
```
log-service/
├── backup.py           # Monitors network outages (legacy version)
├── logging.py          # Main script that logs network status
├── log-analyze.py      # Reads and prints log files
├── network.log         # Log file with network status data
```

---

## **How to Run the Project**
### **1. Install Dependencies**
Ensure you have Python installed:
```bash
sudo apt update && sudo apt install python3
```

### **2. Run the Monitoring Script**
To start network monitoring manually:
```bash
python3 logging.py
```

### **3. View Network Logs**
To analyze recorded network data:
```bash
python3 log-analyze.py
```

---

## **Systemd Integration**
To ensure that the monitoring script runs **automatically** on system boot, you can create a **systemd service**.

### **1. Create a systemd Service File**
Create the following file at `/etc/systemd/system/network-monitor.service`:

```ini
[Unit]
Description=Network Monitoring Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/logging.py
Restart=always
User=root
WorkingDirectory=/path/to/your/
StandardOutput=append:/var/log/network-monitor.log
StandardError=append:/var/log/network-monitor.log

[Install]
WantedBy=multi-user.target
```

### **2. Set Permissions**
```bash
sudo chmod 644 /etc/systemd/system/network-monitor.service
sudo chmod +x /path/to/your/logging.py
```

### **3. Enable and Start the Service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable network-monitor
sudo systemctl start network-monitor
```

### **4. Check Service Status**
```bash
sudo systemctl status network-monitor
```

### **5. Stop or Restart the Service**
```bash
sudo systemctl stop network-monitor
sudo systemctl restart network-monitor
```

---

## **Log File Location**
By default, the log file is stored in:
```
/path/to/your/network.log
```
To view the latest logs:
```bash
tail -f /path/to/your/network.log
```

---

## **Future Improvements**
- **Alert System**: Send email or webhook notifications when connectivity issues occur.
- **Dashboard**: Integrate with a web-based dashboard to visualize network performance.
- **Data Analysis**: Use machine learning to detect recurring network failures.

This project provides a **robust and automated** solution for network monitoring, particularly in **embedded Linux** environments. 🚀
