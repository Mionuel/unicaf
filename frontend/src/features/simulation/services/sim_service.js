import api from "src/features/shared/services/api";

export async function startSimulation() {
  const res = await api.post("/start");
  return res.data;
}

export async function stopSimulation() {
  const res = await api.post("/stop");
  return res.data;
}

export async function fetchTableCount() {
  const response = await api.get("/table/");
  return response.data.total_tables ?? 0;
}
export async function fetchPerson(personId) {
  const res = await api.get(`/people/${personId}`);
  return res.data;
}
