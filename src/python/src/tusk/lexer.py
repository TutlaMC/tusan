from tusk.token import Token
"""
keywords = [
      
      "then", "elseif", "else",
      "that",
      "times","do","as",
      "what","type",
      "characters","items","all",
      "from","of","by","till",
      "capture",
      "get","post","headers","tson",
      "character","item","number",
      "file", "variable", 
      "with","between",
      "named",
      "for", "can",
      "a", "an", "the","so","to",
      "toall",
      "can","cannot",
      "because",
]

types = ["NUMBER","STRING","BOOL","BOOLEAN","LIST","NOTHING","TSON"]

EFFECTS = [
    "set",
    "print",
    "wait",
    "add","remove","split","replace", 
    "length",
    "input","convert",
    "shell", "python",
    "request",
    "index",
    "read","write","rename",
    "delete",
    "random",
    "import",
]

STRUCTURES = [
    "if","while","function","loop"
]
"""

# May not be the best lexer, but hey- if it works it works and don't touch it, you'll prob mess it up

class Lexer:
    def __init__(self,text, interpreter):
        self.text = text

        self.pos = 0
        self.current_token = None

        self.tokens = []

        self.interpreter = interpreter
      
    def reg(self, name, value):
        self.tokens.append(Token(name.upper(), value, self.interpreter))
        self.ctoken = ""
    
    def classify_tokens(self):
        stuff = self.text.split()

        text = self.text
        reader_pos = 0
        self.ctoken = ""

        in_string = False
        in_comment = False
        hex_count = 0
        in_number = False
        start_quote_type = None     

        for i in "(){}[],;:,":
            text = text.replace(i,f" {i} ")
        text = text.replace("'s "," 's ")
        
        text+="\n"
        while reader_pos < len(text): 
            j = text[reader_pos]
            if in_string:
                if j == start_quote_type:
                    in_string = False
                    self.ctoken = self.ctoken.replace("\\n","\n")
                    self.reg("STRING", self.ctoken)
                else:
                    if start_quote_type=="'" and self.ctoken=="s ":
                        in_string = False
                        self.tokens.append(Token("PROPERTY","'s ",self.interpreter))
                        self.ctoken = ""
                    self.ctoken += j
            elif in_comment:
                if j == "\n":
                    in_comment = False
                    self.ctoken = ""
                else: pass
            elif in_number:
                if j in "0123456789.":
                    self.ctoken += j
                elif j in ["+", "-", "*", "/","*", "%"]:
                    in_number = False
                    self.tokens.append(Token("NUMBER", self.ctoken, self.interpreter))
                    reader_pos -= 1
                elif j in " \t\n":
                    in_number = False
                    self.tokens.append(Token("NUMBER", self.ctoken, self.interpreter))
                    self.ctoken = ""
            elif hex_count > 0:
                if j in "0123456789abcdef":
                    hex_count += 1
                    if hex_count == 7:
                        self.tokens.append(Token("HEX", int("0x" + self.ctoken[1:] + j, 16), self.interpreter))
                        self.ctoken = ""
                        hex_count = 0
                    else:
                        self.ctoken += j
                else:
                    hex_count = 0
            else:
                if j in "(){}[],;:":
                    token_type = {
                        "(": "LEFT_PAR",
                        ")": "RIGHT_PAR",
                        "{": "LEFT_CURLY",
                        "}": "RIGHT_CURLY",
                        "[": "LEFT_SQUARE",
                        "]": "RIGHT_SQUARE",
                        ",": "COMMA",
                        ";": "SEMICOLON",
                        ":": "COLON",
                        "{": "LEFT_CURLY",
                        "}": "RIGHT_CURLY",
                    }[j]
                    self.tokens.append(Token(token_type, j, self.interpreter))
                    self.ctoken = ""
                elif j in ["+", "-", "*", "/","**", "%"]:
                    if text[reader_pos+1].isdigit() and (not text[reader_pos-1].isdigit()): # to allow negative numbers
                        self.ctoken = j
                        in_number = True
                    else:
                        self.tokens.append(Token("OPERATOR", j, self.interpreter))
                elif j == "#":
                    if not (len(text) > reader_pos+6 and all(c.lower() in "0123456789abcdef" for c in text[reader_pos+1:reader_pos+7])):
                        in_comment = True
                        self.ctoken = ""
                    else:
                        hex_count = 1
                        self.ctoken = j
                        print(self.ctoken)
                elif j in ["'", '"']:
                    in_string = True
                    start_quote_type = j
                    self.ctoken = ""
                elif j.isdigit():
                    in_number = True
                    self.ctoken=j
                elif j in " \t\n" or reader_pos == len(text)-1:
                    if reader_pos == len(text)-1 and j not in " \t\n": 
                        self.ctoken += j
                    
                    self.ctoken = self.ctoken.replace(" ","").replace("\n","").replace("\t","")
                    if self.ctoken != "":
                        if self.is_number(self.ctoken):
                            self.tokens.append(Token("NUMBER", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in ["true","false"]:
                            self.tokens.append(Token("BOOL", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken == "nothing":
                            self.tokens.append(Token("NOTHING", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in ["and","or","not","contains","in","|","&"]:
                            self.tokens.append(Token("LOGIC", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in ["<", ">", "<=", ">=", "==", "!=","is"]:
                            self.tokens.append(Token("COMPARISION", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in keywords:
                            self.tokens.append(Token("KEYWORD", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in EFFECTS:
                            self.tokens.append(Token("EFFECT",self.ctoken,self.interpreter))
                            self.ctoken=""
                        elif self.ctoken in types:
                            self.tokens.append(Token("TYPE",self.ctoken, self.interpreter))
                            self.ctoken=""
                        elif self.ctoken in STRUCTURES:
                            self.tokens.append(Token("STRUCTURE", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken.startswith("#") or self.ctoken.startswith("0x"):
                            self.reg("hex", self.ctoken)
                        elif self.ctoken in ["miliseconds","seconds","minutes","hours","days","weeks","months","years","milisecond","second","minute","hour","day","week","month","year"]:
                            if self.ctoken.endswith("s"):
                                self.ctoken = self.ctoken[:-1]
                            self.tokens.append(Token("TIME", self.ctoken, self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken == "end":
                            self.tokens.append(Token("ENDSTRUCTURE",self.ctoken,self.interpreter))
                            self.ctoken = ""
                        elif self.ctoken in ["return","break"]:
                            self.tokens.append(Token("BREAKSTRUCTURE",self.ctoken,self.interpreter))
                            self.ctoken=""
                        else:
                            if not self.ctoken in " \t\n": 
                                self.tokens.append(Token("IDENTIFIER", self.ctoken, self.interpreter))
                                self.ctoken = ""
                else:
                    self.ctoken += j

            reader_pos += 1

        self.tokens.append(Token("ENDSCRIPT", "", self.interpreter))
        return self.tokens
    
    def is_number(self,string):
        try:
            float(string)
            return True
        except:
            return False