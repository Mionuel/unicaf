import { AppBar, Tab, Tabs, Toolbar } from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";

function NavBar() {
  const location = useLocation();
  const navigate = useNavigate();

  const routes = [
    { label: "Simulation", path: "/" },
    { label: "Settings", path: "/settings" },
    { label: "Grafana", path: "/grafana" },
  ];

  const currentPath = routes.some((r) => r.path === location.pathname)
    ? location.pathname
    : false;

  return (
    <AppBar position="static" sx={{ bgcolor: "royalblue" }}>
      <Toolbar variant="dense">
        <Tabs
          value={currentPath}
          onChange={(_, newPath) => navigate(newPath)}
          textColor="inherit"
        >
          {routes.map((route) => (
            <Tab key={route.path} label={route.label} value={route.path} />
          ))}
        </Tabs>
      </Toolbar>
    </AppBar>
  );
}

export default NavBar;
