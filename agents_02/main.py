from agents import Agent,SQLiteSession,GuardrailFunctionOutput,input_guardrail ,output_guardrail,InputGuardrailTripwireTriggered,OutputGuardrailTripwireTriggered , OpenAIChatCompletionsModel , AsyncOpenAI , RunConfig , Runner ,set_tracing_disabled , RunContextWrapper
from dotenv import load_dotenv
import os , asyncio 
from guardrail_schema.data import Data_schema
from dotenv import load_dotenv

load_dotenv()
set_tracing_disabled(True)

setApi = os.getenv('GEMINI_API_KEY')
setBase = os.getenv('GEMINI_BASE_PATH')

if not setApi:
    raise ValueError("GEMINI_API_KEY is not set")

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
    tracing_disabled=False
)


# SESSION HISROTY MANAGING
session = SQLiteSession("user_7")



# MAIN GUARDRAIL
# MAIN GUARDRAIL AGENT CALL LLM

Main_guardrail_agent = Agent[Data_schema](
    name="Guardrail agent",
    instructions="check cricket agent instructions",
    model=model,
    output_type=Data_schema
    )

# GUARDRAIL INPUT FUNCTION

@input_guardrail
async def guardrail_input(ctx:RunContextWrapper,agent,input):
    result = await Runner.run(Main_guardrail_agent, context=ctx.context,input=input)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        # tripwire_triggered=True ,  if True that means bad input from user
        tripwire_triggered= not result.final_output.is_cricket_query
    )


# GUARDRAIL OUTPUT FUNCTION
@output_guardrail
async def guardrail_output(ctx:RunContextWrapper,agent,output):
    result = await Runner.run(Main_guardrail_agent, context=ctx.context,input=output)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        # tripwire_triggered=True , if True that means bad input from user
        tripwire_triggered = result.final_output.salary_related_query # ye guard kry ga salary related query ko
    )

cricket_agent = Agent(
    name="Cricket Analyst",
    instructions="""
    - you are a professional cricket analyst and retired international cricketer
    - You are expert in explainig:batting techniques, fast bowling, pitch analysis, dressing room environment, team culture, players daily routine and diet, post match analysis and prematch analysis 
    - Your job is to answer cricket related questions only.
    - Your answer should be in 3 to 8 lines max
""",
    model=model,
    input_guardrails=[guardrail_input],
    output_guardrails=[guardrail_output]
    # tool_use_behavior="stop_on_first_tool"         
)

while True:
    prompt = input("Hello I am Former international cricketer! Ask your query \n")
    if prompt == "close":
        break
    
    try:
        async def run_agent():
            Response = await Runner.run(
                cricket_agent,
                prompt,
                session=session
            )
            print(Response.final_output)

        asyncio.run(run_agent())

    except InputGuardrailTripwireTriggered as bad_Input:
        print(f"{bad_Input}: Mujh sy sirf cricket ka sawal poochiye, Me apko jwab don ga")

    except OutputGuardrailTripwireTriggered as bad_output:
        print(f"{bad_output}: Faltoo sawal mat kiya karo")
