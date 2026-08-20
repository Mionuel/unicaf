import api from "src/features/shared/services/api";

export async function seedDB() {
  const res = await api.post("/seed");
  return true;
}
