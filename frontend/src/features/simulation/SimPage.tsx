import { Button, Stack } from "@mui/material";
import {
  startSimulation,
  stopSimulation,
} from "src/features/simulation/services/sim_service";

function SimPage() {
  const handleStart = async () => {
    const result = await startSimulation();
    console.log(result);
  };

  const handleStop = async () => {
    const result = await stopSimulation();
    console.log(result);
  };

  return (
    <div>
      <h1>Welcome to the Simulation Page!</h1>
      <Stack direction="row" spacing={2}>
        <Button variant="contained" color="success" onClick={handleStart}>
          Start
        </Button>
        <Button variant="contained" color="error" onClick={handleStop}>
          Stop
        </Button>
      </Stack>
    </div>
  );
}

export default SimPage;
