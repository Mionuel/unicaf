import { Button } from "@mui/material";
import { seedDB } from "src/features/settings/services/settings_service";

function SettingsPage() {
  const greeting = "Hello Settings Component!";

  const handleSeed = async () => {
    const result = await seedDB();
    console.log(result);
  };

  return (
    <>
      <h1>{greeting}</h1>
      <Button variant="contained" onClick={handleSeed}>
        Seed Database
      </Button>
    </>
  );
}

export default SettingsPage;
