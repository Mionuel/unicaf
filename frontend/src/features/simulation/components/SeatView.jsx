import { useState } from "react";
import { Box, Popover, Card, CardContent, Typography } from "@mui/material";
import { formatTime } from "src/features/simulation/helpers/formatting";
import { SEAT_SIZE } from "src/features/simulation/helpers/constants";
import { PersonView } from "src/features/simulation/components/PersonView";

function SeatView({ seat }) {
  const [anchorEl, setAnchorEl] = useState(null);
  const [timeRemaining, setTimeRemaining] = useState(null);

  const isOccupied = seat?.status === "occupied";

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);

    // Compute time remaining at the exact moment of the click
    if (isOccupied && seat.expires_at) {
      const remaining = new Date(seat.expires_at).getTime() - Date.now();
      setTimeRemaining(formatTime(remaining));
    }
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <>
      <Box
        onClick={handleClick}
        sx={{
          width: SEAT_SIZE,
          height: SEAT_SIZE,
          border: "1px solid #c6c6c6",
          backgroundColor: isOccupied ? "darkred" : "white",
          cursor: "pointer",
          flexShrink: 0,
        }}
      />
      <Popover
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
        transformOrigin={{ vertical: "top", horizontal: "center" }}
      >
        {/* Seat is occupied */}
        <Card sx={{ minWidth: 200 }}>
          <CardContent>
            {!seat ? (
              <Typography variant="body2" color="text.secondary">
                No seat data.
              </Typography>
            ) : isOccupied ? (
              <>
                <Typography variant="body2" color="text.secondary">
                  Seat ID: {seat.id}
                </Typography>
                <PersonView personId={seat.person_id} />
                <Typography variant="body2">
                  Time remaining: {timeRemaining}
                </Typography>
              </>
            ) : (
              // Seat if not occupied yet
              <>
                <Typography variant="body2" color="text.secondary">
                  Seat ID: {seat.id}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  This seat is free.
                </Typography>
              </>
            )}
          </CardContent>
        </Card>
      </Popover>
    </>
  );
}

export default SeatView;
