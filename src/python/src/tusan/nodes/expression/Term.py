from tusan.Node import *

class TermNode(Node):
    def __init__(self, factor:Token,rules=[]):
        self.auto_eval = True
        self.interpreter = factor.interpreter
        self.rules = rules
        self.returned_var = None
        
        self.factor = factor

    async def create(self):
        tkn1 = await FactorNode(self.factor,rules=self.rules).create()
        
        if self.interpreter.get_next_token().type == "OPERATOR":
            operator = self.interpreter.get_next_token()
            if operator.value in ["*","/","**","^"]:
                operator = self.interpreter.next_token()
                tkn2 = await ExpressionNode(self.interpreter.next_token()).create()
                if operator.value == "*":
                    self.value = tkn1.value * tkn2.value
                elif operator.value == "/":
                    self.value = tkn1.value / tkn2.value
                elif operator.value == "^":
                    self.value = int(tkn1.value)^int(tkn2.value)
            else:
                self.value = tkn1.value
        else:
            self.value = tkn1.value
        return self