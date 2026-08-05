# OPEN ROUTER AGENT

from agents import Agent, Runner, AsyncOpenAI , RunConfig, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()

openRouterapi_key = os.getenv("OPENROUTER_API_KEY")

my_Firstagent: Agent = Agent(
    name="English professor",
    instructions="""
    - You are an Experienced English tutor your job is to help begginer students in english language
    - DO NOT answer if request is not about English questions
    - DO NOT generate answer on yourself if question are not about English language or vocabulary
    - Your Answer should be in 2 to 3 lines max
    - You can simply refuse the answer if you don't know
    """)

my_Secondagent: Agent = Agent(
    name="Travel agent",
    instructions="""
    - You are a world famous traveling agent, and guide people for diffrent tours
    - DO NOT answer if request is not about Traveling 
    - DO NOT generate answer on yourself if question are not about Traveling help
    - You can simply refuse the answer if you don't know
    """)

if not openRouterapi_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=openRouterapi_key,
    base_url="https://openrouter.ai/api/v1"

)

external_client2 = AsyncOpenAI(
    api_key=openRouterapi_key,
    base_url="https://openrouter.ai/api/v1"

)


model = OpenAIChatCompletionsModel(
    model="deepseek/deepseek-r1-0528:free",
    openai_client=external_client
)


config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
my_Prompt = input("Give me your english sentence: \n"  )
agent_Response = Runner.run_sync(my_Firstagent, my_Prompt , run_config=config)
print(agent_Response.final_output)
