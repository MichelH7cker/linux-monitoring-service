import subprocess
from time import time, sleep
import re
from datetime import datetime

# colors
green_color  = '\033[92m' # green
red_color    = '\033[91m' # red
yellow_color = '\033[93m' # yellow 
blue_color   = '\033[94m' # blue 
reset_color  = '\033[0m'  # reset color  

GOOGLE_DNS_IP = "8.8.8.8" # Google's DNS server
OPEN_DNS_IP = "208.67.222.222" # OpenDNS server
CLOUDFLARE_IP = "1.1.1.1" # Cloudflare server

SERVERS_IP = [GOOGLE_DNS_IP, OPEN_DNS_IP, CLOUDFLARE_IP]
SERVERS_NAME = ["Google DNS", "OpenDNS", "Cloudflare server"]

DEBUG = True # print out messages to terminal
OUTAGE_DURATION_SEC = 10 # shortest detectable outage

ONLINE = green_color + "online" + reset_color
OUTAGE = yellow_color + "outage" + reset_color
UNREACHABLE = red_color + "network unreachable" + reset_color

INFO = green_color + "INFO" + reset_color
ERROR = red_color + "ERROR" + reset_color

FILE = "network.log"

def writeLogFile(arg):
    with open(FILE, "a") as f:
        f.write(arg + "\n")

def getDateStr(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d")

def getTimeStr(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%H:%M:%S")

def getPingTime(ping_msg):
    match = re.search(r'\/\d{2,4}\.\d{3}\/', ping_msg)
    if match is not None:
        ping_time = float(match.group(0).replace("/", ''))
    else:
        ping_time = None
    return ping_time

def getNetworkStatus(ping_msg):
    if re.search(r'100.0% packet loss|100% packet loss', ping_msg) != None:
        return OUTAGE
    elif re.search(r'Network is unreachable', ping_msg) != None:
        return UNREACHABLE
    else:
        return ONLINE

def ping(ip):
    ping_process = subprocess.Popen(
            ["ping", "-c", "1", ip], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
    pingp = ping_process.stdout.read().decode('utf-8')

    return pingp

def firstTry():
    attempts_to_connect = 0
    while True:
        if "received" in ping(GOOGLE_DNS_IP):
            attempts_to_connect += 1
            text = "[{}] first connection established at {}".format(INFO, getTimeStr(time()))
            writeLogFile(text)
            print(text)
            break
        else:
            attempts_to_connect += 1
            text = "[{}] error in connection ({}x) at {}".format(ERROR, attempts_to_connect, getTimeStr(time()))
            writeLogFile(text)
            print(text)
        
        sleep(1)
    return attempts_to_connect

def clearLogFile():
    with open(FILE, "w") as f:
        f.truncate() 

def main():
    clearLogFile()
    last_connection_time = time()

    attempts_to_connect = firstTry() 
    text = "[{}] the device tried to connect to network {} times".format(INFO, attempts_to_connect)
    writeLogFile(text)
    print(text)

    while True:
        current_time = time()
        if current_time - last_connection_time > OUTAGE_DURATION_SEC:
            text = "[{}] Network reconnection attempt at {}".format(INFO, getTimeStr(current_time))
            print(text)
            writeLogFile(text)
            last_connection_time = current_time

        i = 0
        STATUS = INFO 
        # run all servers
        while (i < len(SERVERS_IP)):
            ping_msg = ping(SERVERS_IP[i])
            network_status = getNetworkStatus(ping_msg)
            if (network_status == UNREACHABLE):
                STATUS = ERROR
            ping_time = getPingTime(ping_msg)
            timestamp = current_time
            date_str = getDateStr(timestamp)
            time_str = getTimeStr(timestamp)
            
            output = "[{}] ping {} server:".format(STATUS, SERVERS_NAME[i])
            output += "\n\t- date {} and time {}".format(date_str, time_str)
            output += "\n\t- status: {}".format(network_status)
            output += blue_color + "\n\t- last time online: {}".format(getTimeStr(last_connection_time)) + reset_color
            output += "\n\t- ping time: {:.3f} ms".format(ping_time) if ping_time is not None else ""
            output += "\n\t- ping command: {}".format(ping_msg)
            output += "\n" + blue_color + "----------------" + reset_color 

            writeLogFile(output) 
            
            if DEBUG:
                print(output)
            i += 1
        sleep(OUTAGE_DURATION_SEC / 2)

if __name__=="__main__":
    main()
