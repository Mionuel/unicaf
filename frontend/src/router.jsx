import { createBrowserRouter } from "react-router-dom";
import GrafanaViewer from "src/features/grafana/GrafanaView";
import NotFound from "src/features/notfound/NotFound";
import Layout from "src/features/shared/components/Layout";
import SimPage from "src/features/simulation/SimPage";
import SettingsPage from "src/features/settings/SettingsPage";

const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: "/", element: <SimPage /> },
      { path: "/settings", element: <SettingsPage /> },
      { path: "/grafana", element: <GrafanaViewer /> },
      { path: "*", element: <NotFound /> },
    ],
  },
]);

export default router;
