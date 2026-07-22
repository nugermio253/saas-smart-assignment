let chartAgents = null;
let chartGroups = null;
let chartPriority = null;
let chartHour = null;

/////////////////////////////////////////////////////////

async function loadChartAgents() {

    const response = await fetch("/api/dashboard/chart/agents");
    const data = await response.json();

    const labels = data.map(i => i.agent);
    const values = data.map(i => i.tickets);

    if (chartAgents)
        chartAgents.destroy();

    chartAgents = new Chart(
        document.getElementById("chartAgents"),
        {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Tickets",
                    data: values
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        }
    );
}

/////////////////////////////////////////////////////////

async function loadChartGroups() {

    const response = await fetch("/api/dashboard/chart/groups");
    const data = await response.json();

    const labels = data.map(i => i.group);
    const values = data.map(i => i.tickets);

    if (chartGroups)
        chartGroups.destroy();

    chartGroups = new Chart(
        document.getElementById("chartGroups"),
        {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: values
                }]
            },
            options: {
                responsive: true
            }
        }
    );
}

/////////////////////////////////////////////////////////

async function loadChartPriority() {

    const response = await fetch("/api/dashboard/chart/priorities");
    const data = await response.json();

    const labels = data.map(i => i.priority);
    const values = data.map(i => i.tickets);

    if (chartPriority)
        chartPriority.destroy();

    chartPriority = new Chart(
        document.getElementById("chartPriority"),
        {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [{
                    data: values
                }]
            },
            options: {
                responsive: true
            }
        }
    );
}

/////////////////////////////////////////////////////////

async function loadChartHour() {

    const response = await fetch("/api/dashboard/chart/hours");
    const data = await response.json();

    const labels = data.map(i => i.hour);
    const values = data.map(i => i.tickets);

    if (chartHour)
        chartHour.destroy();

    chartHour = new Chart(
        document.getElementById("chartHour"),
        {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Tickets",
                    data: values,
                    fill: false
                }]
            },
            options: {
                responsive: true
            }
        }
    );
}

/////////////////////////////////////////////////////////

async function refreshCharts() {

    await loadChartAgents();

    await loadChartGroups();

    await loadChartPriority();

    await loadChartHour();

}

refreshCharts();

setInterval(refreshCharts, 5000);
