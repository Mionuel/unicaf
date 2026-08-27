import { Button, Stack, Typography } from "@mui/material";
import { useState, useEffect } from "react";
import NumberField from "src/features/settings/components/NumberField";
import {
  seedDB,
  fetchSettings,
  updateSettings,
} from "src/features/settings/services/settings_service";

function SettingsPage() {
  const [simSettings, setSimSettings] = useState({
    simulation_interval: 0.1,
    update_delay: 0.2,
    max_queue_size: 50,
    occupy_seconds_min: 50,
    occupy_seconds_variance: 5,
    occupy_seconds_snack: 10,
    order_cost: 10.0,
    bonus_threshold: 5,
    people_per_second: 10.0,
  });

  const [seedSettings, setSeedSettings] = useState({
    peopleTotal: 10000,
    tablesTotal: 20,
  });

  // fetches the current settings from the backend and updates them on render
  useEffect(() => {
    const loadSettings = async () => {
      try {
        const currentSettings = await fetchSettings();
        setSimSettings(currentSettings);
      } catch (error) {
        console.error("Failed to load settings:", error);
      }
    };

    loadSettings();
  }, []);

  const handleSimChange = (key) => (event) => {
    const newValue = event.target.value;
    setSimSettings((prev) => ({ ...prev, [key]: newValue }));
  };

  const handleApplySimSettings = async () => {
    const result = await updateSettings(simSettings);
    console.log("Settings successfully updated:", result);
  };

  const handleSeedChange = (key) => (event) => {
    const newValue = event?.target ? Number(event.target.value) : Number(event);
    setSeedSettings((prev) => ({ ...prev, [key]: newValue }));
  };

  const handleSeed = async () => {
    const result = await seedDB(seedSettings);
    console.log("Database seeded:", result);
  };

  return (
    <Stack direction="column" spacing={6} sx={{ pb: 8 }}>
      {/* --- SIMULATION SETTINGS SECTION --- */}
      <Stack direction="column" spacing={2}>
        <Typography variant="h4">Simulation Settings</Typography>

        <Stack direction="column" sx={{ maxWidth: 300 }} spacing={2}>
          <Stack direction="row" spacing={2}>
            <NumberField
              type="number"
              label="People per Second"
              min={0.000001}
              step={0.5}
              value={simSettings.people_per_second}
              onChange={handleSimChange("people_per_second")}
            />
            <NumberField
              type="number"
              label="Tick Interval (sec)"
              min={0.0001}
              step={0.1}
              value={simSettings.simulation_interval}
              onChange={handleSimChange("simulation_interval")}
            />
            <NumberField
              type="number"
              label="Update Delay (sec)"
              min={0.0001}
              step={0.1}
              value={simSettings.update_delay}
              onChange={handleSimChange("update_delay")}
            />
            <NumberField
              type="number"
              label="Max Queue Size"
              min={1}
              value={simSettings.max_queue_size}
              onChange={handleSimChange("max_queue_size")}
            />
          </Stack>

          {/* Seat & Time Constraints */}
          <Stack direction="row" spacing={2}>
            <NumberField
              type="number"
              label="Occupy Time (s)"
              min={1}
              value={simSettings.occupy_seconds_min}
              onChange={handleSimChange("occupy_seconds_min")}
            />
            <NumberField
              type="number"
              label="Time Variance (s)"
              min={0}
              value={simSettings.occupy_seconds_variance}
              onChange={handleSimChange("occupy_seconds_variance")}
            />
            <NumberField
              type="number"
              label="Bonus Time (s)"
              min={0}
              value={simSettings.occupy_seconds_snack}
              onChange={handleSimChange("occupy_seconds_snack")}
            />
          </Stack>

          <Stack direction="row" spacing={2}>
            <NumberField
              type="number"
              label="Order Cost"
              min={0}
              step={0.5}
              value={simSettings.order_cost}
              onChange={handleSimChange("order_cost")}
            />
            <NumberField
              type="number"
              label="Bonus Threshold"
              min={1}
              value={simSettings.bonus_threshold}
              onChange={handleSimChange("bonus_threshold")}
            />
          </Stack>
        </Stack>

        <Button
          variant="contained"
          color="success"
          onClick={handleApplySimSettings}
          sx={{ maxWidth: 150 }}
        >
          Apply
        </Button>
      </Stack>

      {/* --- SEEDING SETTINGS SECTION --- */}
      <Stack direction="column" spacing={2}>
        <Typography variant="h4">Seeding Settings</Typography>

        <Stack direction="column" sx={{ maxWidth: 300 }}>
          <Stack direction="row" spacing={2}>
            <NumberField
              type="number"
              label="Total People"
              min={100}
              max={100000}
              value={seedSettings.peopleTotal}
              onChange={handleSeedChange("peopleTotal")}
            />

            <NumberField
              type="number"
              label="Total Tables"
              min={20}
              max={100}
              value={seedSettings.tablesTotal}
              onChange={handleSeedChange("tablesTotal")}
            />
          </Stack>
        </Stack>

        <Button
          variant="contained"
          color="primary"
          onClick={handleSeed}
          sx={{ maxWidth: 100 }}
        >
          Seed DB
        </Button>
      </Stack>
    </Stack>
  );
}

export default SettingsPage;
