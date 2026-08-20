import { Button, Stack, Typography } from "@mui/material";
import { useState } from "react";
import NumberField from "src/features/settings/components/NumberField";
import { seedDB } from "src/features/settings/services/settings_service";

function SettingsPage() {
  // const [simSettings, setSimSettings] = useState({
  //   peoplePerSecond: 2,
  //   simulationInterval: 0.2,
  //   maxQueueSize: 50,
  // });

  // const handleSimChange = (key) => (event) => {
  //   const newValue = event?.target ? Number(event.target.value) : Number(event);
  //   setSimSettings((prev) => ({ ...prev, [key]: newValue }));
  // };

  const [seedSettings, setSeedSettings] = useState({
    peopleTotal: 1000,
    tablesTotal: 20,
  });

  // Curried function for Seeding Settings
  const handleSeedChange = (key) => (event) => {
    const newValue = event?.target ? Number(event.target.value) : Number(event);
    setSeedSettings((prev) => ({ ...prev, [key]: newValue }));
  };

  const handleSeed = async () => {
    const result = await seedDB(seedSettings);
    console.log(result);
  };

  return (
    <>
      <Stack>
        <Typography variant="h4">Simulation Settings</Typography>
      </Stack>

      <Stack direction="column" spacing={4}>
        <Typography variant="h4">Seeding Settings</Typography>

        <Stack direction="column" sx={{ maxWidth: 200 }}>
          <Stack direction="column" spacing={2}>
            <NumberField
              type="number"
              label="People"
              min={100}
              max={10000}
              value={seedSettings.peopleTotal}
              onChange={handleSeedChange("peopleTotal")}
            />

            <NumberField
              type="number"
              label="Tables"
              min={20}
              max={100}
              value={seedSettings.tablesTotal}
              onChange={handleSeedChange("tablesTotal")}
            />
          </Stack>
        </Stack>
        <Button variant="contained" onClick={handleSeed} sx={{ maxWidth: 100 }}>
          Seed DB
        </Button>
      </Stack>
    </>
  );
}

export default SettingsPage;
