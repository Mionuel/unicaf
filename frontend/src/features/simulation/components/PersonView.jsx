import { useState, useEffect } from "react";
import { Typography, Box } from "@mui/material";
import { fetchPerson } from "src/features/simulation/services/sim_service";

export function PersonView({ personId }) {
  const [person, setPerson] = useState(null);

  useEffect(() => {
    if (personId) {
      fetchPerson(personId).then((data) => setPerson(data));
    }
  }, [personId]);

  // the id will be shown until the full data is fetched from the backend
  if (!person) {
    return (
      <Typography variant="body2" color="text.secondary">
        Person ID: {personId}
      </Typography>
    );
  }

  return (
    <Box>
      <Typography variant="body2">Person ID: {personId}</Typography>
      <Typography variant="body2">Name: {person.name}</Typography>
      <Typography variant="body2">
        Credits: {person.credit.toFixed(2)}
      </Typography>
      <Typography variant="body2">
        Bonus Points: {person.bonus_points}
      </Typography>
    </Box>
  );
}
