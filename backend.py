from flask import Flask, jsonify, send_from_directory
import socket
import time

app = Flask(__name__)

hosts = [
    "google.com",
    "cloudflare.com",
    "github.com",
    "this-host-does-not-exist-12345.com"
]


def check_host(host):
    attempts = 4
    successful = 0
    latencies = []

    for _ in range(attempts):
        try:
            start = time.perf_counter()

            # Try connecting to HTTPS port
            connection = socket.create_connection(
                (host, 443),
                timeout=3
            )

            connection.close()

            latency = (time.perf_counter() - start) * 1000
            latencies.append(latency)
            successful += 1

        except Exception:
            pass

    packet_loss = ((attempts - successful) / attempts) * 100

    if successful > 0:
        average_latency = round(
            sum(latencies) / len(latencies), 2
        )
        status = "UP"
    else:
        average_latency = None
        status = "DOWN"

    return {
        "host": host,
        "status": status,
        "latency": average_latency,
        "packet_loss": packet_loss
    }


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
        results.append(check_host(host))

    return jsonify(results)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )