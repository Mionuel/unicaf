import { Outlet } from "react-router-dom";
import NavBar from "src/features/shared/components/NavBar";

function Layout() {
  return (
    <>
      <NavBar />
      <Outlet />
    </>
  );
}

export default Layout;
