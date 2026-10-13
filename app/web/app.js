const $ = (id) => document.getElementById(id);
const log = (message) => { $("log").textContent = String(message); };
async function api(path, options = {}) {
  const response = await fetch(path, { headers: {"Content-Type":"application/json"}, ...options });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "HTTP " + response.status);
  return data;
}
function setStatus(id, available) {
  $(id).textContent = available ? "Available" : "Not found";
  $(id).style.color = available ? "var(--cyan)" : "var(--orange)";
}
async function refreshStatus() {
  try {
    const data = await api("/api/status");
    $("connection").textContent = "Local API connected";
    document.querySelector(".connection .dot").style.background = "var(--cyan)";
    setStatus("nasm", data.nasmAvailable); setStatus("make", data.makeAvailable);
    setStatus("qemu", data.qemuAvailable); setStatus("image", data.imageExists);
    log("API connected. Project: " + data.project + "\nPython: " + data.python);
  } catch (error) {
    $("connection").textContent = "API unavailable";
    log("Could not connect to local API: " + error.message + "\nStart it with: python3 app.py");
  }
}
async function refreshFiles() {
  try {
    const data = await api("/api/files");
    const filter = $("fileFilter").value.toLowerCase();
    const rows = data.files.filter(file => file.path.toLowerCase().includes(filter));
    $("fileRows").replaceChildren();
    for (const file of rows) {
      const tr = document.createElement("tr");
      const path = document.createElement("td"); path.textContent = file.path;
      const size = document.createElement("td"); size.textContent = file.bytes.toLocaleString() + " B";
      tr.append(path, size); $("fileRows").append(tr);
    }
    if (!rows.length) { const tr = document.createElement("tr"); const td = document.createElement("td"); td.colSpan = 2; td.textContent = "No matching files."; tr.append(td); $("fileRows").append(tr); }
  } catch (error) { $("fileRows").textContent = error.message; }
}
async function refreshSettings() {
  try { $("settingsData").textContent = JSON.stringify(await api("/api/settings"), null, 2); }
  catch (error) { $("settingsData").textContent = error.message; }
}
async function runCommand(command, button) {
  const old = button.textContent; button.disabled = true; button.textContent = "Running…";
  log("$ " + command + "\nWorking…");
  try {
    const result = await api("/api/commands", {method:"POST", body:JSON.stringify({command})});
    log("$ " + (result.command || command) + "\nExit code: " + result.returncode + "\n\n" + (result.output || result.error || "Completed."));
    if (result.ok) await refreshStatus();
  } catch (error) { log("Command failed: " + error.message); }
  finally { button.disabled = false; button.textContent = old; }
}
document.querySelectorAll(".nav").forEach(button => button.addEventListener("click", () => {
  document.querySelectorAll(".nav").forEach(item => item.classList.toggle("active", item === button));
  document.querySelectorAll(".view").forEach(view => view.classList.toggle("hidden", view.id !== button.dataset.view));
  if (button.dataset.view === "files") refreshFiles();
  if (button.dataset.view === "settings") refreshSettings();
}));
document.querySelectorAll("[data-command]").forEach(button => button.addEventListener("click", () => runCommand(button.dataset.command, button)));
$("refresh").addEventListener("click", refreshStatus);
$("fileFilter").addEventListener("input", refreshFiles);
$("clearLog").addEventListener("click", () => log("Console cleared."));
refreshStatus();
