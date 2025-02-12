import asyncio

import streamlit as st
import websockets
from streamlit.runtime.scriptrunner import add_script_run_ctx


async def connect_websocket(message: str, placeholder):
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        while True:
            try:
                response = await websocket.recv()
                st.session_state.messages.append(response)
                # Update the placeholder with all messages
                with placeholder:
                    # Clear the container
                    placeholder.empty()
                    # Display all messages in the history
                    for msg in st.session_state.messages:
                        st.write(msg)
            except websockets.exceptions.ConnectionClosed:
                break


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []


st.title("WebSocket Echo Demo")
init_session_state()

# Input field for the message
message = st.text_input("Enter a message to echo:", "Hello!")

# Create a container for messages before the button
messages_container = st.container()

# Display existing messages in the container
with messages_container:
    for msg in st.session_state.messages:
        st.write(msg)

if st.button("Start Streaming"):
    loop = asyncio.new_event_loop()
    add_script_run_ctx(loop)
    asyncio.set_event_loop(loop)
    # Pass the container to the websocket function
    loop.run_until_complete(connect_websocket(message, messages_container))
