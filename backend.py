from flask import Flask, jsonify, send_from_directory
import subprocess
import platform
import re

app = Flask(__name__)

hosts = [
    "google.com",
    "8.8.8.8",
    "1.1.1.1",
    "this-host-does-not-exist-12345.com"
]


@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory("frontend", filename)


@app.route("/api/status")
def network_status():

    results = []

    for host in hosts:

        # Windows uses -n
        # Linux/macOS uses -c
        if platform.system().lower() == "windows":
            command = ["ping", "-n", "4", host]
        else:
            command = ["ping", "-c", "4", host]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=15
            )

            output = result.stdout

            if result.returncode == 0:

                # Extract packet loss
                loss_match = re.search(
                    r"(\d+(?:\.\d+)?)%\s*(?:loss|packet loss)",
                    output,
                    re.IGNORECASE
                )

                # Extract average latency
                latency_match = re.search(
                    r"(?:Average = |avg/.*?= )(\d+(?:\.\d+)?)\s*ms",
                    output,
                    re.IGNORECASE
                )

                if latency_match:
                    average_latency = float(latency_match.group(1))
                else:
                    average_latency = None

                if loss_match:
                    packet_loss = loss_match.group(1)
                else:
                    packet_loss = "0"

                status = "UP"

            else:

                status = "DOWN"
                average_latency = None
                packet_loss = None

        except Exception:

            status = "DOWN"
            average_latency = None
            packet_loss = None

        results.append({
            "host": host,
            "status": status,
            "latency": average_latency,
            "packet_loss": packet_loss
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )