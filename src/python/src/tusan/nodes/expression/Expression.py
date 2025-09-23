from tusan.Node import *
from tusan.Variable import *
from tusan.nodes.base.Name import NameNode
from tusan.nodes.base.function.ExecuteFunction import ExecuteFunctionNode

import asyncio



class ExpressionNode(Node):
    def __init__(self, token:Token,rules=[]):
        self.interpreter = token.interpreter
        self.auto_eval = True
        self.rules = rules
        self.returned_var = None
        self.token = token

    async def create(self):
        if self.token.type=="OPERATOR" and self.token.value == "-": # Negative Numbers
            if self.interpreter.get_next_token().type=="NUMBER": 
                e = self.interpreter.next_token().value
                self.interpreter.current_token = Token("NUMBER",int(self.token.value+e),self.interpreter)
                self.token = self.interpreter.current_token

        tkn1 = await TermNode(self.token,rules=self.rules).create()
        if self.token.interpreter.get_next_token().type in ["OPERATOR", "COMPARISION"]:
            operator = self.interpreter.next_token()
            tkn2 = await ExpressionNode(self.interpreter.next_token(),rules=self.rules).create()
            if operator.type == "OPERATOR":
                if operator.value == "+":
                    self.value = tkn1.value + tkn2.value
                elif operator.value == "-":
                    self.value = tkn1.value - tkn2.value
            elif operator.type == "COMPARISION":
                if operator.value == "<":
                    self.value = tkn1.value < tkn2.value
                elif operator.value == ">":
                    self.value = tkn1.value > tkn2.value
                elif operator.value == "<=":
                    self.value = tkn1.value <= tkn2.value
                elif operator.value == ">=":
                    self.value = tkn1.value >= tkn2.value
                elif operator.value == "==":
                    self.value = tkn1.value == tkn2.value
                elif operator.value == "is":
                    self.value = tkn1.value == tkn2.value
                elif operator.value == "!=":
                    self.value = tkn1.value != tkn2.value
            self.type="3en"
        else:
            self.value = tkn1.value
            self.type="1en"
        self.interpreter.debug_msg(self.interpreter.current_token,self.value, "<- expr (node) end")
        return self