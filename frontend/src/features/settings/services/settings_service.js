import api from "src/features/shared/services/api";

// fetches the current settings from the backend
export async function fetchSettings() {
  try {
    const res = await api.get("/settings");
    return res.data;
  } catch (error) {
    console.error("Failed to fetch settings:", error);
    throw error;
  }
}

// updates the settings on the backend
export async function updateSettings(newSettings) {
  try {
    const res = await api.put("/settings", newSettings);
    return res.data;
  } catch (error) {
    console.error("Failed to update settings:", error);
    throw error;
  }
}

// resets and seeds the database with the provided settings
export async function seedDB(seedSettings) {
  try {
    const res = await api.post("/seed", seedSettings);

    return res.data;
  } catch (error) {
    console.error("Failed to seed DB:", error);
    throw error;
  }
}
