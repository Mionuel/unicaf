import api from "src/features/shared/services/api";

export async function startSimulation() {
  const res = await api.post("/start");
  return res.data;
}

export async function stopSimulation() {
  const res = await api.post("/stop");
  return res.data;
}
