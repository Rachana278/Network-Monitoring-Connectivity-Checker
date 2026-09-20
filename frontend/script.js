let latencyChart;
let packetLossChart;

async function loadNetworkStatus() {

    try {

        const response = await fetch("/api/status");

        const data = await response.json();


        // =========================
        // Dashboard statistics
        // =========================

        const totalHosts = data.length;

        const hostsUp = data.filter(
            host => host.status === "UP"
        ).length;

        const hostsDown = data.filter(
            host => host.status === "DOWN"
        ).length;

        document.getElementById("total-hosts").textContent = totalHosts;
        document.getElementById("hosts-up").textContent = hostsUp;
        document.getElementById("hosts-down").textContent = hostsDown;


        // =========================
        // Network status table
        // =========================

        const table = document.getElementById("network-table");

        table.innerHTML = "";

        data.forEach(host => {

            const row = document.createElement("tr");

            const statusIndicator =
                host.status === "UP" ? "🟢" : "🔴";

            row.innerHTML = `
                <td>${host.host}</td>

                <td>
                    ${statusIndicator} ${host.status}
                </td>

                <td>
                    ${host.latency !== null
                        ? host.latency + " ms"
                        : "N/A"}
                </td>

                <td>
                    ${host.packet_loss !== null
                        ? host.packet_loss + "%"
                        : "N/A"}
                </td>
            `;

            table.appendChild(row);
        });


        // =========================
        // Prepare chart data
        // =========================

        const timestamp = new Date().toLocaleTimeString();

        const upHosts = data.filter(
            host => host.status === "UP"
        );


        // =========================
        // Latency Chart
        // =========================

        const latencyLabels = upHosts.map(
            host => host.host
        );

        const latencyValues = upHosts.map(
            host => host.latency
        );


        if (latencyChart) {
            latencyChart.destroy();
        }


        const latencyCanvas =
            document.getElementById("latency-chart");


        latencyChart = new Chart(
            latencyCanvas,
            {
                type: "bar",

                data: {
                    labels: latencyLabels,

                    datasets: [
                        {
                            label: "Latency (ms)",

                            data: latencyValues
                        }
                    ]
                },

                options: {
                    responsive: true,

                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            }
        );


        // =========================
        // Packet Loss Chart
        // =========================

        const packetLossLabels = upHosts.map(
            host => host.host
        );

        const packetLossValues = upHosts.map(
            host => Number(host.packet_loss)
        );


        if (packetLossChart) {
            packetLossChart.destroy();
        }


        const packetLossCanvas =
            document.getElementById("packet-loss-chart");


        packetLossChart = new Chart(
            packetLossCanvas,
            {
                type: "bar",

                data: {
                    labels: packetLossLabels,

                    datasets: [
                        {
                            label: "Packet Loss (%)",

                            data: packetLossValues
                        }
                    ]
                },

                options: {
                    responsive: true,

                    scales: {
                        y: {
                            beginAtZero: true,

                            max: 100
                        }
                    }
                }
            }
        );

    }

    catch (error) {

        console.error(
            "Error connecting to backend:",
            error
        );

    }
}


// Load data when page opens
loadNetworkStatus();


// Refresh every 10 seconds
setInterval(
    loadNetworkStatus,
    10000
);