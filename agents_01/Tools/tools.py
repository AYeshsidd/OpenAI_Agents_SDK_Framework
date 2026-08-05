from agents import function_tool , RunContextWrapper , FunctionTool
from pydantic import BaseModel


class user_data(BaseModel):
    name:str
    Field:str
    age:int

class tool_schema(BaseModel):
    sentense:str

async def negative_tense(ctx:RunContextWrapper,arg):
    object = tool_schema.model_validate_json(arg)
    sentence = object.sentense
    words = sentence.split()
    auxiliaries = ["am", "is", "are", "was", "were",
                   "has", "have", "will_be", "had",
                   "will", "shall", "can", "may",
                   "should", "would", "could", "might", "must",
                   "do", "does", "did"]

    for i, word in enumerate(words):
        if word.lower() in auxiliaries:
            words.insert(i+1, "not")
            return " ".join(words)

    words.insert(1, "not")
    return " ".join(words)

tense = FunctionTool(
    name="negative_tense",
    description="Convert any given sentence into negative tense",
    params_json_schema=tool_schema.model_json_schema(),
    on_invoke_tool=negative_tense
    
)

# @function_tool
# def get_age(ctx:RunContextWrapper[user_data]):
#     """This tool runs when Query is relate to age """
#     print("AGE TOOL FIRE --->")
#     print("CTX =", ctx.context.age) 
#     return f"User Age is {ctx.context.age}"



@function_tool
def plus_numbers(a: int, b: int) -> str:
    """Add two numbers and return the sum"""
    print("PLUS TOOL FIRE --->")
    return f"your answer is {a+b}"

@function_tool
def subtract_numbers(a: int, b: int) -> str:
    """subtract two numbers and return the answer"""
    print("MINUS TOOL FIRE --->")
    return f"your answer is {a+-b}"

@function_tool
def divide_numbers(a: int, b: int) -> str:
    """Return the result of dividing a by b."""
    print("division TOOL FIRE --->")
    return f"your answer is {a/b}"


# AGENT LEVEL CONTEXT DYANMIC INSTRUCTION

# def dynamic(ctx:RunContextWrapper,agent):
#     print("DYNAMIC CALLED with context:", ctx.context)
#     return f"Hello {ctx.context['name']}"
