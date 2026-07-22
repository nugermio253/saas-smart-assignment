async function loadCards() {

    const response = await fetch("/api/dashboard/cards");
    const data = await response.json();

    const agents = document.getElementById("agents");
    if (agents) agents.innerHTML = data.agents;

    const pending = document.getElementById("pending");
    if (pending) pending.innerHTML = data.pending;

    const total = document.getElementById("total");
    if (total) total.innerHTML = data.total_assignments;

    const today = document.getElementById("today");
    if (today) today.innerHTML = data.today;
}

async function loadRanking() {

    const response = await fetch("/api/dashboard/chart/agents");
    const data = await response.json();

    const table = document.getElementById("ranking");

    if (!table)
        return;

    table.innerHTML = "";

    data.forEach(agent => {

        table.innerHTML += `
            <tr>
                <td>${agent.agent}</td>
                <td class="text-end">${agent.tickets}</td>
            </tr>
        `;

    });

}

async function loadLatest() {

    const response = await fetch("/api/dashboard/latest");
    const data = await response.json();

    const table = document.getElementById("latest");

    if (!table)
        return;

    table.innerHTML = "";

    data.forEach(ticket => {

        table.innerHTML += `
            <tr>
                <td>${ticket.ticket_number}</td>
                <td>${ticket.customer_name}</td>
                <td>${ticket.ticket_title}</td>
                <td>${ticket.group_name}</td>
                <td>${ticket.priority_name}</td>
                <td>${ticket.state_name}</td>
                <td>${ticket.agent_name}</td>
                <td>${ticket.assigned_at}</td>
            </tr>
        `;

    });

}

async function refreshDashboard() {

    try {

        await loadCards();
        await loadRanking();
        await loadLatest();

    } catch (e) {

        console.error("Erro ao atualizar dashboard:", e);

    }

}

refreshDashboard();

setInterval(refreshDashboard, 5000);
