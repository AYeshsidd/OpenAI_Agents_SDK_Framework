import chainlit as cl

@cl.on_message # taking input

async def main(message: cl.Message):
    await cl.Message(
        content=f"chainlit: {message.content}",
    ).send()