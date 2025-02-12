from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            print("Received the following message:", message)
            await websocket.send_text(
                f"Who are you? And what the hell do you mean by {message}"
            )
            print("Sent 5 echoes from backend to frontend")
    except:
        await websocket.close()
