import { useEffect, useState } from "react";
import {
  Box,
  Popover,
  Card,
  CardContent,
  Typography,
  Stack,
} from "@mui/material";

import { useSocket } from "src/features/simulation/hooks/useSocket";
import { formatTime } from "src/features/simulation/helpers/formatting";
import { fetchSettings } from "src/features/settings/services/settings_service";
import { PersonView } from "src/features/simulation/components/PersonView";

function QueueView() {
  const { queueEntries } = useSocket();

  const [popoverAnchor, setPopoverAnchor] = useState(null);
  const [selectedCell, setSelectedCell] = useState(null);
  const [maxQueueSize, setMaxQueueSize] = useState(50);

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

  useEffect(() => {
    const loadSettings = async () => {
      const settings = await fetchSettings();

      setMaxQueueSize(settings.max_queue_size);
    };

    loadSettings();
  }, []);

  const cells = Array.from({ length: maxQueueSize }, (_, index) => {
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
      <Stack alignItems="center" spacing={1}>
        <Typography variant="h4" align="center">
          Queue
        </Typography>
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
      </Stack>

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
              {maxQueueSize}
            </Typography>
            {selectedCell?.entry ? (
              <>
                <PersonView personId={selectedCell.entry.person_id} />
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
