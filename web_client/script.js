const API = "http://127.0.0.1:5001";
let chartInstance = null;

function showTab(tabName) {
    document.querySelectorAll(".content").forEach(div => {
        div.classList.remove("visible");
    });
    document.getElementById(tabName).classList.add("visible");
}

async function loadPlayers() {
    const res = await fetch(`${API}/players`);
    const players = await res.json();

    const list = document.getElementById("player-list");
    list.innerHTML = "";

    players.forEach(p => {
        const li = document.createElement("li");

        li.innerHTML = `
            <span class="player-info">${p.name} — Score: ${p.score} | XP: ${p.xp} | Level: ${p.level}</span>
            <span class="actions">
                <button class="btn" onclick="play(${p.id})">Play</button>
                <button class="btn" onclick="edit(${p.id})">Edit</button>
                <button class="btn" onclick="del(${p.id})">Delete</button>
                <button class="btn" onclick="daily(${p.id})">Daily reward</button>
            </span>
        `;

        list.appendChild(li);
    });

    // Leaderboard
    const sorted = [...players].sort((a, b) => b.score - a.score);
    document.getElementById("leaderboard-list").innerHTML =
        sorted.map(p => `<li>${p.name}: ${p.score}</li>`).join("");

    updateChart(sorted);
}

async function addPlayer() {
    const name = document.getElementById("playerName").value;
    if (!name) return alert("Enter a name");

    await fetch(`${API}/players`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name})
    });

    loadPlayers();
}

async function play(id) {
    const res = await fetch(`${API}/players/${id}/play`, { method: "POST" });
    const data = await res.json();

    let msg = `📜 ${data.quest}\n${data.description}\n+${data.xp_gain} XP, +${data.score_gain} Score`;

    if (data.critical === "success") msg += "\n🔥 Kritični uspeh!";
    if (data.critical === "failure") msg += "\n💀 Kritična napaka!";

    popup(msg);
    loadPlayers();

    addQuestLog(data);
}



async function edit(id) {
    const score = prompt("New score:");
    if (score === null) return;

    await fetch(`${API}/players/${id}/score`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({score: Number(score)})
    });

    loadPlayers();
}

async function del(id) {
    if (!confirm("Delete player?")) return;

    await fetch(`${API}/players/${id}`, {method: "DELETE"});
    loadPlayers();
}

async function daily(id) {
    const res = await fetch(`${API}/players/${id}/daily`, {method: "POST"});
    const data = await res.json();

    if (data.error) popup(data.error);
    else alert("Daily Reward Collected!");

    loadPlayers();
}

function updateChart(players) {
    const ctx = document.getElementById("scoreChart").getContext("2d");

    if (chartInstance) chartInstance.destroy();

    chartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: players.map(p => p.name),
            datasets: [{
                label: "Scores",
                data: players.map(p => p.score),
                backgroundColor: "#00eaff88",
                borderColor: "#00eaff",
                borderWidth: 2
            }]
        }
    });
}

function popup(msg) {
    const box = document.getElementById("popup");
    box.innerText = msg;
    box.style.display = "block";

    setTimeout(() => {
        box.style.display = "none";
    }, 2500);
}

function addQuestLog(q) {
    const log = document.getElementById("quest-log");
    const entry = document.createElement("div");
    entry.className = "log-entry";
    entry.innerText = `${q.quest} (+${q.xp_gain} XP, +${q.score_gain} Score)`;
    log.prepend(entry);

    while (log.childElementCount > 5) {
        log.removeChild(log.lastChild);
    }
}


loadPlayers();
