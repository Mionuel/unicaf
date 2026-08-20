import { useState } from "react";
import { Box, Popover, Card, CardContent, Typography } from "@mui/material";

import { useSocket } from "src/features/simulation/hooks/useSocket";

const QUEUE_SIZE = 50;

function QueueView() {
  const { queueEntries } = useSocket();

  const [popoverAnchor, setPopoverAnchor] = useState(null);
  const [selectedCell, setSelectedCell] = useState(null);

  const handleCellClick = (event, entry, position) => {
    setPopoverAnchor(event.currentTarget);
    setSelectedCell({
      entry: entry ?? null,
      position,
      time: entry
        ? formatTime(Date.now() - new Date(entry.joined_at).getTime())
        : null,
    });
  };

  const handlePopoverClose = () => {
    setPopoverAnchor(null);
    setSelectedCell(null);
  };

  const cells = Array.from({ length: QUEUE_SIZE }, (_, index) => {
    const entry = queueEntries[index];
    const isOccupied = Boolean(entry);

    return (
      <Box
        key={index}
        onClick={(event) => handleCellClick(event, entry, index)}
        sx={{
          width: 40,
          height: 40,
          border: "1px solid #c6c6c6",
          backgroundColor: isOccupied ? "green" : "white",
          cursor: "pointer",
        }}
      />
    );
  });

  return (
    <>
      <Box
        sx={{
          width: "100%",
          display: "grid",
          gridTemplateColumns: "repeat(25, 40px)",
          gap: "4px",
          justifyContent: "center",
        }}
      >
        {cells}
      </Box>

      <Popover
        anchorEl={popoverAnchor}
        open={Boolean(popoverAnchor)}
        onClose={handlePopoverClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
        transformOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Card sx={{ minWidth: 200 }}>
          <CardContent>
            <Typography variant="body2" color="text.secondary">
              Position in queue:{" "}
              {selectedCell !== null ? selectedCell.position + 1 : "-"} /{" "}
              {QUEUE_SIZE}
            </Typography>
            {selectedCell?.entry ? (
              <>
                <Typography variant="body2">
                  Person ID: {selectedCell.entry.person_id}
                </Typography>
                <Typography variant="body2">
                  Time in queue: {selectedCell.time}
                </Typography>
              </>
            ) : (
              <Typography variant="body2" color="text.secondary">
                This spot is empty.
              </Typography>
            )}
          </CardContent>
        </Card>
      </Popover>
    </>
  );
}

export default QueueView;
