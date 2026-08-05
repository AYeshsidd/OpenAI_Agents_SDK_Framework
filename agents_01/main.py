from agents import Agent, Runner ,  AsyncOpenAI , RunConfig,  OpenAIChatCompletionsModel , ItemHelpers , enable_verbose_stdout_logging
from openai.types.responses import ResponseTextDeltaEvent
from agents.agent import StopAtTools
import os , asyncio 
from Tools.tools import divide_numbers , subtract_numbers , plus_numbers   , user_data , tense
from Instruction.dynamic_work import dynamic

from dotenv import load_dotenv

load_dotenv()

setApi = os.getenv('GEMINI_API_KEY')
setBase = os.getenv('GEMINI_BASE_PATH')

if not setApi:
    raise ValueError("GEMINI_API_KEY is not set")

#Reference: https://ai.google.dev/gemini-api/docs/openai

client = AsyncOpenAI(
    api_key=setApi,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
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

# CONTEXT MANAGEMT & DYNAMIC INSTRUCTION
Math_agent: Agent = Agent[user_data](
    name="Maths Expert",
    handoff_description="Specialist in mathematics queries",
    instructions=dynamic,
    tools=[divide_numbers , subtract_numbers , plus_numbers ] ,
    tool_use_behavior= "stop_on_first_tool",
    model=model
)

English_agent: Agent = Agent(
    name="English Expert",
    tools=[tense],   # PRACTICING CUSTOM TOOLS
     handoff_description="Specialist in teaching english Language: translations, meanings, tense changing, grammar etc.",
    instructions="""
    - You are expert in Teaching English langugae. 
    - If the query is about English translation, word meaning, grammar, or sentence conversion → call the tool or provide explanation.
    - Do NOT generate answer if question are other you can simply say I don't understand, sorry!".
    """,
    
)

# print(English_agent.tools)  checking diffrence b/w tool and custom tool 

General_agent: Agent = Agent(
    "GeneralAgent",
    instructions="""
     - You are a General agent
     - Hand off to Math agent if input is related to math or any kind of calculation
     - Hand off to cooking agent if input is related to food
     - Hand off to English agent if input is related to any english sentence or english language query
     """,
    handoffs=[Math_agent, cooking_agent, English_agent])


# SESSION MANAGEMNT
# session = SQLiteSession("user_1")

user_Info = user_data(name ="AYesh_sidd",Field = "Ai Agents",age = 28)

while True:
    prompt = input("Ask your query man: ")
    if prompt in( "close" , "out"):
        break

    agent_Response  = Runner.run_sync(
        Math_agent,
        input=prompt,
        context=user_Info,
        run_config=config,
        ) 

    print(agent_Response.final_output)


# async def run_():
#   prompt= input("Ask your Query:")
#   agent_Response  = await Runner.run(General_agent,prompt,run_config=config,max_turns=7) 
#   print(agent_Response.final_output)

# asyncio.run(run_())

# METHOD AGENT UPDATED_STREAM EVENT
# async def run_streaming():
#    prompt= input("Ask your Query:")
#    agent_Response  = Runner.run_streamed(General_agent,prompt,run_config=config) 
#    async for checking_events in agent_Response.stream_events():
#      # testing event
#       if checking_events.type == "agent_updated_stream_event":
#      #   print(checking_events) 
#        print(f"Agent update: {checking_events.new_agent.name}") # it displays how many types of events are fire0

# asyncio.run(run_streaming())
    

#  METHOD RAW RESPONSE_STREAM EVENT
# async def run_streaming():
#   prompt= input("Ask your Query:")
#   agent_Response  = Runner.run_streamed(Math_agent,prompt,run_config=config) 
#   async for checking_events in agent_Response.stream_events():
#     # testing event
#      if checking_events.type == "raw_response_event" and isinstance(checking_events.data,ResponseTextDeltaEvent): 
#              print(checking_events.data.delta, end="", flush=True) #FOR GETTING FINAL OUTPUT
    
# asyncio.run(run_streaming())

# METHOD RUN ITEM_STREAM EVENT
# async def run_streaming():
#   prompt= input("Ask your Query:")
#   agent_Response  = Runner.run_streamed(General_agent,prompt,run_config=config) 
#   async for checking_events in agent_Response.stream_events():
#     # testing event
#      if checking_events.type == "run_item_stream_event": 

#        if checking_events.item.type  == "message_output_item":
#         print(f"---Message Output:\n {ItemHelpers.text_message_output(checking_events.item)}") # FOR GETTING FINAL OUTPUT
     
     
# asyncio.run(run_streaming())




