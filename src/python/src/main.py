#from tusan.interpreter import *
import asyncio
import json
from tusan.interpreter.Interpreter import Interpreter

with open("lang/load.json","r") as f:
    e = json.load(f)
intr = Interpreter().setup(file="scripts/test.tusk",ext=[e])

intr.addCompileCheck()

asyncio.run(intr.compile())