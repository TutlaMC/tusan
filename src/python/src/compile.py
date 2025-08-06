# This file will let you test your code without intializing Discord
import sys
import asyncio
from tusk.interpreter import Interpreter
import json
file = sys.argv[1]
interpreter = Interpreter()

interpreter.setup(file=file)
if "--debug" in sys.argv:
    interpreter.debug = True
if "--tokens" in sys.argv:
    print(interpreter.tokens)


asyncio.run(interpreter.compile())
if "--data" in sys.argv:
    print(interpreter.data)
if "--vars" in sys.argv:
    print(interpreter.data["vars"])
if "--funcs" in sys.argv:
    print(interpreter.data["funcs"])
if "--events" in sys.argv:
    print(interpreter.data["events"],"\n")
if "--event-executors" in sys.argv:
    print(event_executors)
if "--return" in sys.argv:
    print(interpreter.return_value)
print("==========================================================\n")
