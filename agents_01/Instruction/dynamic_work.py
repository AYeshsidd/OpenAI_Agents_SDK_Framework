from agents import RunContextWrapper , Agent
from Tools.tools import user_data

def dynamic(ctx:RunContextWrapper[user_data],agent:Agent[user_data]):
    
    return f"user name is {ctx.context.name} , user Field is {ctx.context.Field} , user age is {ctx.context.age} you are an experienced Maths teacher "
