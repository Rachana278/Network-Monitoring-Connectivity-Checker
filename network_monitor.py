import subprocess
import time
import os
from datetime import datetime
hosts = ["google.com", "8.8.8.8", "1.1.1.1" , "this-host-does-not-exist-12345.com"]
file_exists = os.path.exists("network_log.csv")
log_file = open("network_log.csv", "a")
if not file_exists:
    log_file.write("Timestamp,Host,Status,Latency,Packet Loss\n")

while True:

    for host in hosts:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = subprocess.run(
            ["ping", "-n", "4", host],
            capture_output=True,
            text=True
        )

        output = result.stdout

        if result.returncode == 0:

            average_line = output.split("Average = ")[1].replace("ms", "")
            average_latency = int(average_line)

            loss_part = output.split("(")[1]
            packet_loss = loss_part.split("%")[0]

            status = "UP"

        else:
            status = "DOWN"
            average_latency = None
            packet_loss = None
            
        log_entry = f"{timestamp},{host},{status},{average_latency},{packet_loss}\n"

        log_file.write(log_entry)
        log_file.flush()    

        print("\n========================================")
        print("       NETWORK MONITORING REPORT")
        print("========================================")
        print("Host           :", host)
        print("Status         :", status)

        if status == "UP":
            print("Average Latency:", average_latency, "ms")
            print("Packet Loss    :", packet_loss, "%")
        else:
            print("Average Latency: N/A")
            print("Packet Loss    : N/A")

        print("========================================")

    time.sleep(10)