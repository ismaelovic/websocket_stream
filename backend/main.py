from asyncio import sleep

from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            print("Received the following message:", message)
            # Echo the received message 5 times
            for _ in range(5):
                await websocket.send_text(f"What the hell do you mean by {message}")
                await sleep(1)
            print("Sent 5 echoes from backend to frontend")
    except:
        await websocket.close()
