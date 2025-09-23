import re
import asyncio

from tusan.Node import *
from tusan.nodes.expression.Condition import *

from tusan.Variable import *

class FunctionNode(Node):
    def __init__(self, token: Token):
        
        self.interpreter = token.interpreter
        self.token = token

    async def create(self):
        from tusan.interpreter import Interpreter
        from tusan.nodes.statement import StatementNode
        from tusan.nodes.expressions import ExpressionNode
        self.name = self.token.value
        self.params = []

        """
        Each Param will look like:

        function add num1 num2:NUMBER num3:NUMBER

        num1 will be: num1 (takes in expression)
        num2 will be: NUMBER:num2 
        """
        param_checks_begun = False
        while self.interpreter.get_next_token() and self.interpreter.get_next_token().type in ["IDENTIFIER"]:
            param = self.interpreter.next_token().value

            # Type
            if self.interpreter.get_next_token().type == "COLON":
                self.interpreter.next_token()
                formed_param = {
                    "name": param,
                    "type": self.interpreter.next_token().value
                }
            else:
                formed_param = {
                    "name": param,
                    "type": "ANY"
                }
            
            # Fallback
            if self.interpreter.is_token("COMPARISION:is"):
                param_checks_begun = True
                self.interpreter.next_token()
                formed_param["fallback"] = (await ExpressionNode(self.interpreter.next_token()).create()).value
            else:
                if not param_checks_begun:
                    formed_param["fallback"] = [None, 5678, "no chance"]
                else:
                    self.interpreter.error("SyntaxError", "You cannot use required paramaters after optional paramaters", notes=["Move the optional paramaters to the end of the function"])
            
            self.params.append(formed_param)
        


        self.interpreter.expect_token("KEYWORD:that")

        self.function_interpreter = Interpreter()

        # puts all the tokens in here
        self.tokens = []
        internal_structure_count = 0
        
        # Check if next token is end
        next_token = self.interpreter.get_next_token()
        if next_token is None:
            self.interpreter.error("SyntaxError", "Unexpected end of file in function definition", notes=["Make sure your function has an 'end' token"])
            return self
            
        if next_token.type == "ENDSTRUCTURE":
            self.interpreter.next_token() 
            self.tokens.append(Token("ENDSCRIPT", "", self.interpreter))
        else:
            while True:
                nxt_tkn = self.interpreter.get_next_token()
                if nxt_tkn is None:
                    self.interpreter.error("SyntaxError", "Unexpected end of file in function definition", notes=["Make sure your function has an 'end' token"])
                    return self
                
                if nxt_tkn.type == "STRUCTURE":
                    internal_structure_count += 1
                    tkn_to_append = self.interpreter.next_token()
                    tkn_to_append.interpreter = self.function_interpreter
                    self.tokens.append(tkn_to_append)
                elif nxt_tkn.type == "ENDSTRUCTURE":
                    if internal_structure_count == 0:
                        self.interpreter.next_token()
                        break
                    else:
                        tkn_to_append = self.interpreter.next_token()
                        tkn_to_append.interpreter = self.function_interpreter
                        self.tokens.append(tkn_to_append)
                        internal_structure_count -= 1
                else:
                    tkn_to_append = self.interpreter.next_token()
                    tkn_to_append.interpreter = self.function_interpreter
                    self.tokens.append(tkn_to_append)

            self.tokens.append(Token("ENDSCRIPT", "", self.interpreter))

        self.function_interpreter.setup(tokens=self.tokens, data=self.interpreter.data, bot=self.interpreter.bot)
        self.interpreter.data["funcs"][self.name] = {
            "params": self.params,
            "interpreter": self.function_interpreter
        }
        
        return self
                    

