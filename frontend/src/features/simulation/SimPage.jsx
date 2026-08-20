import { Button, Stack } from "@mui/material";
import QueueView from "src/features/simulation/components/QueueView";
import { SocketProvider } from "src/features/simulation/context/SocketProvider";
import {
  startSimulation,
  stopSimulation,
} from "src/features/simulation/services/sim_service";
import HallView from "src/features/simulation/components/HallView";

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
    <>
      <h1>Welcome to the Simulation Page!</h1>
      <SocketProvider>
        <Stack direction="column" spacing={2}>
          <QueueView />
          <HallView />
        </Stack>
      </SocketProvider>
      <Stack direction="row" spacing={2}>
        <Button variant="contained" color="success" onClick={handleStart}>
          Start
        </Button>
        <Button variant="contained" color="error" onClick={handleStop}>
          Stop
        </Button>
      </Stack>
    </>
  );
}

export default SimPage;
