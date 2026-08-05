from agents import Agent, Runner, AsyncOpenAI , RunConfig, OpenAIChatCompletionsModel 

import os 
from tools import tool_add, tool_subtract

from dotenv import load_dotenv
load_dotenv()

# setApi = os.getenv('GEMINI_API_KEY')
setApi = os.getenv("OPENAI_API_KEY")

# setBase = os.getenv('GEMINI_BASE_PATH')
# print(setApi)

client = AsyncOpenAI(api_key=setApi)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gpt-4o-mini"

)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled= True  #stop tracing

    
)

cooking_agent: Agent = Agent(
    name="Cooking Expert",
     handoff_description="Specialist in making food",
    instructions="""
    - You are a Cooking expert in pakistani dishes. 
    - Your answer should not be exceed to 5 lines
    - DO NOT reply if the question is not related to Cooking or food.
    - Do NOT generate answer if question are other then cooking and food or you can simply say I don't know about this".
    """,
)

Math_agent: Agent = Agent(
    name="Maths Expert",
    handoff_description="Specialist in mathematics queries",
 
    instructions="""
    - your response should be clean 
    - always check first that calling tools in needed if yes call tool, instead solve query by yourself.
    - after each step write half line explanaition
    - Do NOT generate answer if question are other then Mathematics simply say i am unable to understand".
    """,
    tools=[tool_add,tool_subtract]
    
)

English_agent: Agent = Agent(
    name="English Expert",
     handoff_description="Specialist in teaching english Language",
    instructions="""
    - You are expert in Teaching English langugae. 
    - For any addition problem, call the tool 'tool_add'
    - DO NOT reply if the question is not related to the english.
    - Do NOT generate answer if question are other then cooking and food or you can simply say I don't understand, sorry!".
    """,
    
)

General_agent: Agent = Agent(
    "GeneralAgent",
    instructions="""
     - You are a General agent
     - Hand off to Math agent if input is related to math or any kind of calculation
     - Hand off to Cooking agent if input is related to food
     - Hand off to English agent if input is related to any english language query
     """,
    handoffs=[Math_agent, cooking_agent, English_agent])


prompt= input("Ask your Query:")
agent_Response  = Runner.run_sync(General_agent,prompt,run_config=config) 
print(agent_Response)


# async def run_():
#  prompt= input("Ask your Query:")
#  agent_Response  = await Runner.run(General_agent,prompt,run_config=config) 
#  print(agent_Response.final_output)


# METHOD AGENT UPDATED_STREAM EVENT
# async def run_streaming():
#   prompt= input("Ask your Query:")
#   agent_Response  = Runner.run_streamed(General_agent,prompt,run_config=config) 
#   async for checking_events in agent_Response.stream_events():
#     # testing event
#      if checking_events.type == "agent_updated_stream_event":
#     #   print(checking_events) 
#       print(f"Agent update: {checking_events.type}") # it displays how many types of events are fire
    

# asyncio.run(run_streaming())


#  # METHOD RAW RESPONSE_STREAM EVENT
# async def run_streaming():
#   prompt= input("Ask your Query:")
#   agent_Response  = Runner.run_streamed(General_agent,prompt,run_config=config) 
#   async for checking_events in agent_Response.stream_events():
#     # testing event
#      if checking_events.type == "raw_response_event" and isinstance(checking_events.data,ResponseTextDeltaEvent): 
      
#       print(checking_events.data.delta, end="", flush=True) FOR GETTING FINAL OUTPUT
    
# asyncio.run(run_streaming())



# METHOD RUN ITEM_STREAM EVENT
# async def run_streaming():
#   prompt= input("Ask your Query:")
#   agent_Response  = Runner.run_streamed(General_agent,prompt,run_config=config) 
#   async for checking_events in agent_Response.stream_events():
#     # testing event
#      if checking_events.type == "run_item_stream_event": 

#        if checking_events.item.type  == "message_output_item":
#         print(f"---Message Output:{ItemHelpers.text_message_output(checking_events.item)}") # FOR GETTING FINAL OUTPUT
     
     
# asyncio.run(run_streaming())
