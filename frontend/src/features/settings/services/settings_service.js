import api from "src/features/shared/services/api";

export async function seedDB(seedSettings) {
  try {
    const res = await api.post("/seed", seedSettings);

    return res.data;
  } catch (error) {
    console.error("Failed to seed DB:", error);
    throw error;
  }
}
