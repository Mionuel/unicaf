import { useEffect, useState } from "react";
import { Box, Stack, Typography } from "@mui/material";
import TableView from "src/features/simulation/components/TableView";
import { fetchTableCount } from "src/features/simulation/services/sim_service";

function HallView() {
  const [tableCount, setTableCount] = useState(0);

  useEffect(() => {
    const loadTableCount = async () => {
      const total = await fetchTableCount();
      setTableCount(total);
    };

    loadTableCount();
  }, []);

  const tableIds = Array.from({ length: tableCount }, (_, index) => index + 1);

  return (
    <Stack alignItems="center" spacing={1}>
      <Typography variant="h4" align="center">
        Tables
      </Typography>
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: "repeat(10, 1fr)",
          gap: 1,
          width: "100%",
        }}
      >
        {tableIds.length > 0 ? (
          tableIds.map((id) => (
            <Box
              key={id}
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                minWidth: 100,
              }}
            >
              <TableView tableId={id} />
            </Box>
          ))
        ) : (
          <TableView />
        )}
      </Box>
    </Stack>
  );
}

export default HallView;
