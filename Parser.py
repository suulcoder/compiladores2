from Node import Node
from NodeType import NodeType
from RegexNode import RegexNode


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.parsed_tree = []
        self.tokens = None
        self.current_token_index = 0
        
    def get_symbol(self):
        token = self.current_token

        if token.type == NodeType["LEFT_PARENTHESIS"]:
            self.getNext()
            toReturn = self.get_expression()
            if self.current_token.type != NodeType["RIGHT_PARENTHESIS"]:
                raise Exception('")" were expected')
            self.getNext()
            return toReturn
        elif token.type == NodeType["ID"]:
            self.getNext()
            return RegexNode(operation=None, value=token.value, type_=token.type, name= token.name)
        elif ( 
            token.type == NodeType["CHAR"] or 
            token.type == NodeType["STRING"]):
            self.getNext()
            return RegexNode(operation=None, value= token.value, type_= token.type)

    def parse(self, tokens):
        self.tokens = tokens
        self.getNext()
        if self.current_token == None:
            return None

        res = self.get_expression()
        return res

    def getNext(self):
        if(self.tokens != None and self.current_token_index < len(self.tokens)):
            self.current_token = self.tokens[self.current_token_index]
            self.current_token_index += 1
        else:
            self.current_token = None

    def get_unique_expression(self):
        toReturn = []
        for token in self.scanner.tokens:
            tokens = token.value
            tokens.insert(0, Node(NodeType["LEFT_PARENTHESIS"], '('))
            tokens.append(Node(NodeType["RIGHT_PARENTHESIS"], ')'))
            tokens.append(Node(NodeType["OR"], '|'))
            toReturn += tokens
        toReturn.pop()
        # for n in toReturn:
        #     print(n.type, n.name, n.value)
        return toReturn

    def get_group(self):
        toReturn = self.get_symbol()

        while (self.current_token != None and 
                (
                    self.current_token.type == NodeType["LEFT_BRACKET"] or
                    self.current_token.type == NodeType["LEFT_KLEENE"]
                )):
            if self.current_token.type == NodeType["LEFT_KLEENE"]:
                self.getNext()
                toReturn = RegexNode(operation='KLEENE', first_node=self.get_expression())

                if self.current_token.type != NodeType["RIGHT_KLEENE"]:
                    raise Exception('"}" were expected')
                self.getNext()
            elif self.current_token.type == NodeType["LEFT_BRACKET"]:
                self.getNext()
                toReturn = RegexNode(operation='Parenthesis', first_node=self.get_expression())
                if self.current_token.type != NodeType["RIGHT_BRACKET"]:
                    raise Exception('"]" were expected')
                self.getNext()
        return toReturn
    
    def get_expression(self):
        toReturn = self.end()

        while self.current_token != None and self.current_token.type == NodeType["OR"]:
            self.getNext()
            toReturn = RegexNode(operation='OR', first_node=toReturn, second_node=self.get_expression())

        return toReturn

    def end(self):
        toReturn = self.get_group()

        while self.current_token != None and self.current_token.type == NodeType["CONCATENATION"]:
            self.getNext()
            toReturn = RegexNode(operation='CONCAT',first_node=toReturn,second_node=self.get_group())

        return toReturn