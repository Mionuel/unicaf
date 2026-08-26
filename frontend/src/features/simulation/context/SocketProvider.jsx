// src/context/SimulationSocketContext.tsx
import { createContext, useEffect, useState } from "react";

const SocketContext = createContext();
const WS_URL = "ws://127.0.0.1:8000/ws/";

export function SocketProvider({ children }) {
  const [queueEntries, setQueueEntries] = useState([]);
  const [seats, setSeats] = useState([]);

  useEffect(() => {
    const socket = new WebSocket(WS_URL);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setQueueEntries(data.queue ?? []);
      setSeats(data.seats ?? []);
    };

    return () => socket.close();
  }, []);

  return (
    <SocketContext.Provider value={{ queueEntries, seats }}>
      {children}
    </SocketContext.Provider>
  );
}

export default SocketContext;
