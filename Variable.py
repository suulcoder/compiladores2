from Node import Node
from NodeType import NodeType

from modules import getType

class Variable:
    def __init__(self, word_, identities):
        self.word_index = 0
        self.word = word_
        self.identities = identities
        self.current_character = None
        self.current_word = word_
        self.valid_characters = ['(', ')']
        self.getNext()

    def getNext(self):
        if(self.word_index < len(self.word)):
            self.current_character = self.word[self.word_index]
            self.word_index += 1
        else:
            self.current_character = None

    def parse_variable(self):
        while self.current_character != None:
            if self.current_character.isalpha():
                yield self.generateWord()
            elif self.current_character == '.':
                self.getNext()
                if self.current_character == '.':
                    self.getNext()
                    yield Node(NodeType["RANGE"])
            elif self.current_character == '+':
                self.getNext()
                yield Node(NodeType["UNION"])
            elif self.current_character == '-':
                self.getNext()
                yield Node(NodeType["SUBSTRACTION"])
            elif self.current_character == '\'' or self.current_character == '"':
                yield self.generateNode(self.current_character)
            elif self.current_character == ' ':
                self.getNext()

    def generateNode(self, type):
        Node = self.current_character
        self.getNext()
        while self.current_character != None:
            Node += self.current_character
            self.getNext()
            if self.current_character == type:
                Node += self.current_character
                self.getNext()
                break
        if getType(Node, self.identities):
            return getType(Node, self.identities)

    def generateWord(self):
        word = self.current_character
        self.getNext()
        toReturn = None
        while (self.current_character != None 
                and self.current_character != ' '
                and (
                    self.current_character in self.valid_characters 
                    or self.current_character.isalnum())):
            word += self.current_character
            self.getNext()
        if 'CHR(' in word:
            toReturn = None
            if (
                word.find('(') != -1 and 
                word.find(')') != -1 and 
                word.count('(') == 1 and 
                word.count(')') == 1
                ):
                toReturn = word[word.find('(')+1:word.find(')')]
            if toReturn != None and toReturn.isdigit():
                toReturn = chr(int(toReturn))
            toReturn = Node(NodeType["CHAR"], set(toReturn))
        else:
            toReturn = getType(word, self.identities)
        if toReturn != None:
            return toReturn