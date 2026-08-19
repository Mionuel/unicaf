import { useContext } from "react";
import SocketContext from "src/features/simulation/context/SocketProvider";

export const useSocket = () => {
  const context = useContext(SocketContext);

  if (!context)
    throw new Error("useSocket can only be used inside SocketProvider wrapper");

  return context;
};
