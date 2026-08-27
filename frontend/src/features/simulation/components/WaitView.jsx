import { useEffect, useState } from "react";
import { Typography, Box } from "@mui/material";
import { fetchAverageWaitTime } from "src/features/simulation/services/sim_service";

function WaitView() {
  const [avgWait, setAvgWait] = useState(0);

  useEffect(() => {
    const loadWaitTime = async () => {
      const wait = await fetchAverageWaitTime();
      setAvgWait(wait);
    };
    loadWaitTime();

    const interval = setInterval(async () => {
      const wait = await fetchAverageWaitTime();
      setAvgWait(wait);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ width: "100%", display: "flex", justifyContent: "center" }}>
      <Typography variant="h6" color="text.secondary">
        Average Wait Time: {avgWait.toFixed(1)}s
      </Typography>
    </Box>
  );
}

export default WaitView;
