import { createBrowserRouter } from "react-router-dom";
import App from "src/App";
import NotFound from "src/features/notfound/NotFound";

const router = createBrowserRouter([
  { path: "/simulation", element: <App /> },
  { path: "/settings", element: <App /> },
  { path: "/grafana", element: <App /> },
  { path: "*", element: <NotFound /> },
]);

export default router;
