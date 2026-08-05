from agents import function_tool

@function_tool
def tool_add(a: int, b: int) -> int:
    """Add two numbers and return the sum"""
    print("PLUS TOOL FIRE --->")
    return a + b

@function_tool
def tool_subtract(a: int, b: int) -> int:
    """subtract two numbers and return the answer"""
    print("MINUS TOOL FIRE --->")
    return a +- b


