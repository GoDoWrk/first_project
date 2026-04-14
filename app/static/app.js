async function refreshStatuses() {
  const statusNodes = document.querySelectorAll("[data-service-id]");
  if (!statusNodes.length) return;

  try {
    const response = await fetch("/api/statuses", { cache: "no-store" });
    if (!response.ok) return;
    const payload = await response.json();

    statusNodes.forEach((node) => {
      const id = node.dataset.serviceId;
      const item = payload.services[id];
      if (!item) return;

      node.classList.remove("status-online", "status-offline", "status-unknown");

      if (item.status === "online") {
        node.textContent = "Online";
        node.classList.add("status-online");
      } else if (item.status === "offline") {
        node.textContent = "Offline";
        node.classList.add("status-offline");
      } else {
        node.textContent = "Status off";
        node.classList.add("status-unknown");
      }
    });
  } catch (error) {
    console.warn("Failed to refresh statuses", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const refreshButton = document.getElementById("refresh-status");
  if (refreshButton) {
    refreshButton.addEventListener("click", refreshStatuses);
  }
  refreshStatuses();
});
