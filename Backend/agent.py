from dotenv import load_dotenv
import os
from Rag.Rag import retrieve
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions,RoomOutputOptions,RunContext
from livekit.plugins import (
    openai,
    noise_cancellation,

)

from datetime import datetime
from livekit.agents.llm import function_tool
from livekit.plugins import google

load_dotenv()
print("Environment variables loaded.")
print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")

    @function_tool
    async def VoiceAgentTask(self, context: RunContext, query: str) -> str:
        """Get information about the Voice AI Agent Task or any related details."""
        # print("get_current_date_and_time called with context:", dir(context))
        # current_datetime = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        retrieved_data = retrieve(query, top_k=1)
        res =f"the retrived data is : {retrieved_data[0]['text']}"
        

        return res
    


async def entrypoint(ctx: agents.JobContext):

    
    async def send_text_to_frontend(session, text: str):
        """Send any text back to the frontend UI."""
        await session.data.publish(text.encode("utf-8"))


    session = AgentSession(
        llm=google.realtime.RealtimeModel(
        model="gemini-2.5-flash-native-audio-preview-09-2025",
        voice="Puck",
        temperature=0.8,
        instructions="You are a helpful assistant",
    ),
    
    )
    

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
        
    )

    # @ctx.room.on("track_published")
    # async def handle_track(track, participant):
    #     if track.kind == "audio":
    #         await session.listen_to(track)
    

        
        

    await session.generate_reply(
        instructions="Greet the user and offer your assistance. You should start by speaking in English."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))