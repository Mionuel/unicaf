import { createBrowserRouter } from "react-router-dom";
import App from "src/App";
import GrafanaViewer from "src/features/grafana/GrafanaView";
import NotFound from "src/features/notfound/NotFound";

const router = createBrowserRouter([
  { path: "/simulation", element: <App /> },
  { path: "/settings", element: <App /> },
  { path: "/grafana", element: <GrafanaViewer /> },
  { path: "*", element: <NotFound /> },
]);

export default router;
