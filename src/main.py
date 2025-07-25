from tusk.interpreter import *
import asyncio
intr = Interpreter().setup(file="scripts/test.tusk",ext=["lang/load.json"])
asyncio.run(intr.compile())