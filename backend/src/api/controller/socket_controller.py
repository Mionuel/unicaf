from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.controller.queue_controller import list_queue_now

from psycopg import Connection

from api.controller.seat_controller import fetch_all_seats

router = APIRouter(
    prefix="/ws",
    tags=["Web Socket"]
)

current_client: WebSocket | None = None

@router.websocket("/")
async def state_socket(websocket: WebSocket):
    """
        A web socket endpoint for seding the simulation state
        The simulation state includes the queue entries and seat data
    """
    # needed because the actual data is sent in broadcast_state, not here
    global current_client

    await websocket.accept()
    current_client = websocket

    try:
        while True:
            # doesn't actually receive, just keeps the conncetion alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        current_client = None

async def broadcast_state(db: Connection):
    # If no one is connected to the websocket => return
    if current_client is None:
        return

    # fetch all current queue entries
    queue_entries = list_queue_now(db)
    seats = fetch_all_seats(db)

    payload = {
        # converts the QueueEntry / SeatResponse objects into dicts
        "queue": [entry.model_dump(mode="json") for entry in queue_entries],
        "seats": [seat.model_dump(mode="json") for seat in seats],
    }

    # send the payload
    await current_client.send_json(payload)
