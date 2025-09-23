#from tusan.interpreter import *
import asyncio

code = """
set x to 10
print(x + x)
"""

"""
intr = Interpreter().setup(file="scripts/test.tusk",ext=["lang/load.json"])

intr.addCompileCheck()

asyncio.run(intr.compile())
"""

import tusan.lexer.Lexer