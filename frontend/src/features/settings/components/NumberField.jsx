import { Stack, Typography } from "@mui/material";

function NumberField({ label, ...props }) {
  return (
    <Stack spacing={1}>
      <Typography component="label" variant="h6">
        {label}
      </Typography>
      <input type="number" style={{ padding: "8px" }} {...props} />
    </Stack>
  );
}

export default NumberField;
