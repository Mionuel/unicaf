import { Box } from "@mui/material";
import { useSocket } from "src/features/simulation/hooks/useSocket";
import SeatView from "src/features/simulation/components/SeatView";
import { SEAT_SIZE } from "src/features/simulation/helpers/constants";

export default function TableView({ tableId = 0 }) {
  const { seats } = useSocket();

  // Filter and sort seats belonging to this table
  const tableSeats = seats
    .filter((s) => s.table_id === tableId)
    .sort((a, b) => a.id - b.id);

  const tableHeight = 2 * SEAT_SIZE;

  // Take seats 0-1 for the left side and 2-3 for the right side
  // no seat => null
  const leftSeats = [tableSeats[0] || null, tableSeats[1] || null];
  const rightSeats = [tableSeats[2] || null, tableSeats[3] || null];

  return (
    <Box sx={{ display: "flex", alignItems: "center", gap: "4px" }}>
      {/* Left seats */}
      <Box sx={{ display: "flex", flexDirection: "column", gap: "4px" }}>
        {leftSeats.map((seat, i) => (
          <SeatView key={`left-${i}`} seat={seat} />
        ))}
      </Box>

      {/* Table rectangle */}
      <Box
        sx={{
          width: 20,
          height: tableHeight,
          backgroundColor: "grey.400",
          borderRadius: 1,
          flexShrink: 0,
        }}
      />

      {/* Right seats */}
      <Box sx={{ display: "flex", flexDirection: "column", gap: "4px" }}>
        {rightSeats.map((seat, i) => (
          <SeatView key={`right-${i}`} seat={seat} />
        ))}
      </Box>
    </Box>
  );
}
